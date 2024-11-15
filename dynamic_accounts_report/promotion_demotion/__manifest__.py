{
  'name':"Custom Employee Module",
  'author': "Bluga",

  'website': "https://www.youtube.com/shorts/XMDIhx8i_5w",
  'summary' : "odoo 16 development",

  'category': "Promotion/Demotion ",
  "description": """
    Employee Management System
      -Manage Promotions and Demotions of the employees
""",
  'depends':['mail'],

  "data":[
    'security/ir.model.access.csv',
    'data/cron.xml',
    'view/promotion_demotion.xml',
    'view/menu.xml',

  ]
}