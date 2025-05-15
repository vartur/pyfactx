from typing import Optional, override
from xml.etree.ElementTree import Element, SubElement

from pydantic import Field

from .InvoiceProfile import InvoiceProfile
from .XMLBaseModel import XMLBaseModel
from .namespaces import RAM


class LegalOrganization(XMLBaseModel):
    id: Optional[str] = Field(default=None)
    trading_business_name: Optional[str] = Field(default=None)

    @override
    def to_xml(self, element_name: str, profile: InvoiceProfile) -> Element:
        root = Element(f"{RAM}:{element_name}")

        # ID
        if self.id:
            SubElement(root, f"{RAM}:ID", attrib={"schemeID": "0002"}).text = self.id

        if profile >= InvoiceProfile.BASICWL:
            # TradingBusinessName
            SubElement(root, f"{RAM}:TradingBusinessName").text = self.trading_business_name

        return root
