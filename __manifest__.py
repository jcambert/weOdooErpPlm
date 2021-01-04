# -*- coding: utf-8 -*-
{
    'name': "We Addon ERP/PLM",

    'summary': """
        Extenssion Addon that manage ERP""",

    'description': """
        Addon ERP to manage PLM 
    """,

    'author': "We",
    'website': "http://jc.ambert.free.fr",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Productivity',
    'version': '1.0',
    # any module necessary for this one to work correctly
    'depends': ['mrp','base','product', 'mail', 'uom','mrp'],

    # always loaded
    'data': [
        #'security/plm_security.xml',
        # 'security/ir.model.access.csv',
        'views/mrp_plm_views_menu.xml',
        'views/mrp_plm_views.xml',
        #'views/mrp_plm_production_views.xml',
        'views/product_views.xml',
        #'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
     #   'demo/demo.xml',
    ],
    #Module Installation
    'installable': True,
    'application': True,
    'auto_install': False
}
