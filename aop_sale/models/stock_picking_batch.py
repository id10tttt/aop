# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, float_compare
from odoo.exceptions import UserError
import traceback
import logging

_logger = logging.getLogger(__name__)



class StockPickingBatch(models.Model):
    _inherit = "stock.picking.batch"

    car_no = fields.Char(string='车次号')