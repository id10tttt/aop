# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class SaleLineExternal(models.Model):
    _inherit = 'sale.order.line'

    vin_code = fields.Char('VIN Code')

    service_product_id = fields.Many2one('product.product', string='Fee Type', domain=[('sale_ok', '=', True)],
                                         ondelete='restrict')

    @api.onchange('order_id.partner_id', 'order.carrier_id')
    def _onchange_route_id(self):
        if self.order_id.partner_id or self.order_id.carrier_id:
            _logger.info({
                '*' * 10: self.order_id,
                '=' * 10: self.order_id.partner_id
            })
            return {
                'domain': {
                    'route_id': [('partner_id', '=', self.order_id.partner_id.id)]
                }
            }
        else:
            return {
                'domain': []
            }


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _create_delivery_line(self, carrier, price_unit):
        if self.carrier_id.aop_route_ids if self.carrier_id else False:
            delivery_price_value = self._parse_delivery_price(carrier, price_unit)
            self.order_line.write(delivery_price_value)
        else:
            res = super(SaleOrder, self)._create_delivery_line(carrier, price_unit)

            return res

    def _parse_delivery_price(self, carrier, price_unit):
        if self.partner_id:
            # set delivery detail in the customer language
            carrier = carrier.with_context(lang=self.partner_id.lang)

        # Apply fiscal position
        taxes = carrier.product_id.taxes_id.filtered(lambda t: t.company_id.id == self.company_id.id)
        taxes_ids = taxes.ids
        if self.partner_id and self.fiscal_position_id:
            taxes_ids = self.fiscal_position_id.map_tax(taxes, carrier.product_id, self.partner_id).ids

        route_id = self.carrier_id.aop_route_ids.route_id.id
        # Create the sales order line
        values = {
            'product_uom_qty': 1,
            'service_product_id': carrier.product_id.id,
            'price_unit': price_unit,
            'tax_id': [(6, 0, taxes_ids)],
            'is_delivery': True,
            # 'route_id': route_id
        }

        return values

    @api.multi
    def _remove_delivery_line(self):
        if self.carrier_id.aop_route_ids if self.carrier_id else False:
            pass
        else:
            return super(SaleOrder, self)._remove_delivery_line()

    @api.onchange('partner_id')
    def _domain_delivery_carrier(self):
        if self.partner_id:
            return {'domain': {'carrier_id': [('partner_id', '=', self.partner_id.id)]}}
        else:
            return {
                'domain': []
            }

    def open_vin_picking(self):
        action = self.env.ref('stock.action_picking_tree_all').read()[0]

        pickings = self.mapped('picking_ids')
        if len(pickings) > 1:
            action['domain'] = [('id', 'in', pickings.ids)]
        elif pickings:
            action['views'] = [(self.env.ref('stock.view_picking_form').id, 'form')]
            action['res_id'] = pickings.id
        return action
