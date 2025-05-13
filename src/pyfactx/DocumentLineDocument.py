from typing import Optional, override
from xml.etree.ElementTree import Element, SubElement

from pydantic import Field

from .InvoiceProfile import InvoiceProfile
from .Note import Note
from .XMLBaseModel import XMLBaseModel
from .namespaces import RAM


class DocumentLineDocument(XMLBaseModel):
    line_id: int = Field(...)
    included_note: Optional[Note] = Field(default=None)

    @override
    def to_xml(self, element_name: str, profile: InvoiceProfile) -> Element:
        root = Element(f"{RAM}:{element_name}")

        # LineID
        SubElement(root, f"{RAM}:LineID").text = str(self.line_id)

        # IncludedNote
        if self.included_note:
            root.append(self.included_note.to_xml("IncludedNote", profile))

        return root
