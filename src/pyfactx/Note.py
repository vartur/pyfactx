from typing import Optional
from lxml import etree as ET

from pydantic import Field
from typing_extensions import override

from .InvoiceProfile import InvoiceProfile
from .XMLBaseModel import XMLBaseModel
from .namespaces import NAMESPACES, RAM


class Note(XMLBaseModel):
    content: str = Field(...)
    subject_code: Optional[str] = Field(default=None)  # https://service.unece.org/trade/untdid/d00a/tred/tred4451.htm

    @override
    def to_xml(self, element_name: str, _profile: InvoiceProfile) -> ET.Element:
        root = ET.Element(f"{{{NAMESPACES[RAM]}}}{element_name}")

        # Content
        ET.SubElement(root, f"{{{NAMESPACES[RAM]}}}Content").text = self.content

        # SubjectCode
        if self.subject_code:
            ET.SubElement(root, f"{{{NAMESPACES[RAM]}}}SubjectCode").text = self.subject_code

        return root
