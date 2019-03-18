# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'AOP to-be project',
    'version': '1.0',
    'summary': 'AOP to-be project',
    'author': '1di0t',
    'description': "",
    'website': '',
    'depends': ['product', 'barcodes', 'stock', 'sale', 'delivery'],
    'sequence': 13,
    'data': [
        'security/ir.model.access.csv',
        'views/product_views.xml',
        'views/delivery_carrier.xml',
        'views/sale_stock_views.xml',
        'views/sale_views.xml',
        'views/stock_picking.xml',
        'views/stock_picking_type.xml',
        'views/purchase_order_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
