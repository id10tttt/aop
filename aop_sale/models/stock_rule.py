# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, float_compare
from odoo.exceptions import UserError
import traceback
import logging



_logger = logging.getLogger(__name__)


class ProcurementGroup(models.Model):
    _inherit = 'procurement.group'

    #@api.model
    #def _get_rule(self, product_id, location_id, values):

    #   values.update({'warehouse_id': False})

    #    return super(ProcurementGroup, self)._get_rule(product_id, location_id, values)