from odoo import api,fields,models,_


class CustomSaleOrderLine(models.Model):
  _inherit = "sale.order.line"

  custom_remark = fields.Text(string="Remark")
