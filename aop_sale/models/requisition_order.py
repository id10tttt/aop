# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class RequisitionOrder(models.Model):
    _inherit = 'sale.order'
    _description = u'调度单'

    order_type = fields.Selection([('dispatch', u'调度订单'), ('customer', u'客户订单')],
                                  store=True,
                                  compute='_get_order_type')

    @api.depends('partner_id')
    def _get_order_type(self):
        _logger.info({
            'order_type_context' * 100: self._context.get('order_type_context')
        })
        if self._context.get('order_type_context', False):
            self.order_type = 'dispatch'
        else:
            self.order_type = 'customer'
