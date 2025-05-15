from typing import Optional
from xml.etree.ElementTree import Element, SubElement
from pydantic import Field
from typing_extensions import override

from .InvoiceProfile import InvoiceProfile
from .XMLBaseModel import XMLBaseModel
from .namespaces import RAM


class CreditorFinancialAccount(XMLBaseModel):
    iban_id: Optional[str] = Field(default=None)
    account_name: Optional[str] = Field(default=None)  # From EN16931
    proprietary_id: Optional[str] = Field(default=None)

    @override
    def to_xml(self, element_name: str, profile: InvoiceProfile) -> Element:
        root = Element(f"{RAM}:{element_name}")

        # IBANID
        if self.iban_id:
            SubElement(root, f"{RAM}:IBANID").text = self.iban_id

        if profile >= InvoiceProfile.EN16931:
            # AccountName
            SubElement(root, f"f{RAM}:AccountName").text = self.account_name

        # ProprietaryID
        if self.proprietary_id:
            SubElement(root, f"{RAM}:ProprietaryID").text = self.proprietary_id

        return root
