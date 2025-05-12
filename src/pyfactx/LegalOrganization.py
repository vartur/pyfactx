from typing import Optional
from xml.etree.ElementTree import Element, SubElement

from pydantic import BaseModel, Field

from .InvoiceProfile import InvoiceProfile
from .namespaces import RAM


class LegalOrganization(BaseModel):
    id: Optional[str] = Field(default=None)
    trading_business_name: Optional[str] = Field(default=None)

    def to_xml(self, element_name: str, profile: InvoiceProfile = InvoiceProfile.MINIMUM) -> Element:
        root = Element(f"{RAM}:{element_name}")

        # ID
        if self.id:
            SubElement(root, f"{RAM}:ID", attrib={"schemeID": "0002"}).text = self.id

        if profile != InvoiceProfile.MINIMUM:
            # TradingBusinessName
            SubElement(root, f"{RAM}:TradingBusinessName").text = self.trading_business_name

        return root
