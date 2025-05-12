from typing import Optional

from pydantic import BaseModel, Field

from .TaxCategoryCode import TaxCategoryCode
from .TaxTypeCode import TaxTypeCode
from .VATExemptionReasonCode import VATExemptionReasonCode


class TradeTax(BaseModel):
    calculated_amount: Optional[float] = Field(default=None)
    type_code: TaxTypeCode = Field(...)
    exemption_reason: Optional[str] = Field(default=None)
    basis_amount: Optional[float] = Field(default=None)
    category_code: TaxCategoryCode = Field(...)
    exemption_reason_code: Optional[VATExemptionReasonCode] = Field(default=None)
    due_date_type_code: Optional[str] = Field(default=None)
    rate_applicable_percent: Optional[float] = Field(default=None)