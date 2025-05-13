from typing import Optional
from xml.etree.ElementTree import Element, SubElement

from pydantic import BaseModel, Field

from .InvoiceProfile import InvoiceProfile
from .namespaces import RAM


class Note(BaseModel):
    content: str = Field(...)
    subject_code: Optional[str] = Field(default=None)  # https://service.unece.org/trade/untdid/d00a/tred/tred4451.htm

    def to_xml(self, element_name: str, _profile: InvoiceProfile) -> Element:
        root = Element(f"{RAM}:{element_name}")

        # Content
        SubElement(root, f"{RAM}:Content").text = self.content

        # SubjectCode
        if self.subject_code:
            SubElement(root, f"{RAM}:SubjectCode").text = self.subject_code

        return root
