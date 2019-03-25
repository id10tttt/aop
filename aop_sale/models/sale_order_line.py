# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, float_compare
from odoo.exceptions import UserError
import traceback
import logging



_logger = logging.getLogger(__name__)


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    vin = fields.Many2one('stock.production.lot', 'VIN', domain="[('product_id','=', product_id)]")

    service_product_id = fields.Many2one('product.product',
                                         string='Product',
                                         related='route_id.service_product_id',
                                         domain=[('sale_ok', '=', True)],
                                         ondelete='restrict')

    carrier_id = fields.Many2one('delivery.carrier', string='合同')

    carrier_price = fields.Float(string='合同费用', default=0, digits=dp.get_precision('Product Price'))




    @api.onchange('carrier_id')
    def _onchange_route_id(self):

        _logger.info({
            'carrier_id': self.carrier_id
        })
        self.carrier_price = self.carrier_id.fixed_price

        route_ids = [aop_id.route_id.id for aop_id in self.carrier_id.aop_route_id ]

        if self.order_id.partner_id and self.carrier_id:
            return {
                'domain': {
                    'route_id': [('id', 'in', route_ids)]

                }
            }
        else:
            return {
                'domain': []
            }

    @api.multi
    @api.onchange('product_id')
    def product_id_change(self):
        if self.product_id:
            self.vin = False
            self.product_uom = self.product_id.uom_id.id

    @api.onchange('product_id')
    def _onchange_product_id_set_customer_lead(self):
        pass

    @api.onchange('product_id')
    def _onchange_product_id_uom_check_availability(self):
        pass

    @api.onchange('product_uom_qty', 'product_uom', 'route_id')
    def _onchange_product_id_check_availability(self):
        pass

    @api.depends('state', 'price_reduce', 'product_id', 'untaxed_amount_invoiced', 'qty_delivered')
    def _compute_untaxed_amount_to_invoice(self):
        pass

    @api.depends('state', 'price_reduce', 'service_product_id', 'untaxed_amount_invoiced', 'qty_delivered')
    def _compute_untaxed_amount_to_invoice(self):
        """ Total of remaining amount to invoice on the sale order line (taxes excl.) as
                total_sol - amount already invoiced
            where Total_sol depends on the invoice policy of the product.

            Note: Draft invoice are ignored on purpose, the 'to invoice' amount should
            come only from the SO lines.
        """
        for line in self:
            amount_to_invoice = 0.0
            if line.state in ['sale', 'done']:
                # Note: do not use price_subtotal field as it returns zero when the ordered quantity is
                # zero. It causes problem for expense line (e.i.: ordered qty = 0, deli qty = 4,
                # price_unit = 20 ; subtotal is zero), but when you can invoice the line, you see an
                # amount and not zero. Since we compute untaxed amount, we can use directly the price
                # reduce (to include discount) without using `compute_all()` method on taxes.
                price_subtotal = 0.0
                if line.service_product_id.invoice_policy == 'delivery':
                    price_subtotal = line.price_reduce * line.qty_delivered
                else:
                    price_subtotal = line.price_reduce * line.product_uom_qty

                #price_subtotal += self.carrier_price

                amount_to_invoice = price_subtotal - line.untaxed_amount_invoiced
            line.untaxed_amount_to_invoice = amount_to_invoice

    @api.onchange('service_product_id')
    def _onchange_service_product_id_set_customer_lead(self):
        self.customer_lead = self.product_id.sale_delay


    @api.onchange('service_product_id')
    def _onchange_service_product_id_uom_check_availability(self):
        if not self.product_uom or (self.service_product_id.uom_id.category_id.id != self.product_uom.category_id.id):
            self.product_uom = self.service_product_id.uom_id
        self._onchange_service_product_id_check_availability()

    @api.onchange('product_uom_qty', 'product_uom', 'route_id')
    def _onchange_service_product_id_check_availability(self):
        if not self.service_product_id or not self.product_uom_qty or not self.product_uom:
            self.product_packaging = False
            return {}

        return {}

    @api.multi
    def _compute_tax_id(self):
        for line in self:
            fpos = line.order_id.fiscal_position_id or line.order_id.partner_id.property_account_position_id
            # If company_id is set, always filter taxes by the company
            taxes = line.service_product_id.taxes_id.filtered(
                lambda r: not line.company_id or r.company_id == line.company_id)
            line.tax_id = fpos.map_tax(taxes, line.service_product_id,
                                       line.order_id.partner_shipping_id) if fpos else taxes

    @api.depends('product_uom_qty', 'discount', 'price_unit', 'tax_id', 'carrier_price')
    def _compute_amount(self):
        """
        Compute the amounts of the SO line.
        """
        for line in self:
            price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            taxes = line.tax_id.compute_all(price, line.order_id.currency_id, line.product_uom_qty,
                                            product=line.service_product_id, partner=line.order_id.partner_shipping_id)
            line.update({
                'price_tax': sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])),
                'price_total': taxes['total_included'] + line.carrier_price,
                'price_subtotal': taxes['total_excluded'] + line.carrier_price,
            })

    @api.onchange('product_uom', 'product_uom_qty')
    def product_uom_change(self):
        if not self.product_uom or not self.service_product_id:
            self.price_unit = 0.0
            return
        if self.order_id.pricelist_id and self.order_id.partner_id:
            product = self.service_product_id.with_context(
                lang=self.order_id.partner_id.lang,
                partner=self.order_id.partner_id,
                quantity=self.product_uom_qty,
                date=self.order_id.date_order,
                pricelist=self.order_id.pricelist_id.id,
                uom=self.product_uom.id,
                fiscal_position=self.env.context.get('fiscal_position')
            )
            self.price_unit = self.env['account.tax']._fix_tax_included_price_company(self._get_display_price(product),
                                                                                      product.taxes_id, self.tax_id,
                                                                                      self.company_id)

    @api.multi
    @api.onchange('service_product_id')
    def service_product_id_change(self):
        if not self.service_product_id:
            return {'domain': {'product_uom': []}}

        # remove the is_custom values that don't belong to this template
        for pacv in self.product_custom_attribute_value_ids:
            if pacv.attribute_value_id not in self.service_product_id.product_tmpl_id._get_valid_product_attribute_values():
                self.product_custom_attribute_value_ids -= pacv

        # remove the no_variant attributes that don't belong to this template
        for ptav in self.product_no_variant_attribute_value_ids:
            if ptav.product_attribute_value_id not in self.service_product_id.product_tmpl_id._get_valid_product_attribute_values():
                self.product_no_variant_attribute_value_ids -= ptav

        vals = {}
        domain = {'product_uom': [('category_id', '=', self.service_product_id.uom_id.category_id.id)]}
        if not self.product_uom or (self.service_product_id.uom_id.id != self.product_uom.id):
            vals['product_uom'] = self.service_product_id.uom_id
            vals['product_uom_qty'] = self.product_uom_qty or 1.0

        product = self.service_product_id.with_context(
            lang=self.order_id.partner_id.lang,
            partner=self.order_id.partner_id,
            quantity=vals.get('product_uom_qty') or self.product_uom_qty,
            date=self.order_id.date_order,
            pricelist=self.order_id.pricelist_id.id,
            uom=self.product_uom.id
        )

        result = {'domain': domain}

        title = False
        message = False
        warning = {}
        if product.sale_line_warn != 'no-message':
            title = _("Warning for %s") % product.name
            message = product.sale_line_warn_msg
            warning['title'] = title
            warning['message'] = message
            result = {'warning': warning}
            if product.sale_line_warn == 'block':
                self.service_product_id = False

        name = self.get_sale_order_line_multiline_description_sale(product)

        vals.update(name=name)

        self._compute_tax_id()

        if self.order_id.pricelist_id and self.order_id.partner_id:
            vals['price_unit'] = self.env['account.tax']._fix_tax_included_price_company(self._get_display_price(product), product.taxes_id, self.tax_id, self.company_id)
        self.update(vals)

        return result
