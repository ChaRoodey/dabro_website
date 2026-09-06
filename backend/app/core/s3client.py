import os
from typing import AsyncGenerator
from aiobotocore.session import get_session, AioSession

from app.core.config import settings

os.environ["AWS_REQUEST_CHECKSUM_CALCULATION"] = "when_required"
os.environ["AWS_RESPONSE_CHECKSUM_VALIDATION"] = "when_required"


class S3Client:
    def __init__(
            self,
            access_key: str,
            secret_key: str,
            endpoint_url: str,
            bucket_name: str,
            region_name: str,
            verify: str,
    ):
        self.config = {
            "aws_access_key_id": access_key,
            "aws_secret_access_key": secret_key,
            "endpoint_url": endpoint_url,
            "region_name": region_name,
            "verify": verify,
        }
        self.bucket_name = bucket_name
        self.session = get_session()

    async def get_client(self) -> AsyncGenerator[AioSession, None]:
        async with self.session.create_client("s3", **self.config) as client:
            yield client

    async def upload_file(self, client, file: bytes, object_name: str):
        await client.put_object(
            Bucket=self.bucket_name,
            Key=object_name,
            Body=file,
        )


s3_client = S3Client(
    access_key=settings.S3_ACCESS_KEY,
    secret_key=settings.S3_SECRET_KEY,
    endpoint_url=settings.S3_ENDPOINT_URL,
    bucket_name=settings.S3_BUCKET_NAME,
    region_name=settings.S3_REGION_NAME,
    verify=settings.S3_VERIFY,
)
