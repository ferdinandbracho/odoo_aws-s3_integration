from odoo import models, fields, api


class Docs_Config(models.Model):
    _name = 'docs_config'
    _description = 'docs_config'

    # NAME THE DOCUMENT TYPE
    name = fields.Char(string="Document type")
    # CHOOSE TO WHICH MODEL TO ATTACH THE NEW TYPE OF DOCUMENT
    model = fields.Many2one('ir.model',
                            string="Model")
    # IS THIS DOCUMENT REQUIRED BY BLACKTRUST?
    req_blacktrust = fields.Boolean(string="Required by Blacktrust")
    # SHOULD WE PUSH THIS TYPE OF DOCUMENT TO AN S3 BUCKET?
    s3_bucket = fields.Boolean(string="Push to bucket")


class file_validation_and_management(models.Model):
    _inherit = 'ir.attachment'

    _description = """
                    Inheritance of the model ir.attachment
                    in order to check the validation of documents 
                    (it's life cycle)
    """

    life_cycle = fields.Selection([("New", "New"), ("Validation", "Validation"),
                                   ("Approved", "Approved"), ("Rejected",
                                                              "Rejected"), ("Review", "Review"),
                                   ("Active", "Active")], string="Validación del documento")
