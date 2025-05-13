from typing import Optional
from xml.etree.ElementTree import Element, SubElement

from pydantic import Field
from typing_extensions import override

from .InvoiceProfile import InvoiceProfile
from .XMLBaseModel import XMLBaseModel
from .namespaces import RAM


class TradeAddress(XMLBaseModel):
    postcode: Optional[str] = Field(default=None)
    line_one: Optional[str] = Field(default=None)
    line_two: Optional[str] = Field(default=None)
    line_three: Optional[str] = Field(default=None)
    city: Optional[str] = Field(default=None)
    country: str = Field(...)
    country_subdivision: Optional[str] = Field(default=None)

    @override
    def to_xml(self, element_name: str, profile: InvoiceProfile) -> Element:
        root = Element(f"{RAM}:{element_name}")

        if profile != InvoiceProfile.MINIMUM:
            # PostcodeCode
            if self.postcode:
                SubElement(root, f"{RAM}:PostcodeCode").text = self.postcode

            # LineOne
            if self.line_one:
                SubElement(root, f"{RAM}:LineOne").text = self.line_one

            # LineTwo
            if self.line_two:
                SubElement(root, f"{RAM}:LineTwo").text = self.line_two

            # LineThree
            if self.line_three:
                SubElement(root, f"{RAM}:LineThree").text = self.line_three

            # CityName
            if self.city:
                SubElement(root, f"{RAM}:CityName").text = self.city

        # CountryID
        SubElement(root, f"{RAM}:CountryID").text = self.country

        if profile != InvoiceProfile.MINIMUM:
            # CountrySubdivisionName
            if self.country_subdivision:
                SubElement(root, f"{RAM}:CountrySubDivisionName").text = self.country_subdivision

        return root
