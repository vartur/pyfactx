from datetime import datetime
from xml.etree.ElementTree import Element, SubElement

from pydantic import Field
from typing_extensions import override

from .InvoiceProfile import InvoiceProfile
from .XMLBaseModel import XMLBaseModel
from .namespaces import RAM, UDT


class SupplyChainEvent(XMLBaseModel):
    occurrence_date: datetime = Field(...)

    @override
    def to_xml(self, element_name: str, _profile: InvoiceProfile):
        root = Element(f"{RAM}:{element_name}")

        # OccurrenceDateTime
        occ_date_elem = SubElement(root, f"{RAM}:OccurrenceDateTime")
        SubElement(occ_date_elem, f"{UDT}:DateTimeString",
                   attrib={"format": "102"}).text = self.occurrence_date.strftime("%Y%m%d")

        return root
