from xml.etree.ElementTree import Element, SubElement

from pydantic import BaseModel, Field

from .InvoiceProfile import InvoiceProfile
from .namespaces import RAM, UDT


class Indicator(BaseModel):
    indicator: bool = Field(...)

    def to_xml(self, element_name: str, profile: InvoiceProfile = InvoiceProfile.MINIMUM) -> Element:
        root = Element(f"{RAM}:{element_name}")

        # Indicator
        SubElement(root, f"{UDT}:Indicator").text = "true" if self.indicator else "false"

        return root
