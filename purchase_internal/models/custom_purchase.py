from odoo import fields,api,models,_


class CustomPurchase(models.Model):
  _inherit = 'product.template'

  customer_account_number = fields.Char(string="Account Number")
  custom_remark = fields.Char(string="Remark")