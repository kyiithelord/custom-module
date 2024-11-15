from odoo import fields,models,api,_


class CustomerInfo(models.Model):
  _inherit="res.partner"


  customer_info = fields.Text(string="Customer Info")
  ref = fields.Char(string="reference", default = lambda self:_('New'),readonly=True)





  @api.model_create_multi
  def create(self,vals_list):
    records = super(CustomerInfo,self).create(vals_list)

    for record in records:
      if record.ref == _('New'):
        sequence = self.env['ir.sequence'].next_by_code('res.partner')
        record.ref = f'{record.name} - {sequence}'