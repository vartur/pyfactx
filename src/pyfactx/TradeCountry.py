from lxml import etree as ET
from typing_extensions import override, Final
from pydantic import Field, field_validator

from .InvoiceProfile import InvoiceProfile
from .XMLBaseModel import XMLBaseModel
from .namespaces import NAMESPACES, RAM

VALID_COUNTRY_CODES: Final[frozenset[str]] = frozenset([
    'AF', 'AX', 'AL', 'DZ', 'AS', 'AD', 'AO', 'AI', 'AQ', 'AG', 'AR', 'AM', 'AW',
    'AU', 'AT', 'AZ', 'BS', 'BH', 'BD', 'BB', 'BY', 'BE', 'BZ', 'BJ', 'BM', 'BT',
    'BO', 'BQ', 'BA', 'BW', 'BV', 'BR', 'IO', 'BN', 'BG', 'BF', 'BI', 'KH', 'CM',
    'CA', 'CV', 'KY', 'CF', 'TD', 'CL', 'CN', 'CX', 'CC', 'CO', 'KM', 'CG', 'CD',
    'CK', 'CR', 'CI', 'HR', 'CU', 'CW', 'CY', 'CZ', 'DK', 'DJ', 'DM', 'DO', 'EC',
    'EG', 'SV', 'GQ', 'ER', 'EE', 'SZ', 'ET', 'FK', 'FO', 'FJ', 'FI', 'FR', 'GF',
    'PF', 'TF', 'GA', 'GM', 'GE', 'DE', 'GH', 'GI', 'GR', 'GL', 'GD', 'GP', 'GU',
    'GT', 'GG', 'GN', 'GW', 'GY', 'HT', 'HM', 'VA', 'HN', 'HK', 'HU', 'IS', 'IN',
    'ID', 'IR', 'IQ', 'IE', 'IM', 'IL', 'IT', 'JM', 'JP', 'JE', 'JO', 'KZ', 'KE',
    'KI', 'KP', 'KR', 'KW', 'KG', 'LA', 'LV', 'LB', 'LS', 'LR', 'LY', 'LI', 'LT',
    'LU', 'MO', 'MG', 'MW', 'MY', 'MV', 'ML', 'MT', 'MH', 'MQ', 'MR', 'MU', 'YT',
    'MX', 'FM', 'MD', 'MC', 'MN', 'ME', 'MS', 'MA', 'MZ', 'MM', 'NA', 'NR', 'NP',
    'NL', 'NC', 'NZ', 'NI', 'NE', 'NG', 'NU', 'NF', 'MK', 'MP', 'NO', 'OM', 'PK',
    'PW', 'PS', 'PA', 'PG', 'PY', 'PE', 'PH', 'PN', 'PL', 'PT', 'PR', 'QA', 'RE',
    'RO', 'RU', 'RW', 'BL', 'SH', 'KN', 'LC', 'MF', 'PM', 'VC', 'WS', 'SM', 'ST',
    'SA', 'SN', 'RS', 'SC', 'SL', 'SG', 'SX', 'SK', 'SI', 'SB', 'SO', 'ZA', 'GS',
    'SS', 'ES', 'LK', 'SD', 'SR', 'SJ', 'SE', 'CH', 'SY', 'TW', 'TJ', 'TZ', 'TH',
    'TL', 'TG', 'TK', 'TO', 'TT', 'TN', 'TR', 'TM', 'TC', 'TV', 'UG', 'UA', 'AE',
    'GB', 'US', 'UM', 'UY', 'UZ', 'VU', 'VE', 'VN', 'VG', 'VI', 'WF', 'EH', 'YE',
    'ZM', 'ZW'
])


class TradeCountry(XMLBaseModel):
    """Represents a country in trade context according to UN/CEFACT standards.
    
    This class models country information using ISO 3166-1 alpha-2 country codes.
    
    Attributes:
        country_id: Two-letter ISO 3166-1 alpha-2 country code (e.g., 'FR' for France)
    """

    country_id: str = Field(
        ...,
        description="ISO 3166-1 alpha-2 country code",
        min_length=2,
        max_length=2,
        examples=['DE', 'FR', 'GB']
    )

    @field_validator('country_id')
    def validate_country_id(cls, v: str) -> str:
        """Validates the country code format and existence.

        Args:
            v: The country code to validate

        Returns:
            str: The validated country code in uppercase

        Raises:
            ValueError: If the country code format is invalid or country doesn't exist
        """
        v = v.upper()
        if not v.isalpha():
            raise ValueError("Country code must contain only letters")
        if len(v) != 2:
            raise ValueError("Country code must be exactly 2 letters (ISO 3166-1 alpha-2)")
        if v not in VALID_COUNTRY_CODES:
            raise ValueError(f"Invalid country code '{v}'. Must be a valid ISO 3166-1 alpha-2 code")
        return v

    @classmethod
    def is_valid_country_code(cls, code: str) -> bool:
        """Checks if a country code is valid.

        Args:
            code: The country code to check

        Returns:
            bool: True if the code is a valid ISO 3166-1 alpha-2 country code
        """
        return code.upper() in VALID_COUNTRY_CODES


    @override
    def to_xml(self, element_name: str, profile: InvoiceProfile) -> ET.Element:
        """Converts the trade country to its XML representation.

        Creates an XML element representing this country according to
        the Cross Industry Invoice (CII) XML schema.

        Args:
            element_name: The name to use for the root XML element
            profile: The invoice profile containing serialization settings

        Returns:
            ET.Element: An XML element representing this country

        Example:
            ```xml
            <ram:CountryID>FR</ram:CountryID>
            ```
        """
        root = ET.Element(f"{{{NAMESPACES[RAM]}}}{element_name}")
        ET.SubElement(root, f"{{{NAMESPACES[RAM]}}}ID").text = self.country_id
        return root

    def __str__(self) -> str:
        """Returns a human-readable string representation.

        Returns:
            str: The country code
        """
        return self.country_id


    def __eq__(self, other: object) -> bool:
        """Implements equality testing.

        Args:
            other: Another object to compare with

        Returns:
            bool: True if the other object is a TradeCountry with the same country_id
        """
        if not isinstance(other, TradeCountry):
            return NotImplemented
        return self.country_id == other.country_id