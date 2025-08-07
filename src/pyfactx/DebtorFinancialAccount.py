from lxml import etree as ET
from pydantic import Field, field_validator
from typing_extensions import override
import re
from typing import Optional

from .InvoiceProfile import InvoiceProfile
from .XMLBaseModel import XMLBaseModel
from .namespaces import NAMESPACES, RAM


class DebtorFinancialAccount(XMLBaseModel):
    """Represents a debtor's financial account information in Factur-X.

    This class handles the International Bank Account Number (IBAN) for the debtor's account,
    following ISO 13616 standard for IBAN formatting and validation.

    Attributes:
        iban_id (str): International Bank Account Number (IBAN) of the debtor's account.
            The IBAN consists of:
            - Country code (2 letters)
            - Check digits (2 numbers)
            - Basic Bank Account Number (BBAN) (up to 30 characters)

    Example:
        ```python
        debtor_account = DebtorFinancialAccount(iban_id="DE89370400440532013000")
        ```
    """

    iban_id: str = Field(
        ...,
        description="International Bank Account Number (IBAN)",
        min_length=15,
        max_length=34
    )

    @staticmethod
    def calculate_iban_checksum(iban: str) -> bool:
        """Calculate IBAN checksum using the ISO 7064 MOD 97-10 standard.
        
        Args:
            iban (str): The IBAN string to validate (without spaces, uppercase).
            
        Returns:
            bool: True if the IBAN checksum is valid, False otherwise.
        """
        # Move the first four characters to the end
        rearranged = iban[4:] + iban[:4]

        # Convert letters to numbers (A=10, B=11, ...)
        numerical = ''
        for c in rearranged:
            if c.isalpha():
                numerical += str(ord(c) - ord('A') + 10)
            else:
                numerical += c

        # Convert to integer and calculate the remainder
        try:
            return int(numerical) % 97 == 1
        except ValueError:
            return False

    @staticmethod
    def get_country_iban_length(country_code: str) -> Optional[int]:
        """Get the expected IBAN length for a specific country.
        
        Args:
            country_code (str): Two-letter country code.
            
        Returns:
            Optional[int]: Expected IBAN length for the country, or None if unknown.
        """
        # IBAN lengths by country
        IBAN_LENGTHS = {
            'AL': 28, 'AD': 24, 'AT': 20, 'AZ': 28, 'BH': 22, 'BE': 16, 'BA': 20,
            'BR': 29, 'BG': 22, 'CR': 22, 'HR': 21, 'CY': 28, 'CZ': 24, 'DK': 18,
            'DO': 28, 'EE': 20, 'FO': 18, 'FI': 18, 'FR': 27, 'GE': 22, 'DE': 22,
            'GI': 23, 'GR': 27, 'GL': 18, 'GT': 28, 'HU': 28, 'IS': 26, 'IE': 22,
            'IL': 23, 'IT': 27, 'KZ': 20, 'KW': 30, 'LV': 21, 'LB': 28, 'LI': 21,
            'LT': 20, 'LU': 20, 'MK': 19, 'MT': 31, 'MR': 27, 'MU': 30, 'MC': 27,
            'MD': 24, 'ME': 22, 'NL': 18, 'NO': 15, 'PK': 24, 'PS': 29, 'PL': 28,
            'PT': 25, 'QA': 29, 'RO': 24, 'SM': 27, 'SA': 24, 'RS': 22, 'SK': 24,
            'SI': 19, 'ES': 24, 'SE': 24, 'CH': 21, 'TN': 24, 'TR': 26, 'AE': 23,
            'GB': 22, 'VG': 24
        }
        return IBAN_LENGTHS.get(country_code)

    @field_validator('iban_id')
    def validate_iban(cls, v: str) -> str:
        """Validates the IBAN format and checksum.

        Validates the International Bank Account Number according to ISO 13616 standard.
        
        Args:
            v (str): IBAN to validate.

        Returns:
            str: Validated and formatted IBAN.

        Raises:
            ValueError: If the IBAN format is invalid or checksum verification fails.
        """
        if v is None:
            raise ValueError("IBAN is required")

        # Remove spaces and convert to uppercase
        v = ''.join(v.split()).upper()

        # Basic IBAN format validation
        if not re.match(r'^[A-Z]{2}[0-9]{2}[0-9A-Z]{11,30}$', v):
            raise ValueError(
                "Invalid IBAN format. Must start with country code, "
                "followed by two check digits and BBAN"
            )

        # Validate country-specific length
        country_code = v[:2]
        expected_length = cls.get_country_iban_length(country_code)
        if expected_length is not None and len(v) != expected_length:
            raise ValueError(
                f"Invalid IBAN length for country {country_code}. "
                f"Expected {expected_length} characters, got {len(v)}"
            )

        # Validate IBAN checksum
        if not cls.calculate_iban_checksum(v):
            raise ValueError("Invalid IBAN checksum")

        return v

    @override
    def to_xml(self, element_name: str, _profile: InvoiceProfile) -> ET.Element:
        """Converts the financial account information to XML format.

        Args:
            element_name (str): Name of the XML element to create.
            _profile (InvoiceProfile): The Factur-X profile being used 
                (not used in this implementation but required by interface).

        Returns:
            ET.Element: An XML element containing the financial account information.

        Raises:
            ValueError: If XML creation fails.
        """
        try:
            root = ET.Element(f"{{{NAMESPACES[RAM]}}}{element_name}")

            # IBANID
            iban_element = ET.SubElement(root, f"{{{NAMESPACES[RAM]}}}IBANID")
            iban_element.text = self.iban_id

            return root

        except (ET.XMLSyntaxError, UnicodeEncodeError) as e:
            raise ValueError(f"Failed to create XML element: {str(e)}")
