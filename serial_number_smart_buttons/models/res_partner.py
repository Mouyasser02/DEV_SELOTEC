from odoo import models, fields, api


class res_partner(models.Model):
    _inherit = "res.partner"

    lot_ids = fields.Many2many('stock.production.lot', compute='_compute_lot_ids')

    def _compute_lot_ids(self):
        for rec in self:
            # Get all relevant moves in a single query with proper domain
            moves = rec.env['stock.move'].search([
                ('partner_id', '=', rec.id),
                ('product_id.tracking', '!=', 'none'),
                ('picking_code', 'in', ['outgoing', 'incoming'])
            ])

            # Separate moves by type using mapped approach (more efficient)
            outgoing_moves = moves.filtered(lambda m: m.picking_code == 'outgoing')
            incoming_moves = moves.filtered(lambda m: m.picking_code == 'incoming')

            # Get all move_orig_ids from incoming moves in one go
            all_incoming_orig_ids = incoming_moves.mapped('move_orig_ids')

            # First filter: remove outgoing moves that are origin of any incoming move
            filtered_outgoing = outgoing_moves - all_incoming_orig_ids

            # Second filter: find incoming moves that have incoming move_orig_ids
            incoming_with_incoming_orig = incoming_moves.filtered(
                lambda m: any(orig.picking_code == 'incoming' for orig in m.move_orig_ids)
            )

            # Get outgoing move_orig_ids from the filtered incoming moves
            outgoing_orig_from_incoming = incoming_with_incoming_orig.mapped('move_orig_ids').filtered(
                lambda m: m.picking_code == 'outgoing'
            )

            # Combine the results
            final_moves = filtered_outgoing | outgoing_orig_from_incoming

            # Assign lot_ids
            rec.lot_ids = final_moves.mapped('lot_ids')


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
