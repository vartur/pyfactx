from datetime import datetime
from typing import Optional, override
from lxml import etree as ET

from pydantic import Field

from .InvoiceProfile import InvoiceProfile
from .InvoiceTypeCode import InvoiceTypeCode
from .Note import Note
from .XMLBaseModel import XMLBaseModel
from .namespaces import NAMESPACES, RAM, RSM, UDT


class ExchangedDocument(XMLBaseModel):
    id: str = Field(...)
    type_code: InvoiceTypeCode = Field(default=InvoiceTypeCode.COMMERCIAL_INVOICE)
    issue_date_time: datetime = Field(...)
    included_notes: Optional[list[Note]] = Field(default=None)

    @override
    def to_xml(self, element_name: str, profile: InvoiceProfile) -> ET.Element:
        root = ET.Element(f"{{{NAMESPACES[RSM]}}}{element_name}")

        # ID
        ET.SubElement(root, f"{{{NAMESPACES[RAM]}}}ID").text = self.id

        # TypeCode
        ET.SubElement(root, f"{{{NAMESPACES[RAM]}}}TypeCode").text = str(self.type_code.value)

        # IssueDateTime
        issue_dt_element = ET.SubElement(root, f"{{{NAMESPACES[RAM]}}}IssueDateTime")
        ET.SubElement(issue_dt_element, f"{{{NAMESPACES[UDT]}}}DateTimeString",
                      attrib={"format": "102"}).text = self.issue_date_time.strftime("%Y%m%d")

        # IncludedNotes
        if profile >= InvoiceProfile.BASICWL:
            if self.included_notes:
                for note in self.included_notes:
                    root.append(note.to_xml("IncludedNote", profile))

        return root
