from typing import Optional
from lxml import etree as ET

from pydantic import Field, field_validator
from typing_extensions import override

from .InvoiceProfile import InvoiceProfile
from .UniversalCommunication import UniversalCommunication
from .XMLBaseModel import XMLBaseModel
from .namespaces import NAMESPACES, RAM


class TradeContact(XMLBaseModel):
    """Represents a trade contact according to UN/CEFACT standards.
    
    This class models contact information for trade parties in electronic
    invoices, including personal and departmental details along with
    communication methods.

    Attributes:
        person_name: Name of the contact person
        department_name: Name of the department
        telephone_universal_communication: Phone contact details
        email_uri_universal_communication: Email contact details
    """

    person_name: Optional[str] = Field(
        default=None,
        description="Name of the contact person",
        max_length=140
    )
    
    department_name: Optional[str] = Field(
        default=None,
        description="Name of the department",
        max_length=70
    )
    
    telephone_universal_communication: Optional[UniversalCommunication] = Field(
        default=None,
        description="Phone contact details"
    )
    
    email_uri_universal_communication: Optional[UniversalCommunication] = Field(
        default=None,
        description="Email contact details"
    )

    @field_validator('person_name')
    def validate_person_name(cls, v: Optional[str]) -> Optional[str]:
        """Validates the person name if provided.

        Args:
            v: The person name to validate

        Returns:
            Optional[str]: The validated person name

        Raises:
            ValueError: If name contains invalid characters
        """
        if v is not None:
            if not v.strip():
                raise ValueError("Person name cannot be empty or whitespace")
            if any(char.isdigit() for char in v):
                raise ValueError("Person name should not contain numbers")
        return v

    @field_validator('department_name')
    def validate_department_name(cls, v: Optional[str]) -> Optional[str]:
        """Validates the department name if provided.

        Args:
            v: The department name to validate

        Returns:
            Optional[str]: The validated department name

        Raises:
            ValueError: If name is empty or whitespace
        """
        if v is not None and not v.strip():
            raise ValueError("Department name cannot be empty or whitespace")
        return v

    def has_contact_method(self) -> bool:
        """Checks if at least one contact method is provided.

        Returns:
            bool: True if either phone or email is provided
        """
        return bool(self.telephone_universal_communication or 
                   self.email_uri_universal_communication)

    @override
    def to_xml(self, element_name: str, profile: InvoiceProfile) -> ET.Element:
        """Converts the trade contact to its XML representation.

        Creates an XML element representing this trade contact according to
        the Cross Industry Invoice (CII) XML schema.

        Args:
            element_name: The name to use for the root XML element
            profile: The invoice profile containing serialization settings

        Returns:
            ET.Element: An XML element representing this trade contact

        Example:
            ```xml
            <ram:DefinedTradeContact>
                <ram:PersonName>John Doe</ram:PersonName>
                <ram:DepartmentName>Sales</ram:DepartmentName>
                <ram:TelephoneUniversalCommunication>
                    <!-- Phone details -->
                </ram:TelephoneUniversalCommunication>
                <ram:EmailURIUniversalCommunication>
                    <!-- Email details -->
                </ram:EmailURIUniversalCommunication>
            </ram:DefinedTradeContact>
            ```
        """
        root = ET.Element(f"{{{NAMESPACES[RAM]}}}{element_name}")

        # PersonName
        if self.person_name:
            ET.SubElement(root, f"{{{NAMESPACES[RAM]}}}PersonName").text = self.person_name

        # DepartmentName
        if self.department_name:
            ET.SubElement(root, f"{{{NAMESPACES[RAM]}}}DepartmentName").text = self.department_name

        # TelephoneUniversalCommunication
        if self.telephone_universal_communication:
            root.append(self.telephone_universal_communication.to_xml(
                "TelephoneUniversalCommunication", 
                profile
            ))

        # EmailURIUniversalCommunication
        if self.email_uri_universal_communication:
            root.append(self.email_uri_universal_communication.to_xml(
                "EmailURIUniversalCommunication", 
                profile
            ))

        return root

    def __str__(self) -> str:
        """Returns a human-readable string representation.

        Returns:
            str: Description of the trade contact
        """
        parts = []
        if self.person_name:
            parts.append(f"Person: {self.person_name}")
        if self.department_name:
            parts.append(f"Department: {self.department_name}")
        if not parts:
            return "Empty Trade Contact"
        return ", ".join(parts)