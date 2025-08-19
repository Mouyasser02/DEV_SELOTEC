# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from odoo import tools, _
from odoo.exceptions import ValidationError, AccessError



import logging
_logger = logging.getLogger(__name__)


class product_template(models.Model):
    _inherit = "product.template"


    type_article = fields.Selection(
        [('Mono Sim', 'Mono Sim'),
         ('Double Sim', 'Double Sim'),
         ('Accessoires', 'Accessoires')],
        string="Type", required=True, default='Accessoires'
    )




    


    


