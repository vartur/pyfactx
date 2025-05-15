from lxml import etree as ET

from pydantic import Field

from .InvoiceProfile import InvoiceProfile
from .XMLBaseModel import XMLBaseModel
from .namespaces import NAMESPACES, RAM


class ProductCharacteristic(XMLBaseModel):
    description: str = Field(...)
    value: str = Field(...)

    def to_xml(self, element_name: str, profile: InvoiceProfile) -> ET.Element:
        root = ET.Element(f"{{{NAMESPACES[RAM]}}}{element_name}")

        # Description
        ET.SubElement(root, f"{{{NAMESPACES[RAM]}}}Description").text = self.description

        # Value
        ET.SubElement(root, f"{{{NAMESPACES[RAM]}}}Value").text = self.value

        return root
