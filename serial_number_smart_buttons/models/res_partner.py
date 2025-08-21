from odoo import models, fields, api


class res_partner(models.Model):
    _inherit = "res.partner"

    lot_ids = fields.Many2many('stock.production.lot', compute='_compute_lot_ids')

    def _compute_lot_ids(self):
        for rec in self:
            # Get all move lines for the partner with tracked products
            move_lines = rec.env['stock.move.line'].search([
                ('move_id.partner_id', '=', rec.id),
                ('product_id.tracking', '!=', 'none'),
                ('state', '=', 'done'),
                ('picking_code', 'in', ['outgoing', 'incoming']),
            ])

            # Separate move lines by picking code
            outgoing_lines = move_lines.filtered(lambda ml: ml.picking_code == 'outgoing')
            incoming_lines = move_lines.filtered(lambda ml: ml.picking_code == 'incoming')

            # Identify incoming lines that are returns of returns (should be treated as outgoing)
            incoming_to_treat_as_outgoing = incoming_lines.filtered(
                lambda ml: ml.move_id.move_orig_ids and
                           all(orig_move.picking_code == 'incoming' for orig_move in ml.move_id.move_orig_ids)
            )


            # Combine regular outgoing lines with the special incoming lines (returns of returns)
            all_outgoing_lot_lines = outgoing_lines | incoming_to_treat_as_outgoing

            # Find all lines that have been returned (regular returns)
            returned_lines = incoming_lines.filtered(
                lambda ml: ml.move_id.move_orig_ids and
                           any(orig_move.picking_code == 'outgoing' for orig_move in ml.move_id.move_orig_ids)
            )


            # Get the lot IDs from returned lines to exclude them
            returned_lot_ids = returned_lines.mapped('lot_id')

            # Final filter: exclude any lines that have lot IDs that were returned
            # But keep returns of returns even if they have the same lot ID
            final_lines = all_outgoing_lot_lines.filtered(
                lambda ml: ml.lot_id not in returned_lot_ids or ml in incoming_to_treat_as_outgoing
            )


            # Assign the lot IDs
            rec.lot_ids = final_lines.mapped('lot_id')



    def action_view_stock_production_lot(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id(
            "serial_number_smart_buttons.serial_number_smart_buttons_action_production_lot")
        action['domain'] = [('id', 'in', self.lot_ids.ids)]
        action['context'] = {
            'set_product_readonly': True,
            'default_company_id': (self.company_id or self.env.company).id,
        }
        return action
