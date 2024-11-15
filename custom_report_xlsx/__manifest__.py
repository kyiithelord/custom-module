#-*- coding:utf-8 -*-

{
    'name': 'Custom Detail Report',

    'category': 'Reporting',

    'sequence': 39,

    'summary': 'Custom report',

    'description': "",

    'depends': ['base', 'stock', 'web', 'purchase','report_controller'],

    'data': [
        'security/ir.model.access.csv',
        'wizards/purchase_detail_report.xml',
        'wizards/purchase_order_report.xml',
        'wizards/sale_order_report.xml',
        'wizards/sale_analysis_detail_report.xml'

    ],

    'installable': True,

    'application': False,

}
