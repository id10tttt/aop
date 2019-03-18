# -*- coding: utf-8 -*-

from odoo import models, fields, api


class DeliveryCarrier(models.Model):
    _inherit = 'delivery.carrier'

    partner_id = fields.Many2one('res.partner', 'Partner')
    # aop_route_id = fields.Many2one('aop.route', 'Aop Route ID')
    aop_route_id = fields.One2many('aop.route', 'aop_id', 'Aop Route ID')

    aop_route_ids = fields.Many2many('aop.route', string='AOP route')

