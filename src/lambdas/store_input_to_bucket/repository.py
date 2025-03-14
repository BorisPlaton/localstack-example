from settings import S3Settings


class DocumentS3Repository:

    def __init__(
        self,
        s3_settings: S3Settings,
        s3_client,
    ) -> None:
        self._s3_settings = s3_settings
        self._s3_client = s3_client

    def store_document(
        self,
        content: str,
        key: str,
    ) -> None:
        self._s3_client.put_object(
            Bucket=self._s3_settings.DOCUMENTS_BUCKET,
            Key=key,
            Body=content.encode(),
        )
