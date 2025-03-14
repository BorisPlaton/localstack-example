import boto3
from aws_lambda_powertools import Logger
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.utilities.typing import LambdaContext

from contracts import CreateCustomerInputContract, CustomerOutputContract
from repository.customer import CustomerSQLRepository
from repository.document import DocumentS3Repository
from settings import DatabaseSettings, S3Settings


app = APIGatewayRestResolver()
database_settings = DatabaseSettings()
s3_settings = S3Settings()
s3_client = boto3.client("s3")
logger = Logger()


@app.post('/customer/')
def create_customer():
    repository = CustomerSQLRepository(
        database_settings=database_settings,
    )

    customer_data = CreateCustomerInputContract.model_validate_json(app.current_event.body)

    repository.save(
        first_name=customer_data.first_name,
        last_name=customer_data.last_name,
    )


@app.get('/customer/')
def list_customers():
    repository = CustomerSQLRepository(
        database_settings=database_settings,
    )

    customers = repository.get_all()

    return [
        CustomerOutputContract.model_validate(
            obj=customer,
            from_attributes=True,
        ).model_dump(
            mode='json',
        )
        for customer in customers
    ]


@app.get('/customer/<id_>/')
def get_customer(id_: int):
    repository = CustomerSQLRepository(
        database_settings=database_settings,
    )

    customer = repository.get_by_id(id_=id_)

    return CustomerOutputContract.model_validate(
        obj=customer,
        from_attributes=True,
    ).model_dump(
        mode='json',
    ) if customer else None


@app.get('/document/')
def list_all_documents():
    repository = DocumentS3Repository(
        s3_settings=s3_settings,
        s3_client=s3_client,
    )

    documents_keys = repository.list_documents_keys()

    return documents_keys


@app.get('/document/<key>/')
def get_document_by_key(key: str):
    repository = DocumentS3Repository(
        s3_settings=s3_settings,
        s3_client=s3_client,
    )

    document_content = repository.get_document_content(
        key=key,
    )

    return document_content


@logger.inject_lambda_context
def lambda_handler(
    event: dict,
    context: LambdaContext,
) -> dict:
    return app.resolve(event, context)
