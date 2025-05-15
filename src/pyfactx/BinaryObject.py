from lxml import etree as ET

from pydantic import Field

from .InvoiceProfile import InvoiceProfile
from .XMLBaseModel import XMLBaseModel
from .namespaces import NAMESPACES, RAM


class BinaryObject(XMLBaseModel):
    content_b64: str = Field(...)
    mime_code: str = Field(...)
    filename: str = Field(...)

    def to_xml(self, element_name: str, profile: InvoiceProfile) -> ET.Element:
        root = ET.Element(f"{{{NAMESPACES[RAM]}}}{element_name}", attrib={"mimeCode": self.mime_code, "filename": self.filename})

        root.text = self.content_b64

        return root
