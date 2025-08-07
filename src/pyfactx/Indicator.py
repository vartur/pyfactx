from typing import ClassVar
from lxml import etree as ET
from pydantic import Field, ConfigDict
from typing_extensions import override

from .InvoiceProfile import InvoiceProfile
from .XMLBaseModel import XMLBaseModel
from .namespaces import NAMESPACES, RAM, UDT


class Indicator(XMLBaseModel):
    """Represents a boolean indicator in Factur-X XML.

    This class handles boolean values that need to be represented as XML indicators
    in the Factur-X format. The value is serialized as 'true' or 'false' in the
    resulting XML.

    Attributes:
        indicator: The boolean value to be represented in XML
    """

    model_config = ConfigDict(
        frozen=True,  # Makes the class immutable
        validate_assignment=True
    )

    # XML element names
    XML_ELEMENTS: ClassVar[dict[str, str]] = {
        'indicator': 'Indicator'
    }

    indicator: bool = Field(
        ...,
        description="Boolean value to be represented as XML indicator"
    )

    @override
    def to_xml(self, element_name: str, _profile: InvoiceProfile) -> ET.Element:
        """Converts the indicator to XML format.

        Args:
            element_name: Name of the root XML element
            _profile: The Factur-X profile (unused in this class)

        Returns:
            ET.Element: The XML element containing the indicator

        Example:
            >>> indicator = Indicator(indicator=True)
            >>> xml = indicator.to_xml("MyIndicator", InvoiceProfile.BASIC)
            >>> ET.tostring(xml)
            b'<ram:MyIndicator><udt:Indicator>true</udt:Indicator></ram:MyIndicator>'
        """
        # Create root element
        root = ET.Element(f"{{{NAMESPACES[RAM]}}}{element_name}")

        # Add indicator element with proper namespace
        indicator_element = ET.SubElement(
            root,
            f"{{{NAMESPACES[UDT]}}}{self.XML_ELEMENTS['indicator']}"
        )
        indicator_element.text = str(self.indicator).lower()

        return root

    @classmethod
    def true(cls) -> 'Indicator':
        """Creates an Indicator instance with value True.

        Returns:
            Indicator: A new instance with indicator set to True
        """
        return cls(indicator=True)

    @classmethod
    def false(cls) -> 'Indicator':
        """Creates an Indicator instance with value False.

        Returns:
            Indicator: A new instance with indicator set to False
        """
        return cls(indicator=False)

    def __str__(self) -> str:
        """Returns string representation of the indicator.

        Returns:
            str: 'true' or 'false'
        """
        return str(self.indicator).lower()

    def __bool__(self) -> bool:
        """Allows using the Indicator instance directly in boolean contexts.

        Returns:
            bool: The indicator value
        """
        return self.indicator