# -*- coding: utf-8 -*-

from odoo import models,fields, api
# from ../controllers/BSAImportController import ImportController

# class ImportTemplate(models.Model):

#ADDED IMPORTS BY JUSTIN
# -*- coding: utf-8 -*-


import json

from odoo import http
from odoo.http import request
from odoo.tools import misc

#     @api.model
#     def get_import_templates(self):
#         res = super(ImportTemplate, self).get_import_templates()
#         if self.env.context.get('sale_multi_pricelist_product_template'):
#             if self.user_has_groups('product.group_sale_pricelist'):

#                 return [{
#                     'label': _('Import Template for Products'),
#                     'template': '/product/static/xls/product_template.xls'
#                 }]
#         return 

class bsa_import_wizard(models.TransientModel):
    _inherit = 'base_import.import'

    _name = "bsa.import.wizard"
    _description="Module for BSA data import and cleaning"
    parent_list = fields.Char(string="Parent List",required=True)
    child_list = fields.Char(string="Child List",required=True)
    

    def custom_parse(self):
        self.parse_preview()
        print(":................................................")
    def custom_upload(self):
        print("At custom upload")
    # unmatched_lines = fields.Text(string="Unmatched lines")
    # # creating filed that will keep track of all not readonly fieldslevel = fields.Selection(string = "Level", 

    # potential_fields =self.env['ir.model.fields'].search([('readonly', '=', False),('model', '=', 'product.template')])
    # # print(potential_fields)

    # not_readonly_fields = fields.Selection(string = "potention import fields", selection = [] ) 
    # _compute_selections(self):

#  getting the importable trees based on the model
    #@api.model
    # def get_fields_tree(self, model, depth=FIELDS_RECURSION_LIMIT):

    # @api.multi
    # def method_a(self):
    #      self.env['purchase.order'].method_b()

    # POST /web/dataset/call_kw/bsa.import.wizard/read HTTP/1.1


# {"id":201,"jsonrpc":"2.0","method":"call","params":{"args":[{"res_model":"product.template"}],"model":"base_import.import","method":"create","kwargs":{"context":{"lang":"en_US","tz":"America/New_York","uid":2,"allowed_company_ids":[1]}}}}