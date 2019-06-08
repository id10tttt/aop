# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from odoo import api, fields, models, _
import logging

_logger = logging.getLogger(__name__)


class StockPickingBatch(models.Model):
    _inherit = "stock.picking.batch"

    car_no = fields.Char(string='装车编号')

    partner_id = fields.Many2one('res.partner', string='Vendor')

    picking_purchase_id = fields.Many2one('purchase.order', 'Purchase')

    dispatch_type = fields.Selection([('zy', u'中央调度'),
                                      ('tl', u'铁路调度'),
                                      ('gl', u'公路调度')
                                      ],
                                     string='调度类型',
                                     store=True)

    plan_number = fields.Integer(string='计划数量', default=1)

    plate_number = fields.Char(string='车牌号')

    mount_car_plan_ids = fields.One2many('mount.car.plan', 'stock_picking_batch_id', string='装车计划')

    def create_purchase_order(self):
        data = self._get_purchase_data()
        _logger.info({
            'data': data
        })
        res = self.env['purchase.order'].create(data)

        self.write({
            'picking_purchase_id': res.id
        })

    def _get_purchase_data(self):
        vendor = self.partner_id.id
        res = {
            'partner_id': vendor,
            'user_id': self.env.user.id,
            'invoice_status': 'no',
            'date_order': fields.Datetime.now(),
            'stock_picking_batch_id': self.id
        }
        line_data = self._get_purchase_line_data()
        res.update({
            'order_line': line_data
        })
        return res

    def _get_purchase_line_data(self):
        res = []

        product_ids = []

        for picking in self.picking_ids:
            for line_id in picking.move_ids_without_package:
                data = {
                    'product_id': line_id.product_id.id,
                    #'service_product_id': line_id.picking_type_id.product_id.id,
                    'product_qty': line_id.product_uom_qty,
                    'name': line_id.product_id.name,
                    'date_planned': fields.Datetime.now(),
                    'price_unit': line_id.product_id.lst_price,
                    'product_uom': line_id.product_id.uom_id.id
                }

                if not data['product_id'] in product_ids:
                    product_ids.append(data['product_id'])
                    res.append((0, 0, data))


        return res


class MountCarPlan(models.Model):
    _name = "mount.car.plan"

    name = fields.Char(string='车型')

    layer_option = fields.Selection([
        ('on_layer', u'上层'),
        ('under_layer', u'下层')
    ], string=u'上下层')

    stock_picking_batch_id = fields.Many2one('stock.picking.batch', '批量调度单')