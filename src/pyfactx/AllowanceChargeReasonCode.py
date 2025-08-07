from enum import Enum
from typing import Optional, Dict


class AllowanceChargeReasonCode(Enum):
    """Allowance and charge reason codes based on UN/CEFACT code list 5189.
    
    These codes are used to specify the reason for allowances (discounts) or charges
    in electronic invoices. The codes are compliant with European e-invoicing 
    standards (EN 16931) and UN/CEFACT code list 5189.

    Each code represents a specific reason for applying an allowance or charge
    in business transactions.

    References:
        - UN/CEFACT code list 5189: https://unece.org/trade/uncefact
        - EN 16931 (European e-invoicing standard)
        - Peppol BIS Billing 3.0: https://docs.peppol.eu/poacc/billing/3.0/
    """
    
    BONUS_FOR_WORKS_AHEAD_OF_SCHEDULE = 41
    OTHER_BONUS = 42
    MANUFACTURERS_CONSUMER_DISCOUNT = 60
    DUE_TO_MILITARY_STATUS = 62
    DUE_TO_WORK_ACCIDENT = 63
    SPECIAL_AGREEMENT = 64
    PRODUCTION_ERROR_DISCOUNT = 65
    NEW_OUTLET_DISCOUNT = 66
    SAMPLE_DISCOUNT = 67
    END_OF_RANGE_DISCOUNT = 68
    INCOTERM_DISCOUNT = 70
    POINT_OF_SALE_THRESHOLD_ALLOWANCE = 71
    MATERIAL_SURCHARGE_OR_DEDUCTION = 88
    DISCOUNT = 95
    SPECIAL_REBATE = 100
    FIXED_LONG_TERM = 102
    TEMPORARY = 103
    STANDARD = 104
    YEARLY_TURNOVER = 105

    @classmethod
    def get_description(cls, code: 'AllowanceChargeReasonCode') -> str:
        """Returns a detailed description of the allowance/charge reason code.

        Args:
            code (AllowanceChargeReasonCode): The reason code enum value.

        Returns:
            str: Detailed description of the reason code.

        Example:
            ```python
            desc = AllowanceChargeReasonCode.get_description(
                AllowanceChargeReasonCode.DISCOUNT
            )
            ```
        """
        descriptions: Dict[AllowanceChargeReasonCode, str] = {
            cls.BONUS_FOR_WORKS_AHEAD_OF_SCHEDULE: 
                "Bonus payment or adjustment for works completed ahead of schedule",
            cls.OTHER_BONUS: 
                "Other forms of bonus payment not elsewhere specified",
            cls.MANUFACTURERS_CONSUMER_DISCOUNT: 
                "Discount given by the manufacturer directly to the consumer",
            cls.DUE_TO_MILITARY_STATUS: 
                "Special discount applied due to customer's military status",
            cls.DUE_TO_WORK_ACCIDENT: 
                "Adjustment or allowance related to a work accident",
            cls.SPECIAL_AGREEMENT: 
                "Special reduction based on a specific agreement between parties",
            cls.PRODUCTION_ERROR_DISCOUNT: 
                "Discount given due to a production error or product defect",
            cls.NEW_OUTLET_DISCOUNT: 
                "Special discount applied for new outlets or locations",
            cls.SAMPLE_DISCOUNT: 
                "Discount applied for product samples or demonstration items",
            cls.END_OF_RANGE_DISCOUNT: 
                "Discount for end-of-series, end-of-range, or discontinued products",
            cls.INCOTERM_DISCOUNT: 
                "Discount based on agreed delivery terms (Incoterms)",
            cls.POINT_OF_SALE_THRESHOLD_ALLOWANCE: 
                "Discount applied when reaching point of sale threshold",
            cls.MATERIAL_SURCHARGE_OR_DEDUCTION: 
                "Adjustment applied for material costs (surcharge or deduction)",
            cls.DISCOUNT: 
                "General discount applied to the transaction",
            cls.SPECIAL_REBATE: 
                "Special rebate or reduction based on specific conditions",
            cls.FIXED_LONG_TERM: 
                "Fixed reduction applied based on long-term arrangement",
            cls.TEMPORARY: 
                "Temporary reduction or discount for a limited time",
            cls.STANDARD: 
                "Standard reduction applied according to normal business terms",
            cls.YEARLY_TURNOVER: 
                "Reduction or allowance based on yearly turnover achievements"
        }
        return descriptions.get(code, "Unknown allowance/charge reason code")

    @classmethod
    def from_code(cls, code: int) -> Optional['AllowanceChargeReasonCode']:
        """Creates an AllowanceChargeReasonCode enum from a numeric code.

        Args:
            code (int): The numeric code value.

        Returns:
            Optional[AllowanceChargeReasonCode]: The corresponding enum value,
                or None if not found.

        Example:
            ```python
            code = AllowanceChargeReasonCode.from_code(95)
            if code:
                print(code.name)  # Outputs: "DISCOUNT"
            ```
        """
        try:
            return cls(code)
        except ValueError:
            return None

    @classmethod
    def is_valid_code(cls, code: int) -> bool:
        """Checks if a numeric code is a valid allowance/charge reason code.

        Args:
            code (int): The numeric code to validate.

        Returns:
            bool: True if the code is valid, False otherwise.

        Example:
            ```python
            is_valid = AllowanceChargeReasonCode.is_valid_code(95)
            ```
        """
        return any(code == member.value for member in cls)

    @classmethod
    def get_all_codes(cls) -> list[tuple[int, str]]:
        """Returns all available allowance/charge reason codes with descriptions.

        Returns:
            list[tuple[int, str]]: List of tuples containing code values
                and their descriptions.

        Example:
            ```python
            codes = AllowanceChargeReasonCode.get_all_codes()
            for code, desc in codes:
                print(f"{code}: {desc}")
            ```
        """
        return [(member.value, cls.get_description(member)) 
                for member in cls]

    def __str__(self) -> str:
        """Returns a human-readable string representation of the reason code.

        Returns:
            str: String representation including code and description.

        Example:
            ```python
            code = AllowanceChargeReasonCode.DISCOUNT
            print(str(code))
            ```
        """
        return f"{self.name} ({self.value}): {self.get_description(self)}"

    def is_bonus(self) -> bool:
        """Checks if the code represents a bonus-type allowance.

        Returns:
            bool: True if the code is bonus-related, False otherwise.
        """
        return self.value in {41, 42}

    def is_discount(self) -> bool:
        """Checks if the code represents a discount-type allowance.

        Returns:
            bool: True if the code is discount-related, False otherwise.
        """
        return self.value in {60, 62, 63, 64, 65, 66, 67, 68, 70, 71, 95}

    def is_special_agreement(self) -> bool:
        """Checks if the code represents a special agreement type allowance.

        Returns:
            bool: True if the code is related to special agreements, False otherwise.
        """
        return self.value in {64, 100, 102}