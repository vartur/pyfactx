from datetime import datetime
from typing import Optional, override
from xml.etree.ElementTree import Element, SubElement

from pydantic import Field

from .InvoiceProfile import InvoiceProfile
from .XMLBaseModel import XMLBaseModel
from .namespaces import RAM, UDT


class TradePaymentTerms(XMLBaseModel):
    description: Optional[str] = Field(default=None)
    due_date: Optional[datetime] = Field(default=None)
    direct_debit_mandate_id: Optional[str] = Field(default=None)

    @override
    def to_xml(self, element_name: str, _profile: InvoiceProfile) -> Element:
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
