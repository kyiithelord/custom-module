# -*- coding: utf-8 -*-
# from odoo import http


# class HrModule(http.Controller):
#     @http.route('/hr_module/hr_module', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hr_module/hr_module/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('hr_module.listing', {
#             'root': '/hr_module/hr_module',
#             'objects': http.request.env['hr_module.hr_module'].search([]),
#         })

#     @http.route('/hr_module/hr_module/objects/<model("hr_module.hr_module"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hr_module.object', {
#             'object': obj
#         })
