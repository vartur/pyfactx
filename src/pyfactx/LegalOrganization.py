from typing import Optional, override
from lxml import etree as ET

from pydantic import Field

from .InvoiceProfile import InvoiceProfile
from .XMLBaseModel import XMLBaseModel
from .namespaces import NAMESPACES, RAM


class LegalOrganization(XMLBaseModel):
    id: Optional[str] = Field(default=None)
    trading_business_name: Optional[str] = Field(default=None)

    @override
    def to_xml(self, element_name: str, profile: InvoiceProfile) -> ET.Element:
        root = ET.Element(f"{{{NAMESPACES[RAM]}}}{element_name}")

        # ID
        if self.id:
            ET.SubElement(root, f"{{{NAMESPACES[RAM]}}}ID", attrib={"schemeID": "0002"}).text = self.id

        if profile >= InvoiceProfile.EN16931:
            # TradingBusinessName
            ET.SubElement(root, f"{{{NAMESPACES[RAM]}}}TradingBusinessName").text = self.trading_business_name

        return root
