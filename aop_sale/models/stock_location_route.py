# -*_ coding :utf-8 -*-

from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class StockLocationRoute(models.Model):
    _inherit = 'stock.location.route'

    service_product_id = fields.Many2one('product.product', string='Fee Type', domain=[('sale_ok', '=', True)],
                                         change_default=True, ondelete='restrict')
