# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    src_partner_id = fields.Many2one('res.partner', related='picking_type_id.src_partner_id')
    des_partner_id = fields.Many2one('res.partner', related='picking_type_id.des_partner_id')

    picking_purchase_id = fields.Many2one('purchase.order', 'Purchase')

    def generate_purchase_order(self):
        data = self._get_purchase_data()

        res = self.env['purchase.order'].create(data)

        self.write({
            'picking_purchase_id': res.id
        })
        _logger.info({
            '#' * 60: res.id
        })

    def _get_purchase_data(self):
        vendor =self._get_vendor_partner()
        res = {
            'picking_type_id': self.picking_type_id.id,
            'partner_id': vendor[0],
            'user_id': self.env.user.id,
            'invoice_status': 'no',
            'date_order': fields.Datetime.now(),
            'stock_picking_id': self.id
        }
        line_data = self._get_purchase_line_data()
        res.update({
            'order_line': line_data
        })
        return res

    def _get_vendor_partner(self):
        vendors = []
        for line_id in self.move_ids_without_package:
            if not line_id.product_id.seller_ids:
                raise UserError(u'请先给产品 [ {} ] 指定供应商!'.format(
                    line_id.product_id.name
                ))
            _logger.info({
                '=' * 50: line_id.product_id.seller_ids
            })
            vendors.append(line_id.product_id.seller_ids[0].name.id)
        if len(list(set(vendors))) > 1:
            raise UserError(u'存在多个供应商! ')
        _logger.info({
            '*' * 100: vendors
        })
        return list(set(vendors))

    def _get_purchase_line_data(self):
        res = []
        for line_id in self.move_ids_without_package:
            res.append((0, 0, {
                'product_id': line_id.product_id.id,
                'product_qty': line_id.product_uom_qty,
                'name': line_id.product_id.name,
                'date_planned': fields.Datetime.now(),
                'price_unit': line_id.product_id.lst_price,
                'product_uom': line_id.product_id.uom_id.id
            }))
        return res
