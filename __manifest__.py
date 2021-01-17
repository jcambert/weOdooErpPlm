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
    'depends': ['mrp','base','product', 'mail', 'uom'],

    # always loaded
    'data': [
        'security/plm_security.xml',
        'security/ir.model.access.csv',
        'data/mrp_plm_data.xml',
        'views/mrp_plm_views_menu.xml',
        'views/mrp_plm_type_views.xml',
        'views/mrp_plm_stage_views.xml',
        'views/mrp_plm_tag_views.xml',
        'views/mrp_plm_views.xml',
        'views/product_views.xml',
        'report/plm_report_views_main.xml',
        'report/plm_production_templates.xml'
    ],
    'qweb': ['static/src/xml/*.xml'],
    # only loaded in demonstration mode
    'demo': ['data/mrp_plm_demo.xml'],
    
    #Module Installation
    'installable': True,
    'application': True,
    'auto_install': False
}
