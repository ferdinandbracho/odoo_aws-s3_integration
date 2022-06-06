from odoo import models, fields


class ConfigExtender(models.TransientModel):
    _inherit = "res.config.settings"

    aws_access_key_id = fields.Char(
        string="AWS S3 Access Key ID",
        config_parameter="aws_access_key_id"
    )

    aws_secret_access_key = fields.Char(
        string="AWS S3 Secret Access Key",
        config_parameter="aws_secret_access_key"
    )

    aws_s3_bucket_name = fields.Char(
        string="AWS S3 Bucket Name",
        config_parameter="aws_s3_bucket_name"
    )
