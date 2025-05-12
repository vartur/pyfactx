from typing import Optional

from pydantic import BaseModel, Field


class CreditorFinancialAccount(BaseModel):
    iban_id: Optional[str] = Field(default=None)
    proprietary_id: Optional[str] = Field(default=None)
