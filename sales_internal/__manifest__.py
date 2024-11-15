{
  'name':"Sale Internal",
  'author': "Pyae Sone Hein",

  'website': "https://www.youtube.com/shorts/XMDIhx8i_5w",
  'summary' : "odoo 16 development",

  'category': "Sale Order Management ",
  'depends':['sale','product'],

  "data":[
    'data/sequence.xml',
    'views/internal_ref.xml',
    'views/custom_sale_order_line.xml',
    'views/sale_delivery_note.xml',
  ]
}