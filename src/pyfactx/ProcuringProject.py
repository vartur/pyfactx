from lxml import etree as ET
from typing import override

from pydantic import Field, field_validator, ConfigDict

from .InvoiceProfile import InvoiceProfile
from .XMLBaseModel import XMLBaseModel
from .namespaces import NAMESPACES, RAM


class ProcuringProject(XMLBaseModel):
    """Represents a procuring project in the invoice.

    This class models the project information related to procurement
    in a Factur-X invoice, including project identification and name.

    Attributes:
        id: Project identifier
        name: Project name

    Examples:
        >>> project = ProcuringProject(
        ...     id="PRJ-2025-001",
        ...     name="Office Building Renovation"
        ... )
    """

    model_config = ConfigDict(
        validate_assignment=True,
        str_strip_whitespace=True,
        str_max_length=256  # Reasonable limit for project details
    )

    id: str = Field(
        ...,
        description="Project identifier",
        min_length=1,
        max_length=50,
        examples=["PRJ-2025-001", "2025-PROJECT-123"]
    )

    name: str = Field(
        ...,
        description="Project name",
        min_length=1,
        max_length=256,
        examples=["Office Renovation", "IT Infrastructure Update"]
    )

    @field_validator('id')
    def validate_id(cls, value: str) -> str:
        """Validates the project identifier.

        Args:
            value: Project ID to validate

        Returns:
            str: Validated project ID

        Raises:
            ValueError: If ID validation fails
        """
        # Remove excessive whitespace
        value = value.strip()
        
        # Check for valid characters
        if not all(c.isalnum() or c in '-_.' for c in value):
            raise ValueError(
                "Project ID can only contain letters, numbers, and -_."
            )
            
        # Check for reasonable format
        if not any(c.isalnum() for c in value):
            raise ValueError("Project ID must contain at least one alphanumeric character")
            
        return value

    @field_validator('name')
    def validate_name(cls, value: str) -> str:
        """Validates the project name.

        Args:
            value: Project name to validate

        Returns:
            str: Validated project name

        Raises:
            ValueError: If name validation fails
        """
        # Remove excessive whitespace
        value = " ".join(value.split())
        
        # Check for minimum meaningful content
        if len(value.strip()) < 1:
            raise ValueError("Project name cannot be empty")
            
        # Check for reasonable line length
        if any(len(line) > 100 for line in value.splitlines()):
            raise ValueError("Project name contains lines that are too long")
            
        return value

    @override
    def to_xml(self, element_name: str, _profile: InvoiceProfile) -> ET.Element:
        """Converts the project information to XML format.

        Creates an XML element representing the procuring project according to
        the Factur-X specification.

        Args:
            element_name: Name of the root XML element
            _profile: Factur-X profile (unused but required by interface)

        Returns:
            ET.Element: XML element containing the project data
        """
        root = ET.Element(f"{{{NAMESPACES[RAM]}}}{element_name}")

        # ID (required)
        id_element = ET.SubElement(
            root,
            f"{{{NAMESPACES[RAM]}}}ID"
        )
        id_element.text = self.id

        # Name (required)
        name_element = ET.SubElement(
            root,
            f"{{{NAMESPACES[RAM]}}}Name"
        )
        name_element.text = self.name

        return root

    def __str__(self) -> str:
        """Returns a string representation of the project.

        Returns:
            str: Project information in readable format
        """
        return f"Project {self.id}: {self.name}"

    def get_reference(self) -> str:
        """Returns a formatted reference string for the project.

        Returns:
            str: Formatted project reference
        """
        return f"Project Reference: {self.id}"

    def matches_identifier(self, search_id: str) -> bool:
        """Checks if a given identifier matches this project.

        Args:
            search_id: Project identifier to check

        Returns:
            bool: True if the identifiers match (case-insensitive)
        """
        return self.id.lower() == search_id.lower()