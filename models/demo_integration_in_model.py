# # -*- coding: utf-8 -*-
# # NOT INCLUDED IN MODELS.INIT (DEMO PORPOISE)
# from odoo import models, fields, api
# import base64


# class attachment_partner (models.Model):
#     _inherit = 'ir.attachment'
#     partner = fields.Many2one('res.company')
#     type = fields.Char(string='Tipo de documento')


# class fleet_partner(models.Model):
#     _inherit = 'res.company'
#     _description = """
#                     Inheritance of the model res_company which is
#                     the one that fits the best, according to the requirements
#                     It allows to Sign up the different enterprices that want to
#                     use the Traxi Business service"""

#     """
#     FIELDS REQUIRED BY TRAXI BUSINESS
#     Name - Already exist
#     Address - Already exist related in res_partner
#     Contact Email - Already exist related in res_company
#     Billing Email - MUST CREATE
#     Phone Number - Exists
#     Contact Person - Create and relate to res_partner
#     Website - Exists
#     #####################################################
#     DOCUMENTS REQUIRED BY TRAXI BUSINESS
#     Acta constitutiva
#     Cédula fiscal
#     Documentos de identidad
#     Opinión del SAT
#     Apoderado legal
#     Constancia de Situación Fiscal
#     """
#     # LOAD THE DEFAULT DOCUMENTS FOR COMPANIES
#     @api.model
#     def default_get(self, fields):
#         res = super(fleet_partner, self).default_get(fields)
#         document_lines = [(5, 0, 0)]
#         # GET DOCUMENTS FOR THIS MODEL
#         company_id = self.env['ir.model'].search(
#             [('model', '=', 'res.company')], limit=1)
#         company_id = company_id.id
#         files = self.env['docs_config'].sudo().search(
#             [('model', '=', company_id)])
#         for file in files:
#             line = (0, 0,
#                     {'type': file.name})
#             document_lines.append(line)
#         res.update({'documents': document_lines})
#         return res

#     billing_email = fields.Char(string="Billing email",
#                                 required=True)
#     contact = fields.Many2one('res.users',
#                               string="Contact Person")
#     documents = fields.One2many('ir.attachment',
#                                 'partner',
#                                 string="Gestión documental")


# class file_validation_and_management(models.Model):
#     _inherit = 'ir.attachment'

#     _description = """
#                     Inheritance of the model ir.attachment
#                     in order to check the validation of documents
#                     (it's life cycle) as well as uploading them to a
#                     s3 bucket
#     """

#     life_cycle = fields.Selection([("New", "New"), ("Validation", "Validation"),
#                                    ("Approved", "Approved"), ("Rejected",
#                                                               "Rejected"), ("Review", "Review"),
#                                    ("Active", "Active")], string="Validación del documento")

#     s3_url = fields.Binary(string="S3 bucket url",
#                            compute="_compute_s3_bucket")

#     def _compute_s3_bucket(self):
#         decoded = base64.b64decode(self.datas)
#         open('/tmp/archivo_dec.pdf', 'wb').write(decoded)
#         self.s3_url = self.datas


# class s3_bucket(models.Model):
#     _name = 's3_storage'
#     _description = """
#                     Model to store several api keys of
#                     an aws s3 bucket making one of them
#                     default
#     """
#     s3_api_key = fields.Char(string="S3 API key")
#     default_key = fields.Boolean(string="Default key")
