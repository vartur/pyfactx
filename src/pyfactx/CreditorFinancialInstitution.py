import re

from lxml import etree as ET
from pydantic import Field, field_validator

from .InvoiceProfile import InvoiceProfile
from .XMLBaseModel import XMLBaseModel
from .namespaces import NAMESPACES, RAM


class CreditorFinancialInstitution(XMLBaseModel):
    """Represents a creditor's financial institution in Factur-X.

    This class handles the Business Identifier Code (BIC/SWIFT) of the financial institution,
    according to ISO 9362 standard. The BIC code uniquely identifies banks and financial institutions
    globally.

    Attributes:
        bic_id (str): Business Identifier Code (BIC/SWIFT) of the financial institution.
            Format: BBBBCCLLXXX where:
            - BBBB: Bank code (4 letters)
            - CC: Country code (2 letters)
            - LL: Location code (2 letters/digits)
            - XXX: Branch code (3 characters, optional)

    Example:
        ```python
        institution = CreditorFinancialInstitution(bic_id="DEUTDEFF500")
        ```
    """

    bic_id: str = Field(
        ...,
        description="Business Identifier Code (BIC/SWIFT)",
        min_length=8,
        max_length=11
    )

    @field_validator('bic_id')
    def validate_bic(cls, v: str) -> str:
        """Validates the BIC (SWIFT) code format.

        Args:
            v (str): BIC code to validate.

        Returns:
            str: Validated and formatted BIC code.

        Raises:
            ValueError: If the BIC format is invalid.
        """
        if v is None:
            raise ValueError("BIC code is required")

        # Remove spaces and convert to uppercase
        v = ''.join(v.split()).upper()

        # Validate length (8 or 11 characters)
        if len(v) not in (8, 11):
            raise ValueError("BIC must be either 8 or 11 characters long")

        # Basic BIC format validation using regex
        # BBBB: 4 letters for bank code
        # CC: 2 letters for country code
        # LL: 2 alphanumeric characters for location code
        # XXX: 3 optional characters for branch code
        bic_pattern = r'^[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}(?:[A-Z0-9]{3})?$'
        if not re.match(bic_pattern, v):
            raise ValueError(
                "Invalid BIC format. Must be 4 letters (bank code), "
                "2 letters (country code), 2 alphanumeric chars (location), "
                "and optionally 3 alphanumeric chars (branch)"
            )

        # Additional country code validation
        country_code = v[4:6]
        if not cls.is_valid_country_code(country_code):
            raise ValueError(f"Invalid country code in BIC: {country_code}")

        return v

    @staticmethod
    def is_valid_country_code(country_code: str) -> bool:
        """Validates if the given country code is a valid ISO 3166-1 alpha-2 code.

        Args:
            country_code (str): Two-letter country code to validate.

        Returns:
            bool: True if the country code is valid, False otherwise.
        """
        # List of valid ISO 3166-1 alpha-2 country codes
        # This is a subset focusing on countries that commonly use BIC
        VALID_COUNTRY_CODES = {
            'AD', 'AE', 'AT', 'AU', 'BE', 'BG', 'BH', 'BR', 'CA', 'CH', 'CN',
            'CY', 'CZ', 'DE', 'DK', 'EE', 'ES', 'FI', 'FR', 'GB', 'GR', 'HK',
            'HR', 'HU', 'IE', 'IL', 'IS', 'IT', 'JP', 'LI', 'LT', 'LU', 'LV',
            'MC', 'MT', 'MX', 'NL', 'NO', 'NZ', 'PL', 'PT', 'RO', 'SE', 'SG',
            'SI', 'SK', 'SM', 'TR', 'US', 'VA'
        }
        return country_code in VALID_COUNTRY_CODES

    def to_xml(self, element_name: str, profile: InvoiceProfile) -> ET.Element:
        """Converts the financial institution information to XML format.

        Args:
            element_name (str): Name of the XML element to create.
            profile (InvoiceProfile): The Factur-X profile being used.

        Returns:
            ET.Element: An XML element containing the financial institution information.

        Raises:
            ValueError: If XML creation fails.
        """
        try:
            root = ET.Element(f"{{{NAMESPACES[RAM]}}}{element_name}")

            # BICID
            bic_element = ET.SubElement(root, f"{{{NAMESPACES[RAM]}}}BICID")
            bic_element.text = self.bic_id

            return root

        except (ET.XMLSyntaxError, UnicodeEncodeError) as e:
            raise ValueError(f"Failed to create XML element: {str(e)}")

    @classmethod
    def validate_branch_code(cls, bic: str) -> bool:
        """Validates the branch code portion of a BIC if present.

        Args:
            bic (str): Complete BIC code.

        Returns:
            bool: True if the branch code is valid or not present, False otherwise.
        """
        if len(bic) == 11:
            branch_code = bic[8:]
            # Branch code 'XXX' is a valid default for primary office
            return branch_code.isalnum() or branch_code == 'XXX'
        return True
