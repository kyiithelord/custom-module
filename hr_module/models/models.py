from odoo import models, fields, api

class EmployeePromotionDemotion(models.Model):
    _name = 'employee.promotion.demotion'
    _description = 'Employee Promotion and Demotion'

    employee_name = fields.Char(string='Employee Name', required=True)
    promotion_demotion = fields.Selection(
        [('promotion', 'Promotion'), ('demotion', 'Demotion')],
        string='Promotion/Demotion',
        required=True
    )
    date = fields.Date(string='Date')
    current_position = fields.Char(string='Current Position')
    current_department = fields.Char(string='Current Department')
    new_position = fields.Char(string='New Position')
    new_department = fields.Char(string='New Department')
    current_salary = fields.Float(string='Current Salary')
    increase_amount = fields.Float(string='Increase Amount')
    decrease_amount = fields.Float(string='Decrease Amount')
    new_salary = fields.Float(string='New Salary', compute="_compute_new_salary")


    
    @api.depends('current_salary', 'increase_amount', 'decrease_amount', 'promotion_demotion')
    def _compute_new_salary(self):
        for record in self:
            new_salary = record.current_salary
            if record.promotion_demotion == 'promotion' and record.increase_amount:
                new_salary += record.increase_amount
            elif record.promotion_demotion == 'demotion' and record.decrease_amount:
                new_salary -= record.decrease_amount
            record.new_salary = new_salary
