from datetime import datetime
from typing import Optional, override
from lxml import etree as ET

from pydantic import Field

from .InvoiceProfile import InvoiceProfile
from .XMLBaseModel import XMLBaseModel
from .namespaces import NAMESPACES, RAM, UDT


class SpecifiedPeriod(XMLBaseModel):
    start_date: Optional[datetime] = Field(default=None)
    end_date: Optional[datetime] = Field(default=None)

    @override
    def to_xml(self, element_name: str, _profile: InvoiceProfile) -> ET.Element:
        root = ET.Element(f"{{{NAMESPACES[RAM]}}}{element_name}")

        # StartDateTime
        if self.start_date:
            start_elem = ET.SubElement(root, f"{{{NAMESPACES[RAM]}}}StartDateTime")
            ET.SubElement(start_elem, f"{{{NAMESPACES[UDT]}}}DateTimeString",
                          attrib={"format": "102"}).text = self.start_date.strftime(
                "%Y%m%d")

        # EndDateTime
        if self.end_date:
            end_elem = ET.SubElement(root, f"{{{NAMESPACES[RAM]}}}EndDateTime")
            ET.SubElement(end_elem, f"{{{NAMESPACES[UDT]}}}DateTimeString", attrib={"format": "102"}).text = self.end_date.strftime(
                "%Y%m%d")

        return root
