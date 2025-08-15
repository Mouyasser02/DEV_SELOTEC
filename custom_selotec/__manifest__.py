# -*- coding: utf-8 -*-



{
    'name': 'CUSTOM SELOTEC',
    'version': '15.0',
    'category': 'Custom',
    'summary': '',
    'description': """

       """,
    'website': 'exploit-consult.com',
    'depends': ['base', 'stock',],
    'data': [


        #'security/ir.model.access.csv',
        

        'views/product_template_view.xml',
        'views/stock_move_line_view.xml',
        'views/stock_production_lot_view.xml',


        

        
    ],

    'installable': True,
    'auto_install': False,
    'application': True,

    
    
}
