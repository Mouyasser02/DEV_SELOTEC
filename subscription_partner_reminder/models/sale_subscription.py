from odoo import models, fields, api, _
from datetime import date, timedelta


class sale_subscription(models.Model):
    _inherit = "sale.subscription"

    def send_subscription_reminder(self):
        """Send subscription reminder email to partner"""
        self.ensure_one()
        # Get the email template
        template = self.env.ref('subscription_partner_reminder.subscription_partner_reminder_reminder_mail_template')

        if self.partner_id:
            # Send the email
            template.send_mail(self.id, force_send=True)



    def cron_send_reminder_mail(self):
        today = date.today()
        for subscription in self.search([]):
            if subscription.partner_id:
                if subscription.stage_id.type == "in_progress":
                    reminder_days = subscription.partner_id.sub_period * 30 if subscription.partner_id.sub_period_unit == "month" else subscription.partner_id.sub_period
                    if reminder_days and subscription.date:
                        if ((subscription.date - today) >= timedelta(days=0)) and ((subscription.date - today) <= timedelta(days=reminder_days)):
                            subscription.send_subscription_reminder()