# -*_ coding :utf-8 -*-

from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class SubsidyDebitOrder(models.Model):
    _inherit = 'sale.order'
    _name = 'subsidy.debit.order'
    _description = u'继承 sale.order 表'

