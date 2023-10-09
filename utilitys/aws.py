import boto3
from botocore.exceptions import ClientError
import logging


def upload_file_to_s3(file_path, bucket_name, key):
    # Upload the file
    s3_client = boto3.client("s3")
    try:
        response = s3_client.upload_file(file_path, bucket_name, key)
    except ClientError as e:
        logging.error(e)
        return False
    return True
