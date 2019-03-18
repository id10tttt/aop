# -*- coding: utf-8 -*-
from odoo import http

# class AopPurchase(http.Controller):
#     @http.route('/aop_purchase/aop_purchase/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/aop_purchase/aop_purchase/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('aop_purchase.listing', {
#             'root': '/aop_purchase/aop_purchase',
#             'objects': http.request.env['aop_purchase.aop_purchase'].search([]),
#         })

#     @http.route('/aop_purchase/aop_purchase/objects/<model("aop_purchase.aop_purchase"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('aop_purchase.object', {
#             'object': obj
#         })