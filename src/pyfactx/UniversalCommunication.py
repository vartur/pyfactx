from typing import Optional
from lxml import etree as ET

from pydantic import Field

from .InvoiceProfile import InvoiceProfile
from .XMLBaseModel import XMLBaseModel
from .namespaces import NAMESPACES, RAM


class UniversalCommunication(XMLBaseModel):
    uri_id: Optional[str] = Field(default=None)  # email
    complete_number: Optional[str] = Field(default=None)  # phone number

    def to_xml(self, element_name: str, profile: InvoiceProfile) -> ET.Element:
        root = ET.Element(f"{{{NAMESPACES[RAM]}}}{element_name}")

        # URIID
        if self.uri_id:
            attrib = {"schemeID": "EM"} if element_name == "URIUniversalCommunication" else {}
            ET.SubElement(root, f"{{{NAMESPACES[RAM]}}}URIID", attrib=attrib).text = self.uri_id

        # CompleteNumber
        if self.complete_number:
            ET.SubElement(root, f"{{{NAMESPACES[RAM]}}}CompleteNumber").text = self.complete_number

        return root
