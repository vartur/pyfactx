from xml.etree.ElementTree import Element, SubElement

from pydantic import Field
from typing_extensions import override

from .InvoiceProfile import InvoiceProfile
from .XMLBaseModel import XMLBaseModel
from .namespaces import RAM, UDT


class Indicator(XMLBaseModel):
    indicator: bool = Field(...)

    @override
    def to_xml(self, element_name: str, _profile: InvoiceProfile) -> Element:
        root = Element(f"{RAM}:{element_name}")

        # Indicator
        SubElement(root, f"{UDT}:Indicator").text = "true" if self.indicator else "false"

        return root
