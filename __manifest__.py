# -*- coding: utf-8 -*-
{
    'name': "Fleet Partner",

    'summary': """
        Submit info, documents and check status of partners""",

    'description': """
        Module to manage information related to the submit
        and status of partners using the service of TraxiBusiness
    """,
    
    'author': "Traxion - Demian Avila",
    "website": "https://traxi.mx",
    

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
    ],

}
