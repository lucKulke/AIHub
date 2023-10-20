import boto3
from botocore.exceptions import ClientError
import logging
from botocore.config import Config

my_config = Config(
    region_name="eu-north-1",
    signature_version="v4",
    retries={"max_attempts": 10, "mode": "standard"},
)
s3_client = boto3.client("s3", config=my_config)


def upload_file_to_s3(file_path, bucket_name, key):
    try:
        response = s3_client.upload_file(
            file_path,
            bucket_name,
            key,
            ExtraArgs={
                "ContentType": "audio/wav",
                "Metadata": {"ContentType": "audio/wav"},
            },
        )
    except ClientError as e:
        logging.error(e)
        return False
    return True


def create_presigned_url_expanded(
    client_method_name, method_parameters=None, expiration=3600, http_method=None
):
    try:
        response = s3_client.generate_presigned_url(
            ClientMethod=client_method_name,
            Params=method_parameters,
            ExpiresIn=expiration,
            HttpMethod=http_method,
        )
    except ClientError as e:
        logging.error(e)
        return None

    return response
