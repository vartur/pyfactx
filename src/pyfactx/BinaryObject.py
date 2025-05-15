from xml.etree.ElementTree import Element

from pydantic import Field

from .InvoiceProfile import InvoiceProfile
from .XMLBaseModel import XMLBaseModel
from .namespaces import RAM


class BinaryObject(XMLBaseModel):
    content_b64: str = Field(...)
    mime_code: str = Field(...)
    filename: str = Field(...)

    def to_xml(self, element_name: str, profile: InvoiceProfile) -> Element:
        root = Element(f"{RAM}:{element_name}", attrib={"mimeCode": self.mime_code, "filename": self.filename})

        root.text = self.content_b64

        return root
