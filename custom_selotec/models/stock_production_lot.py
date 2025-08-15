# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from odoo import tools, _
from odoo.exceptions import ValidationError, AccessError



import logging
_logger = logging.getLogger(__name__)


class stock_production_lot(models.Model):
    _inherit = "stock.production.lot"


    type_article = fields.Selection(
        [('Mono Sim', 'Mono Sim'),
         ('Double Sim', 'Double Sim'),
         ('Accessoires', 'Accessoires')],
        string="Type", related="product_id.type_article", store=True
    )

    ime1 = fields.Char(string="IME1")
    ime2 = fields.Char(string="IME2")

    _sql_constraints = [
        ('unique_lot_name', 'unique(name)', 'Lot/numéro de série est unique!'),
        ('unique_ime1', 'unique(ime1)', 'IME1 est unique!'),
        ('unique_ime2', 'unique(ime2)', 'IME2 est unique!'),
    ]

    @api.constrains('type_article', 'ime1', 'ime2')
    def _check_ime_obligation(self):
        for record in self:
            if record.type_article:
                if record.type_article == 'Mono Sim' and not record.ime1:

                    raise ValidationError("IME1 est obligatoire si Type est Mono Sim!")

                if record.type_article == 'Double Sim' and not record.ime1:

                    raise ValidationError("IME1 est obligatoire si Type est Double Sim!")

                if record.type_article == 'Double Sim' and not record.ime2:

                    raise ValidationError("IME2 est obligatoire si Type est Double Sim!")

                # Ensure ime2 is empty for 'Mono Sim'
                if record.type_article == 'Mono Sim' and record.ime2:
                    raise ValidationError("IME2 ne doit pas être renseigné pour le type Mono Sim!")


             
                
    



