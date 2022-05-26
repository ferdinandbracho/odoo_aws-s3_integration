import boto3
import botocore

S3_BUCKET = "traxi-fleet-test"


def s3_connector():
    session = boto3.Session(
        aws_access_key_id="AKIA4ELBCROWJTI7ZO7U",
        aws_secret_access_key="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",
    )

    s3 = session.resource('s3')

    s3_bucket = s3.Bucket(S3_BUCKET)

    return (s3, s3_bucket)


def file_exists(s3, bucket_name, key):
    exists = True
    try:
        s3.meta.client.head_object(Bucket=bucket_name, Key=key)
    except botocore.exceptions.ClientError as e:
        error_code = int(e.response['Error']['Code'])
        if error_code == 404:
            exists = False
    return exists


def delete_file_s3(s3, bucket_name, key,):
    file = s3.Object(bucket_name=bucket_name, key=key)
    file.delete()
