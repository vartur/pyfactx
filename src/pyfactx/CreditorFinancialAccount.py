from typing import Optional, ClassVar, Dict
from lxml import etree as ET
from pydantic import Field, field_validator, model_validator
from typing_extensions import override
import re
from dataclasses import dataclass

from .InvoiceProfile import InvoiceProfile
from .XMLBaseModel import XMLBaseModel
from .namespaces import NAMESPACES, RAM


@dataclass
class IBANInfo:
    """Information about IBAN format for a specific country."""
    length: int
    structure: str
    example: str


class CreditorFinancialAccount(XMLBaseModel):
    """Represents a creditor's financial account information in Factur-X.

    This class handles financial account information according to EN16931 standard
    for electronic invoicing, including IBAN validation and account details.

    Attributes:
        iban_id (Optional[str]): International Bank Account Number (IBAN).
        account_name (Optional[str]): Name of the account holder (EN16931 profile).
        proprietary_id (Optional[str]): Proprietary identifier for the account.
    """

    # Class constants for validation
    MAX_ACCOUNT_NAME_LENGTH: ClassVar[int] = 70
    MAX_PROPRIETARY_ID_LENGTH: ClassVar[int] = 70
    MIN_IBAN_LENGTH: ClassVar[int] = 15
    MAX_IBAN_LENGTH: ClassVar[int] = 34

    # IBAN country information
    IBAN_INFO: ClassVar[Dict[str, IBANInfo]] = {
        'DE': IBANInfo(22, 'DE00 0000 0000 0000 0000 00', 'DE89 3704 0044 0532 0130 00'),
        'FR': IBANInfo(27, 'FR00 0000 0000 0000 0000 0000 000', 'FR14 2004 1010 0505 0001 3M02 606'),
        'GB': IBANInfo(22, 'GB00 0000 0000 0000 0000 00', 'GB29 NWBK 6016 1331 9268 19'),
        # Add more countries as needed
    }

    iban_id: Optional[str] = Field(
        default=None,
        description="International Bank Account Number (IBAN)",
        min_length=MIN_IBAN_LENGTH,
        max_length=MAX_IBAN_LENGTH
    )

    account_name: Optional[str] = Field(
        default=None,
        description="Name of the account holder (EN16931)",
        max_length=MAX_ACCOUNT_NAME_LENGTH
    )

    proprietary_id: Optional[str] = Field(
        default=None,
        description="Proprietary identifier for the account",
        max_length=MAX_PROPRIETARY_ID_LENGTH
    )

    @model_validator(mode='after')
    def validate_at_least_one_identifier(self) -> 'CreditorFinancialAccount':
        """Ensures that at least one account identifier is provided."""
        if not any([self.iban_id, self.proprietary_id]):
            raise ValueError(
                "At least one identifier (IBAN or proprietary ID) must be provided"
            )
        return self

    @staticmethod
    def format_iban(iban: str) -> str:
        """Formats IBAN with proper spacing for display.

        Args:
            iban (str): Raw IBAN string.

        Returns:
            str: Formatted IBAN with spaces every 4 characters.
        """
        iban = ''.join(iban.split()).upper()
        return ' '.join(iban[i:i + 4] for i in range(0, len(iban), 4))

    @staticmethod
    def calculate_iban_checksum(iban: str) -> bool:
        """Calculate IBAN checksum using the ISO 7064 MOD 97-10 standard.
        
        Args:
            iban (str): The IBAN string to validate (without spaces, uppercase).
            
        Returns:
            bool: True if the IBAN checksum is valid.
        """
        try:
            # Move the first four characters to the end
            rearranged = iban[4:] + iban[:4]

            # Convert letters to numbers (A=10, B=11, ...)
            numerical = ''.join(
                str(ord(c) - ord('A') + 10) if c.isalpha() else c
                for c in rearranged
            )

            return int(numerical) % 97 == 1
        except (ValueError, IndexError):
            return False

    @classmethod
    def get_iban_info(cls, country_code: str) -> Optional[IBANInfo]:
        """Get IBAN format information for a specific country.
        
        Args:
            country_code (str): Two-letter country code.
            
        Returns:
            Optional[IBANInfo]: IBAN information for the country, or None if unknown.
        """
        return cls.IBAN_INFO.get(country_code.upper())

    @field_validator('iban_id')
    def validate_iban(cls, v: Optional[str]) -> Optional[str]:
        """Validates the IBAN format and checksum if provided."""
        if v is not None:
            # Remove spaces and convert to uppercase
            v = ''.join(v.split()).upper()

            # Basic IBAN format validation
            if not re.match(r'^[A-Z]{2}[0-9]{2}[0-9A-Z]{11,30}$', v):
                raise ValueError(
                    "Invalid IBAN format. Must start with country code followed "
                    "by two check digits and account number"
                )

            # Validate country-specific format
            country_code = v[:2]
            iban_info = cls.get_iban_info(country_code)
            if iban_info:
                if len(v) != iban_info.length:
                    raise ValueError(
                        f"Invalid IBAN length for {country_code}. "
                        f"Expected {iban_info.length} characters, got {len(v)}. "
                        f"Example: {iban_info.example}"
                    )

            # Validate IBAN checksum
            if not cls.calculate_iban_checksum(v):
                raise ValueError("Invalid IBAN checksum")

            return v
        return None

    @field_validator('account_name', 'proprietary_id')
    def validate_text_fields(cls, v: Optional[str]) -> Optional[str]:
        """Validates text fields for invalid characters and format."""
        if v is not None:
            # Remove leading/trailing whitespace
            v = v.strip()

            # Check for invalid characters
            if re.search(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', v):
                raise ValueError("Field contains invalid control characters")

            # Check for minimum content
            if not v:
                raise ValueError("Field cannot be empty after trimming whitespace")

            # Check for reasonable character set
            if not re.match(r'^[\w\s\-.,&\'"+?/()]*$', v):
                raise ValueError(
                    "Field contains invalid characters. Allowed: letters, numbers, "
                    "spaces, and basic punctuation"
                )

            return v
        return None

    @override
    def to_xml(self, element_name: str, profile: InvoiceProfile) -> ET.Element:
        """Converts the financial account information to XML format.

        Args:
            element_name (str): Name of the XML element to create.
            profile (InvoiceProfile): The Factur-X profile being used.

        Returns:
            ET.Element: An XML element containing the financial account information.

        Raises:
            ValueError: If XML creation fails.
        """
        try:
            root = ET.Element(f"{{{NAMESPACES[RAM]}}}{element_name}")

            # IBANID - formatted with spaces for readability
            if self.iban_id:
                iban_element = ET.SubElement(root, f"{{{NAMESPACES[RAM]}}}IBANID")
                iban_element.text = self.format_iban(self.iban_id)

            # AccountName - only for EN16931 profile and higher
            if profile >= InvoiceProfile.EN16931 and self.account_name:
                name_element = ET.SubElement(
                    root, f"{{{NAMESPACES[RAM]}}}AccountName"
                )
                name_element.text = self.account_name

            # ProprietaryID
            if self.proprietary_id:
                prop_element = ET.SubElement(
                    root, f"{{{NAMESPACES[RAM]}}}ProprietaryID"
                )
                prop_element.text = self.proprietary_id

            return root

        except (ET.XMLSyntaxError, UnicodeEncodeError) as e:
            raise ValueError(f"Failed to create XML element: {str(e)}")

    def __str__(self) -> str:
        """Returns a human-readable string representation."""
        parts = []
        if self.iban_id:
            parts.append(f"IBAN: {self.format_iban(self.iban_id)}")
        if self.account_name:
            parts.append(f"Account Name: {self.account_name}")
        if self.proprietary_id:
            parts.append(f"Proprietary ID: {self.proprietary_id}")
        return ", ".join(parts)

    @classmethod
    def from_iban(cls, iban: str, account_name: Optional[str] = None) -> 'CreditorFinancialAccount':
        """Create an account instance from IBAN.

        Args:
            iban (str): The IBAN.
            account_name (Optional[str]): Optional account holder name.

        Returns:
            CreditorFinancialAccount: New instance with provided IBAN.
        """
        return cls(iban_id=iban, account_name=account_name)
