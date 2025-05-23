from typing import Optional
from lxml import etree as ET
from pydantic import Field
from typing_extensions import override

from .InvoiceProfile import InvoiceProfile
from .XMLBaseModel import XMLBaseModel
from .namespaces import NAMESPACES, RAM


class CreditorFinancialAccount(XMLBaseModel):
    iban_id: Optional[str] = Field(default=None)
    account_name: Optional[str] = Field(default=None)  # From EN16931
    proprietary_id: Optional[str] = Field(default=None)

    @override
    def to_xml(self, element_name: str, profile: InvoiceProfile) -> ET.Element:
        root = ET.Element(f"{{{NAMESPACES[RAM]}}}{element_name}")

        # IBANID
        if self.iban_id:
            ET.SubElement(root, f"{{{NAMESPACES[RAM]}}}IBANID").text = self.iban_id

        if profile >= InvoiceProfile.EN16931:
            # AccountName
            ET.SubElement(root, f"{{{NAMESPACES[RAM]}}}AccountName").text = self.account_name

        # ProprietaryID
        if self.proprietary_id:
            ET.SubElement(root, f"{{{NAMESPACES[RAM]}}}ProprietaryID").text = self.proprietary_id

        return root
