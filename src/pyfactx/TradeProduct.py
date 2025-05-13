from typing import Optional
from xml.etree.ElementTree import Element, SubElement

from pydantic import BaseModel, Field

from .InvoiceProfile import InvoiceProfile
from .namespaces import RAM

class TradeProduct(BaseModel):
    global_id: Optional[str] = Field(default=None)
    name: str = Field(...)

    def to_xml(self, element_name: str, _profile: InvoiceProfile) -> Element:
        root = Element(f"{RAM}:{element_name}")

        # GlobalID
        if self.global_id:
            SubElement(root, f"{RAM}:GlobalID").text = self.global_id

        # Name
        SubElement(root, f"{RAM}:Name").text = self.name

        return root