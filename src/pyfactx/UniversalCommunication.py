from typing import Optional
from lxml import etree as ET
import re

from pydantic import Field, field_validator, ConfigDict

from .InvoiceProfile import InvoiceProfile
from .XMLBaseModel import XMLBaseModel
from .namespaces import NAMESPACES, RAM


class UniversalCommunication(XMLBaseModel):
    """Represents universal communication details.
    
    This class models electronic communication details like email addresses
    and phone numbers according to UN/CEFACT standards.
    
    Attributes:
        uri_id: Email address
        complete_number: Phone number (can include spaces for readability)
    """

    model_config = ConfigDict(
        validate_assignment=True,
        strict=True
    )

    uri_id: Optional[str] = Field(
        default=None,
        description="Email address",
        pattern=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
        examples=["contact@example.com"]
    )

    complete_number: Optional[str] = Field(
        default=None,
        description="Phone number (can include spaces)",
        examples=["+1 202 555 0123", "+44 20 7123 4567"]
    )

    @field_validator('uri_id')
    def validate_email(cls, v: Optional[str]) -> Optional[str]:
        """Validates the email address.
        
        Args:
            v: The email address to validate
            
        Returns:
            Optional[str]: The validated email address
            
        Raises:
            ValueError: If the email address is invalid
        """
        if v is not None:
            v = v.strip().lower()
            if not v:
                return None

            # Detailed email validation pattern
            pattern = re.compile(r'''
                ^[a-zA-Z0-9._%+-]+       # username
                @                        # @ symbol
                [a-zA-Z0-9.-]+          # domain name
                \.[a-zA-Z]{2,}$         # top-level domain
            ''', re.VERBOSE)

            if not pattern.match(v):
                raise ValueError("Invalid email address format")

            # Check maximum length
            if len(v) > 254:  # RFC 5321
                raise ValueError("Email address too long")

        return v

    @field_validator('complete_number')
    def validate_phone(cls, v: Optional[str]) -> Optional[str]:
        """Validates the phone number.

        Accepts:
        - International format with + prefix
        - Local format without + prefix
        - Spaces between number groups
        """
        if v is not None:
            v = v.strip()
            if not v:
                return None

            # Remove multiple spaces
            v = ' '.join(v.split())

            # Extract digits for length validation
            digits_only = ''.join(c for c in v if c.isdigit())

            # Check minimum length
            if len(digits_only) < 8:
                raise ValueError("Phone number must have at least 8 digits")

            # Check maximum length
            if len(digits_only) > 15:
                raise ValueError("Phone number cannot have more than 15 digits")

            # Validate format: optional +, followed by digits and spaces
            if not re.match(r'^\+?[0-9][0-9 ]*$', v):
                raise ValueError("Phone number can only contain digits, spaces, and optional + prefix")

            return v

        return v


    def to_xml(self, element_name: str, profile: InvoiceProfile) -> ET.Element:
        """Converts the communication details to XML representation.

        Creates an XML element representing the communication details according to
        the Cross Industry Invoice (CII) XML schema.

        Args:
            element_name: The name to use for the root XML element
            profile: The invoice profile containing serialization settings

        Returns:
            ET.Element: An XML element representing the communication details

        Example:
            ```xml
            <ram:URIUniversalCommunication>
                <ram:URIID schemeID="EM">contact@example.com</ram:URIID>
            </ram:URIUniversalCommunication>
            ```
        """
        root = ET.Element(f"{{{NAMESPACES[RAM]}}}{element_name}")

        # URIID (Email)
        if self.uri_id:
            attrib = {"schemeID": "EM"} if element_name == "URIUniversalCommunication" else {}
            ET.SubElement(
                root,
                f"{{{NAMESPACES[RAM]}}}URIID",
                attrib=attrib
            ).text = self.uri_id

        # CompleteNumber (Phone)
        if self.complete_number:
            ET.SubElement(
                root,
                f"{{{NAMESPACES[RAM]}}}CompleteNumber"
            ).text = self.complete_number

        return root


    def __str__(self) -> str:
        """Returns a human-readable string representation.

        Returns:
            str: Description of the communication details
        """
        parts = []
        if self.uri_id:
            parts.append(f"Email: {self.uri_id}")
        if self.complete_number:
            parts.append(f"Phone: {self.complete_number}")
        return " | ".join(parts) if parts else "No communication details"


    def __repr__(self) -> str:
        """Returns a detailed string representation.

        Returns:
            str: Detailed representation of the communication details
        """
        parts = []
        if self.uri_id:
            parts.append(f"uri_id='{self.uri_id}'")
        if self.complete_number:
            parts.append(f"complete_number='{self.complete_number}'")
        return f"UniversalCommunication({', '.join(parts)})"
