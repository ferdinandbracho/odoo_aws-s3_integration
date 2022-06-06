from odoo import models, fields, api
from . import s3_helpers
import base64
import hashlib
import botocore


class AttachmentExtender(models.Model):
    _inherit = "ir.attachment"

    document_type = fields.Char(store=False, invisible=True)

    def create(self, vals_list):
        record_tuple_set = set()

        # remove computed field depending of datas
        vals_list = [{
            key: value
            for key, value
            in vals.items()
            if key not in ('file_size', 'checksum', 'store_fname')
        } for vals in vals_list]

        for values in vals_list:
            values = self._check_contents(values)
            raw, datas = values.pop('raw', None), values.pop('datas', None)
            if raw or datas:
                if isinstance(raw, str):
                    # b64decode handles str input but raw needs explicit encoding
                    raw = raw.encode()
                values.update(self._get_datas_related_values(
                    raw or base64.b64decode(datas or b''),
                    values['mimetype'],
                    vals_list[0]['type']
                ))
            record_tuple = (values.get('res_model'), values.get('res_id'))
            record_tuple_set.add(record_tuple)

        # don't use possible contextual recordset for check, see commit for details
        Attachments = self.browse()
        for res_model, res_id in record_tuple_set:
            Attachments.check('create', values={
                              'res_model': res_model, 'res_id': res_id})
        return super(AttachmentExtender, self).create(vals_list)

    def _get_datas_related_values(self, data, mimetype, traxi_doc=None):
        values = {
            'file_size': len(data),
            'checksum': self._compute_checksum(data),
            'index_content': self._index(data, mimetype),
            'store_fname': False,
            'db_datas': data,
        }
        if data and self._storage() != 'db':
            values['store_fname'] = self._file_write(
                data, values['checksum'], traxi_doc)
            values['db_datas'] = False
        return values

    # Override file writer
    def _file_write(self, value, checksum, traxi_doc):
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

    # Override file reader
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
            file_exists = s3_helpers.file_exists(s3, s3_bucket.name, fname)

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
                read = s3_key.get()['Body'].read()
                read = base64.b64decode(s3_key.get()['Body'].read())
        # Todo: improve this error handler
        except:
            read = super(AttachmentExtender, self)._file_read(fname)
        return read

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
            file_exists = s3_helpers.file_exists(
                s3, s3_bucket.name, fname)

            if file_exists:
                s3_helpers.delete_file_s3(s3, s3_bucket.name, fname,)

            self._mark_for_gc(fname)
        # Todo: improve this error handler
        except:
            self._mark_for_gc(fname)
