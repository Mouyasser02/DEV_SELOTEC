from odoo import models, fields, api


class res_partner(models.Model):
    _inherit = "res.partner"

    sub_period = fields.Integer("Subscription period", default=1)
    sub_period_unit = fields.Selection([('day', 'Day'), ('month', 'Month')], "Subscription period unit", default="day")