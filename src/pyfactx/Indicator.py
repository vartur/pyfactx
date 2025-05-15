from lxml import etree as ET

from pydantic import Field
from typing_extensions import override

from .InvoiceProfile import InvoiceProfile
from .XMLBaseModel import XMLBaseModel
from .namespaces import NAMESPACES, RAM, UDT


class Indicator(XMLBaseModel):
    indicator: bool = Field(...)

    @override
    def to_xml(self, element_name: str, _profile: InvoiceProfile) -> ET.Element:
        root = ET.Element(f"{{{NAMESPACES[RAM]}}}{element_name}")

        # Indicator
        ET.SubElement(root, f"{{{NAMESPACES[UDT]}}}Indicator").text = "true" if self.indicator else "false"

        return root
