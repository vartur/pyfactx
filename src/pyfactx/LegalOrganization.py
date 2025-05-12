from typing import Optional

from pydantic import BaseModel, Field

from .InvoiceProfile import InvoiceProfile


class LegalOrganization(BaseModel):
    id: Optional[str] = Field(default=None)
    trading_business_name: Optional[str] = Field(default=None)

    def to_xml(self, profile: InvoiceProfile = InvoiceProfile.MINIMUM):
        xml_string = ""
        if self.id is not None:
            xml_string += f"<ram:ID schemeID=\"0002\">{self.id}</ram:ID>"

        if profile != InvoiceProfile.MINIMUM:

            if self.trading_business_name is not None:
                xml_string += f"<ram:TradingBusinessName>{self.trading_business_name}</ram:TradingBusinessName>"
