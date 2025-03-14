from aws_lambda_powertools.utilities.parser.models import SqsRecordModel
from aws_lambda_powertools.utilities.parser.types import Json
from pydantic import BaseModel


class DocumentContent(BaseModel):
    key: str
    content: str


class StoreDocumentSQSRecordInputContract(SqsRecordModel):
    body: Json[DocumentContent]
