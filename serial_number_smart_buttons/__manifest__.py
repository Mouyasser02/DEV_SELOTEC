{
    'name': 'SERIAL NUMBER SMART BUTTONS',
    'version': '15.0.0.0.0',
    'category': 'Sale/Contacts',
    'description': """
This module is used to define smart buttons on the contacts form views that:
    - Shows the serial numbers that have been received or returned of the selected product (Product smart button).
       """,
    'author': 'Facilitator',
    'website': 'exploit-consult.com',
    'depends': ['custom_selotec', 'sale_management', 'contacts'],
    'data': [
        'views/res_partner_view.xml',
        'views/stock_production_lot_view.xml',
    ],

    'installable': True,
    'auto_install': False,
    'application': True,

    
    
}
