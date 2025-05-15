from datetime import datetime
from lxml import etree as ET

from pydantic import Field
from typing_extensions import override

from .InvoiceProfile import InvoiceProfile
from .XMLBaseModel import XMLBaseModel
from .namespaces import NAMESPACES, RAM, UDT


class SupplyChainEvent(XMLBaseModel):
    occurrence_date: datetime = Field(...)

    @override
    def to_xml(self, element_name: str, _profile: InvoiceProfile) -> ET.Element:
        root = ET.Element(f"{{{NAMESPACES[RAM]}}}{element_name}")

        # OccurrenceDateTime
        occ_date_elem = ET.SubElement(root, f"{{{NAMESPACES[RAM]}}}OccurrenceDateTime")
        ET.SubElement(occ_date_elem, f"{{{NAMESPACES[UDT]}}}DateTimeString",
                      attrib={"format": "102"}).text = self.occurrence_date.strftime("%Y%m%d")

        return root
