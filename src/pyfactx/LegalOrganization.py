from typing import Optional, override
from lxml import etree as ET

from pydantic import Field, field_validator, ConfigDict

from .InvoiceProfile import InvoiceProfile
from .XMLBaseModel import XMLBaseModel
from .namespaces import NAMESPACES, RAM


class LegalOrganization(XMLBaseModel):
    """Represents a legal organization in Factur-X invoice.

    This class models the legal organization details according to Factur-X/EN16931 standards.
    It includes identification and trading name information for business entities.

    Attributes:
        id: Legal entity identifier
        trading_business_name: Official trading name of the organization.
            Required for EN16931 and higher profiles.

    Examples:
        >>> org = LegalOrganization(id="529900XYZSPDX6QIVV84", trading_business_name="ACME Corp")
        >>> org.id
        '529900XYZSPDX6QIVV84'
    """

    model_config = ConfigDict(
        str_strip_whitespace=True,
        str_min_length=1,
        validate_assignment=True
    )

    id: Optional[str] = Field(
        default=None,
        description="Legal Entity Identifier"
    )

    trading_business_name: Optional[str] = Field(
        default=None,
        description="Official trading name of the organization",
        max_length=512
    )


    @field_validator('trading_business_name')
    def validate_trading_name(cls, value: Optional[str]) -> Optional[str]:
        """Validates the trading business name.

        Args:
            value: Trading business name to validate

        Returns:
            The validated trading business name

        Raises:
            ValueError: If the name contains invalid characters or is empty when provided
        """
        if value is not None:
            if not value.strip():
                raise ValueError("Trading business name cannot be empty when provided")
            if any(char in value for char in '<>&'):
                raise ValueError("Trading business name contains invalid XML characters")
        return value

    @override
    def to_xml(self, element_name: str, profile: InvoiceProfile) -> ET.Element:
        """Converts the organization data to XML format.

        Creates an XML element representing the legal organization according to
        the Factur-X specification and the given profile level.

        Args:
            element_name: Name of the root XML element
            profile: Factur-X profile determining required elements

        Returns:
            ET.Element: XML element containing the organization data
        """
        root = ET.Element(f"{{{NAMESPACES[RAM]}}}{element_name}")

        if self.id:
            id_elem = ET.SubElement(root, f"{{{NAMESPACES[RAM]}}}ID")
            id_elem.text = self.id
            id_elem.set("schemeID", "0002")

        if profile >= InvoiceProfile.EN16931:
            name_elem = ET.SubElement(root, f"{{{NAMESPACES[RAM]}}}TradingBusinessName")
            name_elem.text = self.trading_business_name

        return root

    def __str__(self) -> str:
        """Returns a string representation of the organization.

        Returns:
            str: Organization details in readable format
        """
        parts = []
        if self.trading_business_name:
            parts.append(f"Name: {self.trading_business_name}")
        if self.id:
            parts.append(f"LEI: {self.id}")
        return " | ".join(parts) if parts else "Empty Organization"