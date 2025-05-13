from datetime import datetime
from typing import Optional, override
from xml.etree.ElementTree import Element, SubElement

from pydantic import Field

from .InvoiceProfile import InvoiceProfile
from .XMLBaseModel import XMLBaseModel
from .namespaces import RAM, UDT


class SpecifiedPeriod(XMLBaseModel):
    start_date: Optional[datetime] = Field(default=None)
    end_date: Optional[datetime] = Field(default=None)

    @override
    def to_xml(self, element_name: str, _profile: InvoiceProfile) -> Element:
        root = Element(f"{RAM}:{element_name}")

        # StartDateTime
        if self.start_date:
            start_elem = SubElement(root, f"{RAM}:StartDateTime")
            SubElement(start_elem, f"{UDT}:DateTimeString", attrib={"format": "102"}).text = self.start_date.strftime(
                "%Y%m%d")

        # EndDateTime
        if self.end_date:
            end_elem = SubElement(root, f"{RAM}:EndDateTime")
            SubElement(end_elem, f"{UDT}:DateTimeString", attrib={"format": "102"}).text = self.end_date.strftime(
                "%Y%m%d")

        return root
