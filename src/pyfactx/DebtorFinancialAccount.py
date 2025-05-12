from pydantic import BaseModel, Field


class DebtorFinancialAccount(BaseModel):
    iban_id: str = Field(...)
