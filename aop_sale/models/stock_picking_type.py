# -*- coding: utf-8 -*-

from odoo import models, fields, api


class StockPickingType(models.Model):
    _inherit = 'stock.picking.type'

    src_partner_id = fields.Many2one('res.partner', string='Src partner')
    des_partner_id = fields.Many2one('res.partner', string='Des partner')

    product_id = fields.Many2one('product.product')

    aging = fields.Float('时效', default=1)

    operate_type_id = fields.Many2one('operate.type', string="操作类型")

    operate_type_name = fields.Char('作业内容', related='operate_type_id.name')


class OperateType(models.Model):
    _name = 'operate.type'

    name = fields.Char(string='作业内容', required=True)

    #code = fields.Char(string='操作编码')