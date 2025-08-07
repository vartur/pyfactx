from enum import StrEnum
from typing import Dict


class TaxTypeCode(StrEnum):
    """Tax type codes according to UN/EDIFACT code list 5153.
    
    These codes represent different types of duties, taxes, and fees used in
    international trade and business transactions.

    References:
        UN/EDIFACT code list 5153: Duty or tax or fee type name code
        https://unece.org/trade/uncefact
    """

    PETROLEUM_TAX = "AAA"
    PROVISIONAL_COUNTERVAILING_DUTY_CASH = "AAB"
    PROVISIONAL_COUNTERVAILING_DUTY_BOND = "AAC"
    TOBACCO_TAX = "AAD"
    ENERGY_FEE = "AAE"
    COFFEE_TAX = "AAF"
    ANTI_DUMPING_DUTY = "ADD"
    IMPOSTA_DI_BOLLO = "BOL"
    AGRICULTURAL_LEVY = "CAP"
    CAR_TAX = "CAR"
    PAPER_CONSORTIUM_TAX = "COC"
    COMMODITY_SPECIFIC_TAX = "CST"
    COUNTERVAILING_DUTY = "CVD"
    ENVIRONMENTAL_TAX = "ENV"
    EXCISE_DUTY = "EXC"
    AGRICULTURAL_EXPORT_REBATE = "EXP"
    FEDERAL_EXCISE_TAX = "FET"
    FREE = "FRE"
    GENERAL_CONSTRUCTION_TAX = "GCN"
    GOODS_AND_SERVICES_TAX = "GST"
    ILLUMINANTS_TAX = "ILL"
    IMPORT_TAX = "IMP"
    INDIVIDUAL_TAX = "IND"
    BUSINESS_LICENSE_FEE = "LAC"
    LOCAL_CONSTRUCTION_TAX = "LCN"
    LIGHT_DUES_PAYABLE = "LDP"
    LOCAL_SALES_TAX = "LOC"
    LUST_TAX = "LST"
    MONETARY_COMPENSATORY_AMOUNT = "MCA"
    MISCELLANEOUS_CASH_DEPOSIT = "MCD"
    OTHER_TAXES = "OTH"
    PROVISIONAL_DUTY_BOND = "PDB"
    PROVISIONAL_DUTY_CASH = "PDC"
    PREFERENCE_DUTY = "PRF"
    SPECIAL_CONSTRUCTION_TAX = "SCN"
    SHIFTED_SOCIAL_SECURITIES = "SSS"
    STATE_SALES_TAX = "STT"
    SUSPENDED_DUTY = "SUP"
    SURTAX = "SUR"
    SHIFTED_WAGE_TAX = "SWT"
    ALCOHOL_MARK_TAX = "TAC"
    TOTAL = "TOT"
    TURNOVER_TAX = "TOX"
    TONNAGE_TAXES = "TTA"
    VALUATION_DEPOSIT = "VAD"
    VALUE_ADDED_TAX = "VAT"

    @property
    def description(self) -> str:
        """Gets the human-readable description of the tax type.

        Returns:
            str: Description of the tax type
        """
        return self._get_descriptions()[str(self.value)]

    @classmethod
    def _get_descriptions(cls) -> Dict[str, str]:
        """Internal method to get descriptions mapping.

        Returns:
            Dict[str, str]: Mapping of tax type codes to their descriptions
        """
        return {
            cls.PETROLEUM_TAX: "Tax on petroleum products",
            cls.PROVISIONAL_COUNTERVAILING_DUTY_CASH: "Provisional countervailing duty paid in cash",
            cls.PROVISIONAL_COUNTERVAILING_DUTY_BOND: "Provisional countervailing duty secured by bond",
            cls.TOBACCO_TAX: "Tax on tobacco products",
            cls.ENERGY_FEE: "Fee charged for energy consumption",
            cls.COFFEE_TAX: "Tax on coffee products",
            cls.ANTI_DUMPING_DUTY: "Anti-dumping duty",
            cls.IMPOSTA_DI_BOLLO: "Italian stamp duty tax",
            cls.AGRICULTURAL_LEVY: "Agricultural levy",
            cls.CAR_TAX: "Tax on vehicles",
            cls.PAPER_CONSORTIUM_TAX: "Paper consortium tax",
            cls.COMMODITY_SPECIFIC_TAX: "Tax specific to certain commodities",
            cls.COUNTERVAILING_DUTY: "Countervailing duty",
            cls.ENVIRONMENTAL_TAX: "Environmental tax",
            cls.EXCISE_DUTY: "Excise duty",
            cls.AGRICULTURAL_EXPORT_REBATE: "Agricultural export rebate",
            cls.FEDERAL_EXCISE_TAX: "Federal excise tax",
            cls.FREE: "Free of tax",
            cls.GENERAL_CONSTRUCTION_TAX: "General construction tax",
            cls.GOODS_AND_SERVICES_TAX: "Goods and services tax (GST)",
            cls.ILLUMINANTS_TAX: "Tax on illuminants",
            cls.IMPORT_TAX: "Import tax",
            cls.INDIVIDUAL_TAX: "Individual tax",
            cls.BUSINESS_LICENSE_FEE: "Business license fee",
            cls.LOCAL_CONSTRUCTION_TAX: "Local construction tax",
            cls.LIGHT_DUES_PAYABLE: "Light dues payable",
            cls.LOCAL_SALES_TAX: "Local sales tax",
            cls.LUST_TAX: "Leaking Underground Storage Tank tax",
            cls.MONETARY_COMPENSATORY_AMOUNT: "Monetary compensatory amount",
            cls.MISCELLANEOUS_CASH_DEPOSIT: "Miscellaneous cash deposit",
            cls.OTHER_TAXES: "Other taxes",
            cls.PROVISIONAL_DUTY_BOND: "Provisional duty secured by bond",
            cls.PROVISIONAL_DUTY_CASH: "Provisional duty paid in cash",
            cls.PREFERENCE_DUTY: "Preference duty",
            cls.SPECIAL_CONSTRUCTION_TAX: "Special construction tax",
            cls.SHIFTED_SOCIAL_SECURITIES: "Shifted social securities",
            cls.STATE_SALES_TAX: "State sales tax",
            cls.SUSPENDED_DUTY: "Suspended duty",
            cls.SURTAX: "Surtax",
            cls.SHIFTED_WAGE_TAX: "Shifted wage tax",
            cls.ALCOHOL_MARK_TAX: "Alcohol mark tax",
            cls.TOTAL: "Total of all taxes",
            cls.TURNOVER_TAX: "Turnover tax",
            cls.TONNAGE_TAXES: "Tonnage taxes",
            cls.VALUATION_DEPOSIT: "Valuation deposit",
            cls.VALUE_ADDED_TAX: "Value added tax (VAT)"
        }

    @classmethod
    def get_description(cls, code: str) -> str:
        """Gets the description for a given tax type code.

        Args:
            code: The tax type code to look up

        Returns:
            str: Description of the tax type

        Raises:
            KeyError: If the code is not valid
        """
        descriptions = cls._get_descriptions()
        if code not in descriptions:
            raise KeyError(f"Invalid tax type code: {code}")
        return descriptions[code]

    def is_provisional(self) -> bool:
        """Checks if the tax type is provisional.

        Returns:
            bool: True if the tax type is provisional
        """
        return self in (
            self.PROVISIONAL_COUNTERVAILING_DUTY_CASH,
            self.PROVISIONAL_COUNTERVAILING_DUTY_BOND,
            self.PROVISIONAL_DUTY_BOND,
            self.PROVISIONAL_DUTY_CASH
        )

    def is_construction_related(self) -> bool:
        """Checks if the tax type is construction-related.

        Returns:
            bool: True if the tax type is related to construction
        """
        return self in (
            self.GENERAL_CONSTRUCTION_TAX,
            self.LOCAL_CONSTRUCTION_TAX,
            self.SPECIAL_CONSTRUCTION_TAX
        )

    def is_sales_tax(self) -> bool:
        """Checks if the tax type is a sales tax.

        Returns:
            bool: True if the tax type is a sales tax
        """
        return self in (
            self.LOCAL_SALES_TAX,
            self.STATE_SALES_TAX,
            self.VALUE_ADDED_TAX,
            self.GOODS_AND_SERVICES_TAX
        )