from typing import Optional
from lxml import etree as ET

from pydantic import Field

from .InvoiceProfile import InvoiceProfile
from .XMLBaseModel import XMLBaseModel
from .namespaces import NAMESPACES, RAM


class TradeSettlementFinancialCard(XMLBaseModel):
    id: str = Field(...)
    cardholder_name: Optional[str] = Field(default=None)

    def to_xml(self, element_name: str, profile: InvoiceProfile) -> ET.Element:
        root = ET.Element(f"{{{NAMESPACES[RAM]}}}{element_name}")

        # ID
        ET.SubElement(root, f"{{{NAMESPACES[RAM]}}}ID").text = self.id

        # CardholderName
        if self.cardholder_name:
            ET.SubElement(root, f"{{{NAMESPACES[RAM]}}}CardholderName").text = self.cardholder_name

        return root
