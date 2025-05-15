from datetime import datetime
from typing import Optional, override
from lxml import etree as ET

from pydantic import Field

from .InvoiceProfile import InvoiceProfile
from .XMLBaseModel import XMLBaseModel
from .namespaces import NAMESPACES, RAM, UDT


class TradePaymentTerms(XMLBaseModel):
    description: Optional[str] = Field(default=None)
    due_date: Optional[datetime] = Field(default=None)
    direct_debit_mandate_id: Optional[str] = Field(default=None)

    @override
    def to_xml(self, element_name: str, _profile: InvoiceProfile) -> ET.Element:
        root = ET.Element(f"{{{NAMESPACES[RAM]}}}{element_name}")

        # Description
        if self.description:
            ET.SubElement(root, f"{{{NAMESPACES[RAM]}}}Description").text = self.description

        # DueDateDateTime
        if self.due_date:
            due_date_elem = ET.SubElement(root, f"{{{NAMESPACES[RAM]}}}DueDateDateTime")
            ET.SubElement(due_date_elem, f"{{{NAMESPACES[UDT]}}}DateTimeString",
                          attrib={"format": "102"}).text = self.due_date.strftime(
                "%Y%m%d")

        # DirectDebitMandateID
        if self.direct_debit_mandate_id:
            ET.SubElement(root, f"{{{NAMESPACES[RAM]}}}DirectDebitMandateID").text = self.direct_debit_mandate_id

        return root
