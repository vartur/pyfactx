from lxml import etree as ET

from pydantic import Field

from .InvoiceProfile import InvoiceProfile
from .XMLBaseModel import XMLBaseModel
from .namespaces import NAMESPACES, RAM


class ProcuringProject(XMLBaseModel):
    id: str = Field(...)
    name: str = Field(...)

    def to_xml(self, element_name: str, profile: InvoiceProfile) -> ET.Element:
        root = ET.Element(f"{{{NAMESPACES[RAM]}}}{element_name}")

        # ID
        ET.SubElement(root, f"{{{NAMESPACES[RAM]}}}ID").text = self.id

        # Name
        ET.SubElement(root, f"{{{NAMESPACES[RAM]}}}ID").text = self.name

        return root
