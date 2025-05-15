from lxml import etree as ET
from pydantic import Field
from typing_extensions import override

from .InvoiceProfile import InvoiceProfile
from .XMLBaseModel import XMLBaseModel
from .namespaces import NAMESPACES, RAM


class DebtorFinancialAccount(XMLBaseModel):
    iban_id: str = Field(...)

    @override
    def to_xml(self, element_name: str, _profile: InvoiceProfile) -> ET.Element:
        root = ET.Element(f"{{{NAMESPACES[RAM]}}}{element_name}")

        # IBANID
        ET.SubElement(root, f"{{{NAMESPACES[RAM]}}}IBANID").text = self.iban_id

        return root
