from lxml import etree as ET

from pydantic import Field

from .InvoiceProfile import InvoiceProfile
from .XMLBaseModel import XMLBaseModel
from .namespaces import NAMESPACES, RAM


class CreditorFinancialInstitution(XMLBaseModel):
    bic_id: str = Field(...)

    def to_xml(self, element_name: str, profile: InvoiceProfile) -> ET.Element:
        root = ET.Element(f"{{{NAMESPACES[RAM]}}}{element_name}")

        # BICID
        ET.SubElement(root, f"{{{NAMESPACES[RAM]}}}BICID").text = self.bic_id

        return root
