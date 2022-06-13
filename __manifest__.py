# -*- coding: utf-8 -*-
{
    'name': "Traxi Documents Manager",
    'summary': """
        Manage documents""",
    'description': """
        Module to manage documents and the relations to different models, 
        and toggle between multiple options, such like s3 storage and BlackTrust 
        validation
        Main Features
        -------------
        * Create documents models
        * Relate documents models with other models
        * Add flag to documents to determine if s3 storage is needed
        * Add flag to documents to determine if blacktrust validation is needed
    """,
    'author': "Traxion - (Ferdinand Bracho - Demian Avila)",
    "website": "https://traxi.mx",
    'version': '0.1',
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Customizations',
    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # Security
        'security/ir.model.access.csv',

        # Views
        'views/views.xml',
        'views/config_extender_form_view.xml'
    ],
    "installable": True,
    "assets": {
        "web.assets_backend": [
            "trx_docs/static/src/**/*",
        ],
    },
    "application": True,
    "license": "LGPL-3",

}
