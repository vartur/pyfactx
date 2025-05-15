from xml.etree.ElementTree import Element, SubElement

from pydantic import Field

from .InvoiceProfile import InvoiceProfile
from .XMLBaseModel import XMLBaseModel
from .namespaces import RAM


class TradeCountry(XMLBaseModel):
    country_id: str = Field(...)

    def to_xml(self, element_name: str, profile: InvoiceProfile) -> Element:
        root = Element(f"{RAM}:{element_name}")

        # ID
        SubElement(root, f"{RAM}:ID").text = self.country_id

        return root
