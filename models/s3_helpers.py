import boto3
import botocore


def s3_connector(ACCESS_KEY, SECRET_KEY, S3_BUCKET):
    # try:
    session = boto3.Session(
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
    )
    s3 = session.resource('s3')
    s3_bucket = s3.Bucket(S3_BUCKET)
    return (s3, s3_bucket)


def file_exists(s3, bucket_name, key):
    exists = False
    try:
        s3.meta.client.head_object(Bucket=bucket_name, Key=key)
        exists = True
        return exists
    except botocore.exceptions.ClientError as e:
        error_code = int(e.response['Error']['Code'])
        return exists, error_code


def delete_file_s3(s3, bucket_name, key,):
    file = s3.Object(bucket_name=bucket_name, key=key)
    file.delete()
