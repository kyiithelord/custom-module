from odoo import fields,api,models,_
from datetime import datetime



class PromotionDemotion(models.Model):
    _name = "promotion.demotion"
    _inherit = 'mail.thread'

    employee_id = fields.Many2one('hr.employee',string="Employee Id")
    action_type = fields.Selection([('none','None'),('promotion','Promotion'),(
        'demotion','Demotion'
    )],default="none")
    start_date = fields.Date(string='Start Date')
    current_department = fields.Char(string='Current Department',readonly=True,store=True)
    new_department = fields.Many2one('hr.department',string='New Department')
    current_salary = fields.Integer(string='Current Salary')
    increase_salary_amount = fields.Integer(string='Increase Amount')
    decrease_salary_amount = fields.Integer(string='Decrease Amount')
    current_job_position = fields.Char(string='Job Position')
    new_job_position = fields.Many2one('hr.job',string='New Jobs Position')
    state = fields.Boolean(default=False)


    def salary_calculate(self):
        current_form = self.env['promotion.demotion'].search([('start_date','=',datetime.today())])
        for rec in current_form:
            new_salary = 0
            if rec.action_type == 'promotion':
                new_salary = rec.current_salary + rec.increase_salary_amount
            elif rec.action_type == 'demotion':
                new_salary = rec.current_salary - rec.decrease_salary_amount

            employee_contract = self.env['hr.contract'].search([('employee_id','=',rec.employee_id.id)])
            
            if employee_contract:
                employee_contract.wage = new_salary
                rec.current_salary = new_salary
            rec.state = True

        print('===============>',current_form)

    @api.onchange('employee_id')
    def update_employee(self):
        current_salary = self.env['hr.contract'].search([('employee_id','=',self.employee_id.id)]).wage
        self.current_salary = current_salary
        self.current_department = self.employee_id.department_id.name
        self.current_job_position = self.employee_id.job_id.name

    