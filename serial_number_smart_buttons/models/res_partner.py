from odoo import models, fields, api


class res_partner(models.Model):
    _inherit = "res.partner"

    lot_ids = fields.Many2many('stock.production.lot', compute='_compute_lot_ids')


    def _compute_lot_ids(self):
        for rec in self:
            moves = rec.env['stock.move'].search([('partner_id', '=', rec.id), ('product_id.tracking', '!=', 'none')])
            rec.lot_ids = moves.mapped(lambda x: x.lot_ids)


    # This method to review
    def action_view_stock_production_lot(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id("serial_number_smart_buttons.serial_number_smart_buttons_action_production_lot")
        action['domain'] = [('id', 'in', self.lot_ids.ids)]
        action['context'] = {
            'set_product_readonly': True,
            'default_company_id': (self.company_id or self.env.company).id,
        }
        return action
