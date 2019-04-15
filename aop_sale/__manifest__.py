# -*- coding: utf-8 -*-
{
    'name': "aop_sale",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "1di0t",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['sale', 'sale_management', 'sale_stock', 'delivery', 'stock_picking_batch', 'purchase_stock', 'barcodes'],

    # always loaded
    'data': [
        'security/aop_sale_groups.xml',
        'security/ir.model.access.csv',
        'views/sale_order_views.xml',
        'views/delivery_carrier.xml',
        'views/sale_views.xml',
        'views/stock_menu_views.xml',
        'views/stock_picking_batch_view.xml',
        'views/purchase_views.xml',
        'views/stock_picking_views.xml',
        'views/stock_picking.xml',
        'views/purchase_order_views.xml',
        #'views/sale_stock_views.xml',
        'views/stock_location_route.xml',
        'views/subsidy_debit_order.xml',
        'views/stock_quant_views.xml',
        'views/stock_move_views.xml'
    ],
}