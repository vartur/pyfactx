from typing import Optional
from lxml import etree as ET

from pydantic import Field
from typing_extensions import override

from .InvoiceProfile import InvoiceProfile
from .XMLBaseModel import XMLBaseModel
from .namespaces import NAMESPACES, RAM


class TradeAddress(XMLBaseModel):
    postcode: Optional[str] = Field(default=None)
    line_one: Optional[str] = Field(default=None)
    line_two: Optional[str] = Field(default=None)
    line_three: Optional[str] = Field(default=None)
    city: Optional[str] = Field(default=None)
    country: str = Field(...)
    country_subdivision: Optional[str] = Field(default=None)

    @override
    def to_xml(self, element_name: str, profile: InvoiceProfile) -> ET.Element:
        root = ET.Element(f"{{{NAMESPACES[RAM]}}}{element_name}")

        if profile >= InvoiceProfile.BASICWL:
            # PostcodeCode
            if self.postcode:
                ET.SubElement(root, f"{{{NAMESPACES[RAM]}}}PostcodeCode").text = self.postcode

            # LineOne
            if self.line_one:
                ET.SubElement(root, f"{{{NAMESPACES[RAM]}}}LineOne").text = self.line_one

            # LineTwo
            if self.line_two:
                ET.SubElement(root, f"{{{NAMESPACES[RAM]}}}LineTwo").text = self.line_two

            # LineThree
            if self.line_three:
                ET.SubElement(root, f"{{{NAMESPACES[RAM]}}}LineThree").text = self.line_three

            # CityName
            if self.city:
                ET.SubElement(root, f"{{{NAMESPACES[RAM]}}}CityName").text = self.city

        # CountryID
        ET.SubElement(root, f"{{{NAMESPACES[RAM]}}}CountryID").text = self.country

        if profile >= InvoiceProfile.BASICWL:
            # CountrySubdivisionName
            if self.country_subdivision:
                ET.SubElement(root, f"{{{NAMESPACES[RAM]}}}CountrySubDivisionName").text = self.country_subdivision

        return root
