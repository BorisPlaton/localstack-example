from typing import NamedTuple

from botocore.exceptions import ClientError

from settings import S3Settings


class Document(NamedTuple):
    key: str
    content: str


class DocumentS3Repository:

    def __init__(
        self,
        s3_settings: S3Settings,
        s3_client,
    ) -> None:
        self._s3_settings = s3_settings
        self._s3_client = s3_client

    def list_documents_keys(self) -> list[str]:
        bucket_data = self._s3_client.list_objects_v2(
            Bucket=self._s3_settings.DOCUMENTS_BUCKET,
        )

        return [document['Key'] for document in bucket_data["Contents"]] if "Contents" in bucket_data else []

    def get_document_content(
        self,
        key: str,
    ) -> str | None:
        try:
            document = self._s3_client.get_object(
                Bucket=self._s3_settings.DOCUMENTS_BUCKET,
                Key=key,
            )
        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchKey':
                return
            raise e

        document_content = document["Body"].read().decode()

        return document_content
