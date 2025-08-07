from typing import Optional
from lxml import etree as ET

from pydantic import Field, field_validator
from typing_extensions import override

from .InvoiceProfile import InvoiceProfile
from .XMLBaseModel import XMLBaseModel
from .namespaces import NAMESPACES, RAM


class TradeAddress(XMLBaseModel):
    """Represents a trade address according to UN/CEFACT standards.
    
    This class models a postal address used in trade documents, particularly
    in electronic invoices. It supports different levels of detail based on
    the invoice profile being used.

    Attributes:
        postcode (Optional[str]): Postal code or ZIP code
        line_one (Optional[str]): First line of the address (e.g., street and number)
        line_two (Optional[str]): Second line of the address (e.g., building, suite)
        line_three (Optional[str]): Third line of the address (e.g., additional info)
        city (Optional[str]): City or town name
        country (str): ISO 3166-1 alpha-2 country code (required)
        country_subdivision (Optional[str]): Region, state, or province
    """

    postcode: Optional[str] = Field(
        default=None,
        description="Postal code or ZIP code",
        max_length=16
    )
    line_one: Optional[str] = Field(
        default=None,
        description="First line of the address (e.g., street and number)",
        max_length=256
    )
    line_two: Optional[str] = Field(
        default=None,
        description="Second line of the address (e.g., building, suite)",
        max_length=256
    )
    line_three: Optional[str] = Field(
        default=None,
        description="Third line of the address (e.g., additional info)",
        max_length=256
    )
    city: Optional[str] = Field(
        default=None,
        description="City or town name",
        max_length=128
    )
    country: str = Field(
        ...,
        description="ISO 3166-1 alpha-2 country code",
        min_length=2,
        max_length=2
    )
    country_subdivision: Optional[str] = Field(
        default=None,
        description="Region, state, or province",
        max_length=128
    )

    @field_validator('country')
    def validate_country_code(cls, v: str) -> str:
        """Validates that the country code is in ISO 3166-1 alpha-2 format.

        Args:
            v: The country code to validate

        Returns:
            str: The validated country code in uppercase

        Raises:
            ValueError: If the country code is not valid
        """
        v = v.upper()
        if not v.isalpha() or len(v) != 2:
            raise ValueError("Country code must be a 2-letter ISO 3166-1 alpha-2 code")
        return v

    @override
    def to_xml(self, element_name: str, profile: InvoiceProfile) -> ET.Element:
        """Converts the address to its XML representation.

        Creates an XML element representing this address according to
        the Cross Industry Invoice (CII) XML schema. The content varies
        based on the invoice profile level.

        Args:
            element_name: The name to use for the root XML element
            profile: The invoice profile containing serialization settings

        Returns:
            ET.Element: An XML element representing this address

        Example:
            ```xml
            <ram:TradeAddress>
                <ram:PostcodeCode>12345</ram:PostcodeCode>
                <ram:LineOne>123 Main St</ram:LineOne>
                <ram:CityName>Springfield</ram:CityName>
                <ram:CountryID>US</ram:CountryID>
                <ram:CountrySubDivisionName>IL</ram:CountrySubDivisionName>
            </ram:TradeAddress>
            ```
        """
        root = ET.Element(f"{{{NAMESPACES[RAM]}}}{element_name}")

        # Extended information for BASICWL profile and above
        if profile >= InvoiceProfile.BASICWL:
            if self.postcode:
                ET.SubElement(root, f"{{{NAMESPACES[RAM]}}}PostcodeCode").text = self.postcode

            if self.line_one:
                ET.SubElement(root, f"{{{NAMESPACES[RAM]}}}LineOne").text = self.line_one

            if self.line_two:
                ET.SubElement(root, f"{{{NAMESPACES[RAM]}}}LineTwo").text = self.line_two

            if self.line_three:
                ET.SubElement(root, f"{{{NAMESPACES[RAM]}}}LineThree").text = self.line_three

            if self.city:
                ET.SubElement(root, f"{{{NAMESPACES[RAM]}}}CityName").text = self.city

        # Country is always required
        ET.SubElement(root, f"{{{NAMESPACES[RAM]}}}CountryID").text = self.country

        # Extended information for BASICWL profile and above
        if profile >= InvoiceProfile.BASICWL:
            if self.country_subdivision:
                ET.SubElement(root, f"{{{NAMESPACES[RAM]}}}CountrySubDivisionName").text = self.country_subdivision

        return root

    def __str__(self) -> str:
        """Returns a human-readable string representation of the address.

        Returns:
            str: Formatted address string
        """
        parts = []
        if self.line_one:
            parts.append(self.line_one)
        if self.line_two:
            parts.append(self.line_two)
        if self.line_three:
            parts.append(self.line_three)
        if self.city:
            city_parts = [self.city]
            if self.country_subdivision:
                city_parts.append(self.country_subdivision)
            if self.postcode:
                city_parts.append(self.postcode)
            parts.append(" ".join(city_parts))
        parts.append(self.country)
        return "\n".join(parts)