import boto3
from botocore.exceptions import ClientError
import logging
from botocore.config import Config
import os
import aioboto3
from datetime import datetime
import typing

region = os.getenv("AWS_BUCKET_REGION")
my_config = Config(
    region_name=region,
    signature_version="v4",
    retries={"max_attempts": 10, "mode": "standard"},
)
s3_client = boto3.client("s3", config=my_config)
aioboto3_session = aioboto3.Session()


async def upload_file_content_directly_to_s3(
    file: typing.BinaryIO, bucket: str, key: str, file_content_type: str
):
    async with aioboto3_session.client("s3", config=my_config) as s3:
        try:
            await s3.upload_fileobj(
                file, bucket, key, ExtraArgs={"ContentType": file_content_type}
            )
        except Exception as e:
            print(f"Unable to s3 upload to {key}: {e} ({type(e)})", flush=True)
            return str(e)

    return "successfully stored in s3"


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
