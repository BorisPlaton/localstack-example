from pydantic import BaseModel


class CreateCustomerInputContract(BaseModel):
    first_name: str
    last_name: str


class CustomerOutputContract(BaseModel):
    id: int
    first_name: str
    last_name: str
