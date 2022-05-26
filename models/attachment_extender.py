from odoo import models, fields, api
from . import s3_helpers
import base64
import hashlib
import boto3

# Starting s3 connection
s3, s3_bucket = s3_helpers.s3_connector()


class AttachmentExtender(models.Model):
    _inherit = "ir.attachment"

    # Override file writer
    def _file_write(self, value, checksum):
        # Todo: add conditional logic to check if the current instance is flagged as s3 storage needed: in that case run the follow code, else run:
        # ! fname = super(S3Attachment, self)._file_write(value, checksum)
        bin_value = base64.b64encode(value)
        fname = hashlib.sha1(bin_value).hexdigest()
        s3.Object(s3_bucket.name, fname).put(Body=bin_value)
        return fname

    # Override file reader
    def _file_read(self, fname):
        # Checking the existence of the file in bucket
        file_exists = s3_helpers.file_exists(s3, s3_bucket.name, fname)

        # If not exist check the local file system
        if not file_exists:
            try:
                read = super(AttachmentExtender, self)._file_read(fname)
            except Exception:
                # file not found in the local file system either.
                return False

        # If file exist reading it
        else:
            s3_key = s3.Object(s3_bucket.name, fname)
            read = s3_key.get()['Body'].read()
            read = base64.b64decode(s3_key.get()['Body'].read())
        return read

    def _file_delete(self, fname):
        # Checking the existence of the file in bucket
        file_exists = s3_helpers.file_exists(s3, s3_helpers.S3_BUCKET, fname)

        if file_exists:
            s3_helpers.delete_file_s3(s3, s3_helpers.S3_BUCKET, fname,)

        self._mark_for_gc(fname)
