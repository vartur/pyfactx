from datetime import datetime
from typing import Optional, override
from xml.etree.ElementTree import Element, SubElement

from pydantic import Field

from .InvoiceProfile import InvoiceProfile
from .InvoiceTypeCode import InvoiceTypeCode
from .Note import Note
from .XMLBaseModel import XMLBaseModel
from .namespaces import RAM, RSM, UDT


class ExchangedDocument(XMLBaseModel):
    id: str = Field(...)
    type_code: InvoiceTypeCode = Field(default=InvoiceTypeCode.COMMERCIAL_INVOICE)
    issue_date_time: datetime = Field(...)
    included_notes: Optional[list[Note]] = Field(default=None)

    @override
    def to_xml(self, element_name: str, profile: InvoiceProfile) -> Element:
        root = Element(f"{RSM}:{element_name}")

        # ID
        SubElement(root, f"{RAM}:ID").text = self.id

        # TypeCode
        SubElement(root, f"{RAM}:TypeCode").text = str(self.type_code.value)

        # IssueDateTime
        issue_dt_element = SubElement(root, f"{RAM}:IssueDateTime")
        SubElement(issue_dt_element, f"{UDT}:DateTimeString",
                   attrib={"format": "102"}).text = self.issue_date_time.strftime("%Y%m%d")

        # IncludedNotes
        if profile != InvoiceProfile.MINIMUM and self.included_notes:
            for note in self.included_notes:
                root.append(note.to_xml("IncludedNote", profile))

        return root
