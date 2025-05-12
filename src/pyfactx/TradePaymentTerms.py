from datetime import datetime
from typing import Optional
from xml.etree.ElementTree import Element, SubElement

from pydantic import BaseModel, Field

from .InvoiceProfile import InvoiceProfile
from .namespaces import RAM, UDT


class TradePaymentTerms(BaseModel):
    description: Optional[str] = Field(default=None)
    due_date: Optional[datetime] = Field(default=None)
    direct_debit_mandate_id: Optional[str] = Field(default=None)

    def to_xml(self, element_name: str, profile: InvoiceProfile = InvoiceProfile.MINIMUM) -> Element:
        root = Element(f"{RAM}:{element_name}")

        # Description
        if self.description:
            SubElement(root, f"{RAM}:Description").text = self.description

        # DueDateDateTime
        if self.due_date:
            due_date_elem = SubElement(root, f"{RAM}:DueDateDateTime")
            SubElement(due_date_elem, f"{UDT}:DateTimeString", attrib={"format": "102"}).text = self.due_date.strftime(
                "%Y%m%d")

        # DirectDebitMandateID
        if self.direct_debit_mandate_id:
            SubElement(root, f"{RAM}:DirectDebitMandateID").text = self.direct_debit_mandate_id

        return root
