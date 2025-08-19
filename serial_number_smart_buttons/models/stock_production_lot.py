from odoo import fields, models, api

class stock_production_lot(models.Model):
    _inherit = "stock.production.lot"

    last_delivery_date = fields.Datetime("Last delivery date", compute="_compute_last_delivery_date")

    def _compute_last_delivery_date(self):
        serial_products = self.filtered(lambda l: l.product_id.tracking != 'none')
        delivery_ids_by_lot = serial_products._find_delivery_ids_by_lot()
        (self - serial_products).last_delivery_date = False
        for lot in serial_products:
            if lot.product_id.tracking != 'none' and len(delivery_ids_by_lot[lot.id]) > 0:
                lot.last_delivery_date = self.env['stock.picking'].browse(delivery_ids_by_lot[lot.id]).sorted(key='date_done', reverse=True)[0].date_done
            else:
                lot.last_delivery_date = False
