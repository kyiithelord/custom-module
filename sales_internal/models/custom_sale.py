from odoo import api,fields,models,_


class CustomSale(models.Model):
  _inherit = 'sale.order'

  delivery_note = fields.Text(string="Delivery Note")