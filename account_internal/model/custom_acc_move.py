from odoo import models,fields,api,_
class Accountmove(models.Model):
    _inherit = 'account.move'
    def _get_payment_data(self):
        names = []

        invoice_payments = self.invoice_payments_widget
        if invoice_payments and isinstance(invoice_payments, dict):
            content = invoice_payments.get('content', [])
            for item in content:
                reconcile_amount = item.get('amount')
                reconcile_date = item.get('date')
                names.append({
                    'amount': reconcile_amount,
                    'date': reconcile_date
                })

        return names