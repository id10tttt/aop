# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductProduct(models.Model):
    _inherit = 'product.template'
    _description = 'add VIN code and product type'

    #vin_code = fields.Char('VIN Code')
    vin = fields.Char('VIN')    #由于其它地方都是vin,因此修改了下定义
    type = fields.Selection(selection_add=[('storable_service', 'Storable Service')])
