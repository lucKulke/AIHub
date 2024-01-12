from botocore.config import Config
import os
import aioboto3

import typing

region = os.getenv("AWS_BUCKET_REGION")
my_config = Config(
    region_name=region,
    signature_version="v4",
    retries={"max_attempts": 10, "mode": "standard"},
)

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
