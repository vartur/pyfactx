from typing import Optional
from xml.etree.ElementTree import Element, SubElement

from pydantic import Field

from .InvoiceProfile import InvoiceProfile
from .XMLBaseModel import XMLBaseModel
from .namespaces import RAM


class TradeSettlementFinancialCard(XMLBaseModel):
    id: str = Field(...)
    cardholder_name: Optional[str] = Field(default=None)

    def to_xml(self, element_name: str, profile: InvoiceProfile) -> Element:
        root = Element(f"{RAM}:{element_name}")

        # ID
        SubElement(root, f"{RAM}:ID").text = self.id

        # CardholderName
        if self.cardholder_name:
            SubElement(root, f"{RAM}:CardholderName").text = self.cardholder_name

        return root
