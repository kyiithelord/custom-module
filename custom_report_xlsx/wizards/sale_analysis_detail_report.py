import xlsxwriter
from odoo import api, models, fields, _
from odoo.exceptions import UserError
from io import BytesIO


class SaleAnalysisDetailReport(models.TransientModel):
    _name = 'sale.analysis.detail.report'
    _description = 'Sale Analysis Detail Report'

    def _company_id_domain(self):
        return [('id', 'in', self.env.user.company_ids.ids)]

    company_id = fields.Many2one('res.company', 'Company', domain=_company_id_domain,
                                 default=lambda self: self.env.user.company_id.id)
    date_from = fields.Date(string="Date From")
    date_to = fields.Date(string="Date To")
    customer_ids = fields.Many2many('res.partner', string='Customer')
    category_ids = fields.Many2one(comodel_name="product.category", string="Category")
    product_ids = fields.Many2many(comodel_name="product.product",
                                   string="Products",
                                   domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")
    division_ids = fields.Many2many('res.country.state',string='Division')
    team_ids = fields.Many2many('crm.team',string='Team')
   

    @api.onchange('category_id')
    def _onchange_product(self):
        if self.category_id:
            product_tmpl_id = self.env['product.template'].search(
                [('categ_id', '=', self.category_id.id)])
            if product_tmpl_id:
                product_tmpl_id = tuple(product_tmpl_id.ids)
                return {'domain': {'product_ids': [('id', 'in', self.env["product.product"].
                                                    search([("product_tmpl_id", "in", product_tmpl_id)]).ids)]},
                        'value': {'product_ids': False}}

        if not self.category_id:
            self.update({
                'product_ids': False
            })
            return {'domain': {
                'product_ids': [('id', 'in', self.env["product.product"].search([("active", "=", True)]).ids)]}}

    def print_report(self):
        report_name = 'Sale Analysis Detail Report'
        records = self.get_data()
        return {
            'type': 'ir.actions.act_url',
            'url': '/download/excel?id=%s&model=%s&report_name=%s' % (self.id, self._name, report_name),
            'target': 'new',
        }

    def get_data(self):
        condition_str = " "
        # import pdb
        # pdb.set_trace()
        if self.company_id:
            condition_str += " and am.company_id = " + str(self.company_id.id)

        if self.date_from and self.date_to:
            condition_str += " and TO_CHAR(am.invoice_date, 'YYYY-MM-DD') between '" + str(
                self.date_from) + "' and '" + \
                             str(self.date_to) + "'"

        if self.customer_ids:
            vend_ids = tuple(self.customer_ids.ids)
            if len(vend_ids) == 1:
                condition_str += " and am.partner_id in ({})".format(vend_ids[0])
            else:
                condition_str += " and am.partner_id in {}".format(vend_ids)

        # if self.category_id:
        #     condition_str += " and aml.categ_id = " + str(self.category_id.id)

        if self.product_ids:
            pt_ids = tuple(self.product_ids.ids)
            if len(self.product_ids) == 1:
                condition_str += " and aml.product_id in ({})".format(pt_ids[0])
            else:
                condition_str += " and aml.product_id in {}".format(pt_ids)

        self.env.cr.execute("""
                select TO_CHAR (am.create_date, 'YYYY-MM-DD HH:MI:SS') as invoice_creation_date, 
                To_CHAR (am.invoice_date, 'YYYY-MM-DD') as invoice_date,
                am.name as invoice_number,
                am.invoice_origin as source_document,
                rp.name as customer_name,
                aml.name as invoice_item_name,
                rcs.name as division,
                pcate.complete_name as category_name,
                aml.price_unit as invoice_selling_price,
                aml.price_subtotal as invoice_total,
                aml.quantity as quantity,
                aml.discount as discount,
                aml.parent_state as invoice_state,
                rcm.name as company,
                crmt.name ->> 'en_US' as sale_team

                from account_move am
                inner join account_move_line aml on aml.move_id = am.id
                inner join res_partner rp on rp.id = am.partner_id
                -- inner join account_move_line aml on aml.product_id = porduct_product on product.id
                inner join product_product pp on pp.id = aml.product_id
                inner join product_template ptm on ptm.id = pp.product_tmpl_id
                inner join product_category pcate on pcate.id = ptm.categ_id
                inner join res_country_state rcs on rcs.country_id = rp.country_id
                inner join res_company rcm on rcm.id = am.company_id
                inner join crm_team crmt on crmt.id = am.team_id
                where am.state in ('posted') and am.move_type in('out_invoice') and aml.display_type in ('product')
                """ + condition_str + """ order by am.invoice_date """)
        records = self.env.cr.dictfetchall()
        if not records:
            raise UserError(_('There is no data.'))
        return records

    def get_xlsx(self, response):
        records = self.get_data()
        excel = BytesIO()
        workbook = xlsxwriter.Workbook(excel, {'in_memory': True})
        sheet = workbook.add_worksheet('Sheet1')

        title_style = workbook.add_format({
            'font_name': 'Arial', 'font_size': 11,
            'valign': 'vcenter', 'align': 'center', 'bold': True,
            'bg_color': '#d3d3d3',
        })

        header_style = workbook.add_format({
            'font_name': 'Arial', 'font_size': 10, 'bold': True,
            'valign': 'vcenter', 'align': 'center', 'border': 1,
        })

        header_style_gray = workbook.add_format({
            'font_name': 'Arial', 'font_size': 10, 'bold': True,
            'valign': 'vcenter', 'align': 'center', 'border': 1,
            'bg_color': '#d3d3d3',
        })

        serial_no_style = workbook.add_format({
            'font_name': 'Arial', 'font_size': 9,
            'valign': 'vcenter', 'align': 'center', 'border': 1,
        })

        label_cell_style = workbook.add_format({
            'font_name': 'Arial', 'font_size': 9,
            'valign': 'vcenter', 'align': 'left',
        })

        number_cell_style = workbook.add_format({
            'font_name': 'Arial', 'font_size': 9, 'right': 1,
            'valign': 'vcenter', 'align': 'right', 'num_format': '#,##0K'
        })

        footer_label_style = workbook.add_format({
            'font_name': 'Arial', 'font_size': 9, 'top': 1, 'bottom': 1,
            'valign': 'vcenter', 'align': 'left', 'bold': True,
        })

        footer_number_style = workbook.add_format({
            'font_name': 'Arial', 'font_size': 9, 'top': 1, 'bottom': 1, 'right': 1,
            'valign': 'vcenter', 'align': 'right', 'num_format': '#,##0K', 'bold': True,
        })

        y_offset = 0
        row_no = 0
        sheet.merge_range(y_offset, 0, y_offset, 14, 'Sale Analysis Detail Report', title_style)
        y_offset += 2
        sheet.write(y_offset, 0, _('From'), header_style_gray)
        sheet.write(y_offset, 1, self.date_from and str(self.date_from) or '', serial_no_style)
        y_offset += 1
        sheet.write(y_offset, 0, _('To'), header_style_gray)
        sheet.write(y_offset, 1, self.date_to and str(self.date_to) or '', serial_no_style)
        y_offset += 2
        # create header
        sheet.write(y_offset, 0, _('No'), header_style_gray)
        sheet.write(y_offset, 1, _('Invoice Creation Date'), header_style_gray)
        sheet.write(y_offset, 2, _('Invoice Date'), header_style_gray)
        sheet.write(y_offset, 3, _('Invoice Number'), header_style_gray)
        sheet.write(y_offset, 4, _('Invoice Origin'), header_style_gray)
        sheet.write(y_offset, 5, _('Customer Name'), header_style_gray)
        sheet.write(y_offset, 6, _('Division'), header_style_gray)
        sheet.write(y_offset, 7, _('Invoice Items Name'), header_style_gray)
        sheet.write(y_offset, 8, _('Selling Price'), header_style_gray)
        sheet.write(y_offset, 9, _('Invoice Total'), header_style_gray)
        sheet.write(y_offset, 10, _('Quantity'), header_style_gray)
        sheet.write(y_offset, 11, _('Discount'), header_style_gray)
        sheet.write(y_offset, 12, _('Invoice State'), header_style_gray)
        sheet.write(y_offset, 13, _('Company'), header_style_gray)
        sheet.write(y_offset, 14, _('Sale Team'), header_style_gray)
        number = 1

        for record in records:
            y_offset += 1
            sheet.write(y_offset,0,number,label_cell_style)
            # product = self.env['product.product'].browse(record['product_id'])
            sheet.write(y_offset, 1, record['invoice_creation_date'], serial_no_style)
            sheet.write(y_offset, 2, record['invoice_date'], serial_no_style)
            sheet.write(y_offset, 3, record['invoice_number'], serial_no_style)
            sheet.write(y_offset, 4, record['source_document'], serial_no_style)
            sheet.write(y_offset, 5, record['customer_name'], serial_no_style)
            sheet.write(y_offset, 6, record['division'], serial_no_style)
            sheet.write(y_offset, 7, record['category_name'], serial_no_style)
            sheet.write(y_offset, 8, record['invoice_selling_price'], serial_no_style)
            sheet.write(y_offset, 9, record['invoice_total'], serial_no_style)
            sheet.write(y_offset, 10, record['quantity'], serial_no_style)
            sheet.write(y_offset, 11, record['discount'], serial_no_style)
            sheet.write(y_offset, 12, record['invoice_state'], serial_no_style)
            sheet.write(y_offset, 13, record['company'], serial_no_style)
            sheet.write(y_offset, 14, record['sale_team'], serial_no_style)
            number +=1
        workbook.close()
        excel.seek(0)
        response.stream.write(excel.read())
        excel.close()