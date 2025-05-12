from typing import Optional
from xml.etree.ElementTree import Element, SubElement
from pydantic import BaseModel, Field

from .InvoiceProfile import InvoiceProfile
from .namespaces import RAM


class CreditorFinancialAccount(BaseModel):
    iban_id: Optional[str] = Field(default=None)
    proprietary_id: Optional[str] = Field(default=None)

    def to_xml(self, element_name: str, profile: InvoiceProfile = InvoiceProfile.MINIMUM) -> Element:
        root = Element(f"{RAM}:{element_name}")

        # IBANID
        if self.iban_id:
            SubElement(root, f"{RAM}:IBANID").text = self.iban_id

        # ProprietaryID
        if self.proprietary_id:
            SubElement(root, f"{RAM}:ProprietaryID").text = self.proprietary_id

        return root
