from odoo import fields,api,models,_


class CustomSale(models.Model):
  _inherit = 'product.template'
  _rec_name = 'ref'

  ref = fields.Char(string="Reference",default = lambda self:_("New"),readonly=True)

  @api.model_create_multi
  def create(self, vals_list):
    records = super(CustomSale,self).create(vals_list)

    for record in records:
      if record.ref == _('New'):
        sequence = self.env['ir.sequence'].next_by_code('product.template')
        record.ref = f'{sequence} - {record.name}'
        
    return records

 

  # def name_get(self):
  #   res = []
  #   for rec in self:
  #     name = f'{rec.ref} - {rec.name}'
  #     res.append((rec.id,name))
  #   return res  






  # @api.model_create_multi
  # def create(self,vals_list):
  #   for vals in vals_list:
  #     vals['ref'] = self.env['ir.sequence'].next_by_code('product.template')
  #   return super(CustomRef,self).create(vals_list)  