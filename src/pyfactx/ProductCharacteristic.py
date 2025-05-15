from xml.etree.ElementTree import Element, SubElement

from pydantic import Field

from .InvoiceProfile import InvoiceProfile
from .XMLBaseModel import XMLBaseModel
from .namespaces import RAM


class ProductCharacteristic(XMLBaseModel):
    description: str = Field(...)
    value: str = Field(...)

    def to_xml(self, element_name: str, profile: InvoiceProfile) -> Element:
        root = Element(f"{RAM}:{element_name}")

        # Description
        SubElement(root, f"{RAM}:Description").text = self.description

        # Value
        SubElement(root, f"{RAM}:Value").text = self.value

        return root
