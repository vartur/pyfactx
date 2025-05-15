from typing import Optional
from lxml import etree as ET

from pydantic import Field
from typing_extensions import override

from .InvoiceProfile import InvoiceProfile
from .UnitCode import UnitCode
from .XMLBaseModel import XMLBaseModel
from .namespaces import NAMESPACES, RAM


class LineTradeDelivery(XMLBaseModel):
    billed_quantity: float = Field(...)
    unit: Optional[UnitCode] = Field(default=None)

    @override
    def to_xml(self, element_name: str, _profile: InvoiceProfile) -> ET.Element:
        root = ET.Element(f"{{{NAMESPACES[RAM]}}}{element_name}")

        # BilledQuantity
        attrib = {"unitCode": self.unit} if self.unit else {}
        ET.SubElement(root, f"{{{NAMESPACES[RAM]}}}BilledQuantity", attrib=attrib).text = str(self.billed_quantity)

        return root
