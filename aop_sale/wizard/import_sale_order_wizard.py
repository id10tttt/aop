# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, RedirectWarning
from odoo.exceptions import UserError


class ImportSaleOrderXWizard(models.TransientModel):
    """ 创建销售订单 """
    _name = 'import.sale.order.wizard'

    import_file = fields.Binary(
        string='导入文件 (*.xlsx)',
    )

    order_source = fields.Selection([
        ('host', '主机厂原订单'),
        ('otd', 'OTD系统订单'),
        ('other', '其它订单')
        ],
        string='订单来源',
        default='host'
    )

    state = fields.Selection(
        [('choose', 'Choose'),
         ('get', 'Get')],
        default='choose'
    )

    @api.multi
    def action_import(self):
        #raise UserError('订单数据项不完整!')
        #raise UserError('各项基础数据匹配失败!')

        raise UserError('订单重复导入!')



        return

