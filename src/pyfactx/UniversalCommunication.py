from typing import Optional
from xml.etree.ElementTree import Element, SubElement

from pydantic import Field

from .InvoiceProfile import InvoiceProfile
from .XMLBaseModel import XMLBaseModel
from .namespaces import RAM


class UniversalCommunication(XMLBaseModel):
    uri_id: Optional[str] = Field(default=None)  # email
    complete_number: Optional[str] = Field(default=None)  # phone number

    def to_xml(self, element_name: str, profile: InvoiceProfile) -> Element:
        root = Element(f"{RAM}:{element_name}")

        # URIID
        if self.uri_id:
            SubElement(root, f"{RAM}:URIID", attrib={"schemeID": "EM"}).text = self.uri_id

        # CompleteNumber
        if self.complete_number:
            SubElement(root, f"{RAM}:CompleteNumber").text = self.complete_number

        return root
