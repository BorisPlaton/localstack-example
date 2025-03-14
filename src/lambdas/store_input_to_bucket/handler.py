import boto3
from aws_lambda_powertools.utilities.batch import (
    BatchProcessor,
    EventType,
    process_partial_response,
)
from aws_lambda_powertools.utilities.typing import LambdaContext

from contracts import StoreDocumentSQSRecordInputContract
from settings import S3Settings
from repository import DocumentS3Repository


processor = BatchProcessor(
    event_type=EventType.SQS,
    model=StoreDocumentSQSRecordInputContract,
)
s3_settings = S3Settings()
s3_client = boto3.client("s3")


def record_handler(record: StoreDocumentSQSRecordInputContract):
    repository = DocumentS3Repository(
        s3_settings=s3_settings,
        s3_client=s3_client,
    )

    repository.store_document(
        key=record.body.key,
        content=record.body.content,
    )


def lambda_handler(event, context: LambdaContext):
    return process_partial_response(
        event=event,
        record_handler=record_handler,
        processor=processor,
        context=context,
    )
