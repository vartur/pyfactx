from lxml import etree as ET
from typing import override

from pydantic import Field, field_validator, ConfigDict

from .InvoiceProfile import InvoiceProfile
from .XMLBaseModel import XMLBaseModel
from .namespaces import NAMESPACES, RAM


class ProductCharacteristic(XMLBaseModel):
    """Represents a characteristic or attribute of a product in the invoice.

    This class models product characteristics according to the Factur-X standard,
    allowing for detailed product attribute descriptions and their corresponding values.

    Attributes:
        description: Description of the characteristic (e.g., "Color", "Size", "Material")
        value: The actual value of the characteristic (e.g., "Red", "XL", "Cotton")

    Examples:
        >>> color = ProductCharacteristic(
        ...     description="Color",
        ...     value="Navy Blue"
        ... )
        >>> size = ProductCharacteristic(
        ...     description="Size",
        ...     value="XL"
        ... )
    """

    model_config = ConfigDict(
        validate_assignment=True,
        str_strip_whitespace=True,
        str_max_length=1000
    )

    description: str = Field(
        ...,
        description="Description of the product characteristic",
        min_length=1,
        max_length=256,
        examples=["Color", "Size", "Material", "Weight"]
    )

    value: str = Field(
        ...,
        description="Value of the product characteristic",
        min_length=1,
        max_length=256,
        examples=["Red", "XL", "Cotton", "150g"]
    )

    @field_validator('description')
    def validate_description(cls, value: str) -> str:
        """Validates the characteristic description.

        Args:
            value: Description to validate

        Returns:
            str: Validated description

        Raises:
            ValueError: If description validation fails
        """
        # Remove excessive whitespace
        value = " ".join(value.split())
        
        # Check for minimum meaningful content
        if len(value.strip()) < 1:
            raise ValueError("Characteristic description cannot be empty")
            
        # Check for reasonable length
        if len(value) > 256:
            raise ValueError("Characteristic description is too long")
            
        # Check for valid characters
        if not all(c.isprintable() for c in value):
            raise ValueError("Description contains invalid characters")
            
        return value

    @field_validator('value')
    def validate_value(cls, value: str) -> str:
        """Validates the characteristic value.

        Args:
            value: Value to validate

        Returns:
            str: Validated value

        Raises:
            ValueError: If value validation fails
        """
        # Remove excessive whitespace
        value = " ".join(value.split())
        
        # Check for minimum meaningful content
        if len(value.strip()) < 1:
            raise ValueError("Characteristic value cannot be empty")
            
        # Check for reasonable length
        if len(value) > 256:
            raise ValueError("Characteristic value is too long")
            
        # Check for valid characters
        if not all(c.isprintable() for c in value):
            raise ValueError("Value contains invalid characters")
            
        return value

    @override
    def to_xml(self, element_name: str, _profile: InvoiceProfile) -> ET.Element:
        """Converts the product characteristic to XML format.

        Creates an XML element representing the product characteristic according to
        the Factur-X specification.

        Args:
            element_name: Name of the root XML element
            _profile: Factur-X profile (unused but required by interface)

        Returns:
            ET.Element: XML element containing the characteristic data
        """
        root = ET.Element(f"{{{NAMESPACES[RAM]}}}{element_name}")

        # Description (required)
        description_element = ET.SubElement(
            root,
            f"{{{NAMESPACES[RAM]}}}Description"
        )
        description_element.text = self.description

        # Value (required)
        value_element = ET.SubElement(
            root,
            f"{{{NAMESPACES[RAM]}}}Value"
        )
        value_element.text = self.value

        return root

    def __str__(self) -> str:
        """Returns a string representation of the characteristic.

        Returns:
            str: Characteristic in "description: value" format
        """
        return f"{self.description}: {self.value}"

    def matches(self, search_term: str) -> bool:
        """Checks if the characteristic matches a search term.

        Args:
            search_term: Term to search for in description or value

        Returns:
            bool: True if the search term is found in description or value
        """
        search_term = search_term.lower()
        return (
            search_term in self.description.lower() or
            search_term in self.value.lower()
        )

    def to_dict(self) -> dict:
        """Converts the characteristic to a dictionary.

        Returns:
            dict: Dictionary containing the characteristic data
        """
        return {
            "description": self.description,
            "value": self.value
        }

    @classmethod
    def from_key_value(cls, key: str, value: str) -> "ProductCharacteristic":
        """Creates a characteristic from a key-value pair.

        Args:
            key: Description of the characteristic
            value: Value of the characteristic

        Returns:
            ProductCharacteristic: New characteristic instance

        Raises:
            ValueError: If key or value validation fails
        """
        return cls(description=key, value=value)