from enum import StrEnum
from typing import Dict


class TaxCategoryCode(StrEnum):
    """Tax category codes according to UN/CEFACT code list 5305.
    
    These codes are used to indicate the tax category for goods and services
    in accordance with European VAT regulations and international trade standards.

    Attributes:
        VAT_REVERSE_CHARGE (str): Code "AE" - VAT Reverse Charge
        EXEMPT_FROM_TAX (str): Code "E" - Exempt from tax
        STANDARD_RATE (str): Code "S" - Standard rate
        ZERO_RATED_GOODS (str): Code "Z" - Zero rated goods
        FREE_EXPORT_ITEM (str): Code "G" - Free export item
        SERVICES_OUTSIDE_SCOPE (str): Code "O" - Services outside scope of tax
        VAT_EXEMPT_EEA_INTRA_COMMUNITY_SUPPLY_GOODS_AND_SERVICES (str): Code "K" - VAT exempt for EEA intra-community supply
        CANARY_ISLANDS_GENERAL_INDIRECT_TAX (str): Code "L" - IGIC (Canary Islands)
        CEUTA_MELILLA_TAX_PRODUCTION_SERVICES_AND_IMPORTATION (str): Code "M" - IPSI (Ceuta and Melilla)
        TRANSFERRED_VAT (str): Code "B" - Transferred VAT
    """

    VAT_REVERSE_CHARGE = "AE"
    EXEMPT_FROM_TAX = "E"
    STANDARD_RATE = "S"
    ZERO_RATED_GOODS = "Z"
    FREE_EXPORT_ITEM = "G"
    SERVICES_OUTSIDE_SCOPE = "O"
    VAT_EXEMPT_EEA_INTRA_COMMUNITY_SUPPLY_GOODS_AND_SERVICES = "K"
    CANARY_ISLANDS_GENERAL_INDIRECT_TAX = "L"
    CEUTA_MELILLA_TAX_PRODUCTION_SERVICES_AND_IMPORTATION = "M"
    TRANSFERRED_VAT = "B"

    @property
    def description(self) -> str:
        """Gets the human-readable description of the tax category.

        Returns:
            str: Description of the tax category
        """
        return self._get_descriptions()[str(self.value)]

    @classmethod
    def _get_descriptions(cls) -> Dict[str, str]:
        """Internal method to get descriptions mapping.

        Returns:
            Dict[str, str]: Mapping of tax category codes to their descriptions
        """
        return {
            cls.VAT_REVERSE_CHARGE: "VAT Reverse Charge applies",
            cls.EXEMPT_FROM_TAX: "Exempt from tax",
            cls.STANDARD_RATE: "Standard VAT rate applicable",
            cls.ZERO_RATED_GOODS: "Zero rated goods",
            cls.FREE_EXPORT_ITEM: "Free export item, tax not charged",
            cls.SERVICES_OUTSIDE_SCOPE: "Services outside scope of tax",
            cls.VAT_EXEMPT_EEA_INTRA_COMMUNITY_SUPPLY_GOODS_AND_SERVICES: "VAT exempt for EEA intra-community supply",
            cls.CANARY_ISLANDS_GENERAL_INDIRECT_TAX: "IGIC (Canary Islands General Indirect Tax)",
            cls.CEUTA_MELILLA_TAX_PRODUCTION_SERVICES_AND_IMPORTATION: "IPSI (Tax for Production, Services and Importation in Ceuta and Melilla)",
            cls.TRANSFERRED_VAT: "Transferred VAT"
        }

    @classmethod
    def get_description(cls, code: str) -> str:
        """Gets the description for a given tax category code.

        Args:
            code: The tax category code to look up

        Returns:
            str: Description of the tax category

        Raises:
            KeyError: If the code is not valid
        """
        descriptions = cls._get_descriptions()
        if code not in descriptions:
            raise KeyError(f"Invalid tax category code: {code}")
        return descriptions[code]

    def is_zero_rated(self) -> bool:
        """Checks if the tax category represents a zero-rated condition.

        Returns:
            bool: True if the category is zero-rated
        """
        return self in (self.ZERO_RATED_GOODS, self.FREE_EXPORT_ITEM)

    def is_exempt(self) -> bool:
        """Checks if the tax category represents a tax-exempt condition.

        Returns:
            bool: True if the category is tax-exempt
        """
        return self in (
            self.EXEMPT_FROM_TAX,
            self.VAT_EXEMPT_EEA_INTRA_COMMUNITY_SUPPLY_GOODS_AND_SERVICES
        )

    def requires_tax_number(self) -> bool:
        """Checks if the tax category requires a tax registration number.

        Returns:
            bool: True if a tax number is required
        """
        return self in (
            self.VAT_REVERSE_CHARGE,
            self.VAT_EXEMPT_EEA_INTRA_COMMUNITY_SUPPLY_GOODS_AND_SERVICES
        )