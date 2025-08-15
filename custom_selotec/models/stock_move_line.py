# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from odoo import tools, _
from odoo.exceptions import ValidationError, AccessError



import logging
_logger = logging.getLogger(__name__)


class stock_move_line(models.Model):
    _inherit = "stock.move.line"



    type_article = fields.Selection(
        [('Mono Sim', 'Mono Sim'),
         ('Double Sim', 'Double Sim'),
         ('Accessoires', 'Accessoires')],
        string="Type", related="lot_id.type_article"
    )

    ime1 = fields.Char(string="IME1", related="lot_id.ime1")
    ime2 = fields.Char(string="IME2", related="lot_id.ime2")

    the_partner_id = fields.Many2one(
        'res.partner', 
        string='Partner', 
        related='move_id.picking_id.partner_id', 
        readonly=True, 
        store=True
    )

    @api.onchange('product_id') 
    def _onchange_the_product_id(self): 
        if self.product_id: 
            if self.product_id.tracking == 'serial':

                all_num_series_per_product = self.env['stock.production.lot'].search([('product_id', '=', self.product_id.id), ('company_id', '=', self.company_id.id)])

                if all_num_series_per_product:

                    valid_num_series_per_product = []

                    for num_serie in all_num_series_per_product:

                        message = None

                        message, recommended_location = self.env['stock.quant']._check_serial_number(self.product_id,
                                                                                                     num_serie,
                                                                                                     self.company_id,
                                                                                                     self.location_id,
                                                                                                     self.picking_id.location_id)

                        if not message:

                            valid_num_series_per_product.append(num_serie.id)

                    if valid_num_series_per_product :

                        dynamic_domain = [('id', 'in', valid_num_series_per_product)]  # Example interval
                        return {'domain': {'lot_id': dynamic_domain}}
                    else:
                        # Reset to default domain
                        return {'domain': {'lot_id': []}}



    
    



