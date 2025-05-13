from xml.etree.ElementTree import Element, SubElement

from pydantic import BaseModel, Field

from .InvoiceProfile import InvoiceProfile
from .namespaces import RAM


class DebtorFinancialAccount(BaseModel):
    iban_id: str = Field(...)

    def to_xml(self, element_name: str, _profile: InvoiceProfile) -> Element:
        root = Element(f"{RAM}:{element_name}")

        # IBANID
        SubElement(root, f"{RAM}:IBANID").text = self.iban_id

        return root
