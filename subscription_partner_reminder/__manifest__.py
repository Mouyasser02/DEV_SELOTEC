{
    'name': 'SUBSCRIPTION PARTNER REMINDER',
    'version': '15.0.0.0.0',
    'category': 'Contacts/Subscription',
    'description': """
This module is used to define fields in the contact form view:

    - Period : Int field that represents the value.
    - Period unit : Selection field that represents the unit either day or month.

Also it creates an automation rule that runs everyday to send a relaunch
mail to the user if today is between the period value and the end date of the subscription date.

Besides it requires a mail template that this module provide to include the customer name and the subscription details.

       """,
    'author': 'Facilitator',
    'website': 'exploit-consult.com',
    'depends': ['subscription_oca', 'base_automation', 'contacts'],
    'data': [
        "data/cron_reminder_mail.xml",
        "data/reminder_mail_template.xml",
        "views/res_partner_view.xml",
    ],

    'installable': True,
    'auto_install': False,
    'application': True,
}
