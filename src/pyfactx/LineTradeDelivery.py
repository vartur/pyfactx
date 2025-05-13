from typing import Optional
from xml.etree.ElementTree import Element, SubElement

from pydantic import Field
from typing_extensions import override

from .InvoiceProfile import InvoiceProfile
from .UnitCode import UnitCode
from .XMLBaseModel import XMLBaseModel
from .namespaces import RAM


class LineTradeDelivery(XMLBaseModel):
    billed_quantity: float = Field(...)
    unit: Optional[UnitCode] = Field(default=None)

    @override
    def to_xml(self, element_name: str, _profile: InvoiceProfile) -> Element:
        root = Element(f"{RAM}:{element_name}")

        # BilledQuantity
        attrib = {"unitCode": self.unit} if self.unit else {}
        SubElement(root, f"{RAM}:BilledQuantity", attrib=attrib).text = str(self.billed_quantity)

        return root
