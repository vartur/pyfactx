from typing import Optional
from lxml import etree as ET

from pydantic import Field

from .InvoiceProfile import InvoiceProfile
from .XMLBaseModel import XMLBaseModel
from .namespaces import NAMESPACES, RAM


class ProductClassification(XMLBaseModel):
    list_id: Optional[str] = Field(default=None)
    class_code: str = Field(...)

    def to_xml(self, element_name: str, profile: InvoiceProfile) -> ET.Element:
        root = ET.Element(f"{{{NAMESPACES[RAM]}}}{element_name}")

        # ClassCode
        attrib = {"listID": self.list_id} if self.list_id else {}
        ET.SubElement(root, f"{{{NAMESPACES[RAM]}}}ClassCode", attrib=attrib).text = self.class_code

        return root
