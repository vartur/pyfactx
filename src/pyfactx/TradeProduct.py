from typing import Optional, override
from xml.etree.ElementTree import Element, SubElement

from pydantic import Field

from .InvoiceProfile import InvoiceProfile
from .XMLBaseModel import XMLBaseModel
from .namespaces import RAM


class TradeProduct(XMLBaseModel):
    global_id: Optional[str] = Field(default=None)
    name: str = Field(...)

    @override
    def to_xml(self, element_name: str, _profile: InvoiceProfile) -> Element:
        root = Element(f"{RAM}:{element_name}")

        # GlobalID
        if self.global_id:
            SubElement(root, f"{RAM}:GlobalID").text = self.global_id

        # Name
        SubElement(root, f"{RAM}:Name").text = self.name

        return root
