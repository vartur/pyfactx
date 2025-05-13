from datetime import datetime
from xml.etree.ElementTree import Element, SubElement

from pydantic import BaseModel, Field

from .InvoiceProfile import InvoiceProfile
from .namespaces import RAM, UDT


class SupplyChainEvent(BaseModel):
    occurrence_date: datetime = Field(...)

    def to_xml(self, element_name: str, _profile: InvoiceProfile):
        root = Element(f"{RAM}:{element_name}")

        # OccurrenceDateTime
        occ_date_elem = SubElement(root, f"{RAM}:OccurrenceDateTime")
        SubElement(occ_date_elem, f"{UDT}:DateTimeString",
                   attrib={"format": "102"}).text = self.occurrence_date.strftime("%Y%m%d")

        return root
