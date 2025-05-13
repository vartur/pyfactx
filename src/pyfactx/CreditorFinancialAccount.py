from typing import Optional
from xml.etree.ElementTree import Element, SubElement
from pydantic import Field
from typing_extensions import override

from .InvoiceProfile import InvoiceProfile
from .XMLBaseModel import XMLBaseModel
from .namespaces import RAM


class CreditorFinancialAccount(XMLBaseModel):
    iban_id: Optional[str] = Field(default=None)
    proprietary_id: Optional[str] = Field(default=None)

    @override
    def to_xml(self, element_name: str, _profile: InvoiceProfile) -> Element:
        root = Element(f"{RAM}:{element_name}")

        # IBANID
        if self.iban_id:
            SubElement(root, f"{RAM}:IBANID").text = self.iban_id

        # ProprietaryID
        if self.proprietary_id:
            SubElement(root, f"{RAM}:ProprietaryID").text = self.proprietary_id

        return root
