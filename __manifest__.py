# -*- coding: utf-8 -*-



{
    'name': 'Data Cleaning Enhacement Module',
    'version': '1.0',
    'license': 'OPL-1',
    'author': 'Odoo Inc',
    'category': '',
    'summary': 'Add additional functionality to the data cleaning module',
    'description': """
    """,
    'assets': {
        'web.assets_qweb': [
            'odoo_data_cleaning/static/src/xml/bsa_import.xml'           
        ],
        'web.assets_backend': [
            (
                'after',
                'base_import/static/src/legacy/js/import_action.js',
                'odoo_data_cleaning/static/src/js/bsa_import_actions.js'
            ),        
        ]
    },
    'depends': ['sale','base_import','web'],
    'data': [],
             
}