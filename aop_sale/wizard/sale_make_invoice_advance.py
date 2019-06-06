# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import time

from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError


class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"

    # advance_payment_method = fields.Selection([
    #     ('delivered', '可创建明细行'),
    #     ('all', '可创建明细 ( 扣除预付定金 )'),
    #     ('percentage', '预付定金(百分比)'),
    #     ('fixed', '预付定金(固定总额)')
    #     ], string='你要怎样创建台账?')

    advance_payment_method = fields.Selection([
        ('delivered', u'主产品明细'),
        ('all', u'子产品明细'),
        ('percentage', u'主产品百分比'),
        ('fixed', u'子产品百分比'),
        ('main_product_amount', u'主产品部分金额'),
        ('child_product_amount', u'子产品部分金额'),
    ], string=u'创建结算清单')

    reconciliation_batch_no = fields.Char('Reconciliation batch no')
