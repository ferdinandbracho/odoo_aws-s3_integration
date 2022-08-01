from odoo import models, fields, api
from . import s3_helpers
import base64
import hashlib
import botocore


class AttachmentExtender(models.Model):
    _inherit = "ir.attachment"
    category = fields.Char(string="Categoría del documento")

    @api.model
    def odoo_assets(self):
        #attachments = self.env["ir.attachment"].search([])
        #print("---------------------------------------", flush=True)
        #print(attachments, flush=True)
        #print("---------------------------------------", flush=True)
        #for attachment in attachments:
        #    attachment.category = "Odoo asset"
        #ALL THE INITIAL ATTACHMENTS MUST BE ODOO ASSET
        #query = "UPDATE ir_attachment SET category='Odoo asset'"
        #self._cr.execute(query)

        return True

    @api.model_create_multi
    def create(self, vals_list):
        
        #CHECK IF THE AWS VALIES EXISTS, ELSE SKIP
        if len(self.env["res.config.settings"].search([]))==0:
            return super(AttachmentExtender, self).create(vals_list)


        print("---------------------------------------", flush=True)
        print("CREATE RUNS FIRST", flush=True)
        print(vals_list, flush=True)
        print("---------------------------------------", flush=True)
        
        #THE ASSETS OF ODOO DOESNT CREATE AT INSTALLING, THEY CREATE AT OPEN OF PROJECT
        odoo_assets = ["web.assets_common.min.css", "web.assets_frontend.min.css", 
                "web.assets_common_minimal.min.js", "web.assets_frontend_minimal.min.js",
                "web.assets_common_lazy.min.js", "web.assets_frontend_lazy.min.js"
                "web.assets_backend.min.css", "web.assets_common.min.js",
                "web.assets_backend.min.js", "web.assets_backend_prod_only.min.js",
                "web.assets_common.css", "web.assets_common.css.map", 
                "web.assets_backend.css", "web.assets_backend.css.map",
                "web.assets_common.js", "web.assets_common.js.map",
                "web.assets_backend.js", "web.assets_backend.js.map",
                "web.assets_backend_prod_only.js","web.assets_backend_prod_only.js.map",
                "res.company.scss"]

        record_tuple_set = set()
        #IF IT'S CREATING AN ASSET, PASS THE METHOD
        if vals_list[0]["name"] in odoo_assets:
            print("THIS IS A MF ASSET", flush=True)
            print(vals_list[0].keys(), flush=True)
            return super(AttachmentExtender, self).create(vals_list)

        # remove computed field depending of datas
        vals_list = [{
            key: value
            for key, value
            in vals.items()
            if key not in ('file_size', 'checksum', 'store_fname')
        } for vals in vals_list]

        for values in vals_list:
            values = self._check_contents(values)
            document_type = values['type']
            raw, datas, = values.pop('raw', None), values.pop(
                'datas', None)
            if document_type == "Odoo asset":
                continue
            if raw or datas:
                if isinstance(raw, str):
                    # b64decode handles str input but raw needs explicit encoding
                    raw = raw.encode()
                values.update(self._get_datas_related_values(
                    raw or base64.b64decode(datas or b''),
                    values['mimetype'],
                    trx_doc=document_type
                ))

            # 'check()' only uses res_model and res_id from values, and make an exists.
            # We can group the values by model, res_id to make only one query when
            # creating multiple attachments on a single record.
            record_tuple = (values.get('res_model'), values.get('res_id'))
            record_tuple_set.add(record_tuple)

        # don't use possible contextual recordset for check, see commit for details
        Attachments = self.browse()
        for res_model, res_id in record_tuple_set:
            Attachments.check('create', values={
                              'res_model': res_model, 'res_id': res_id})
        return super(AttachmentExtender, self).create(vals_list)

    def _get_datas_related_values(self, data, mimetype, trx_doc=None):
        values = {
            'file_size': len(data),
            'checksum': self._compute_checksum(data),
            'index_content': self._index(data, mimetype),
            'store_fname': False,
            'db_datas': data,
        }
        if data and self._storage() != 'db':
            values['store_fname'] = self._file_write(
                data, values['checksum'], trx_doc)
            values['db_datas'] = False
        return values

        # rewrite file writer
    def _file_write(self, value, checksum, traxi_doc=None):
        # search for current document
        document = self.env['docs_config'].sudo().search(
            [('name', '=', traxi_doc)])

        # Validate if s3 storage is needed
        if document.s3_bucket:
            # Starting s3 connection
            try:
                s3, s3_bucket = s3_helpers.s3_connector(
                    ACCESS_KEY=self.env["ir.config_parameter"].get_param(
                        "aws_access_key_id"),
                    SECRET_KEY=self.env["ir.config_parameter"].get_param(
                        "aws_secret_access_key"),
                    S3_BUCKET=self.env["ir.config_parameter"].get_param(
                        "aws_s3_bucket_name")
                )

                bin_value = base64.b64encode(value)
                fname = hashlib.sha1(bin_value).hexdigest()
                s3.Object(s3_bucket.name, fname).put(Body=bin_value)

                fname = super(AttachmentExtender, self)._file_write(
                    value, checksum)

            # Todo: improve this error handler
            except:
                fname = super(AttachmentExtender, self)._file_write(
                    value, checksum)
        else:
            fname = super(AttachmentExtender, self)._file_write(
                value, checksum)
        return fname

    # rewrite file reader
    def _file_read(self, fname):

        # Starting s3 connection
        try:
            s3, s3_bucket = s3_helpers.s3_connector(
                ACCESS_KEY=self.env["ir.config_parameter"].get_param(
                    "aws_access_key_id"),
                SECRET_KEY=self.env["ir.config_parameter"].get_param(
                    "aws_secret_access_key"),
                S3_BUCKET=self.env["ir.config_parameter"].get_param(
                    "aws_s3_bucket_name"))

            # Checking the existence of the file in bucket
            file_exists, error = s3_helpers.file_exists(
                s3, s3_bucket.name, fname)

            # If not exist check the local file system
            if not file_exists:
                try:
                    read = super(AttachmentExtender, self)._file_read(fname)
                # Todo: improve this error handler
                except Exception:
                    # file not found in the local file system either.
                    return False

            # If file exist reading it
            else:
                s3_key = s3.Object(s3_bucket.name, fname)
                # read = s3_key.get()['Body'].read()
                read = base64.b64decode(s3_key.get()['Body'].read())
        # Todo: improve this error handler
        except:
            read = super(AttachmentExtender, self)._file_read(fname)
        return read

    # rewrite file delete
    def _file_delete(self, fname):
        # Starting s3 connection
        try:
            s3, s3_bucket = s3_helpers.s3_connector(
                ACCESS_KEY=self.env["ir.config_parameter"].get_param(
                    "aws_access_key_id"),
                SECRET_KEY=self.env["ir.config_parameter"].get_param(
                    "aws_secret_access_key"),
                S3_BUCKET=self.env["ir.config_parameter"].get_param(
                    "aws_s3_bucket_name"))

            # Checking the existence of the file in bucket
            file_exists, error = s3_helpers.file_exists(
                s3, s3_bucket.name, fname)

            # If not exist delete in  the local file system
            if file_exists:
                s3_helpers.delete_file_s3(s3, s3_bucket.name, fname,)

            # If file exist reading it
            else:
                print('Error when try to connect to aws s3 bucket :', error)
                super(AttachmentExtender, self)._file_delete(fname)

        # Todo: improve this error handler
        except:
            super(AttachmentExtender, self)._file_delete(fname)
