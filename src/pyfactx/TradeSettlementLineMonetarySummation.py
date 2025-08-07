from typing import Optional
from lxml import etree as ET

from pydantic import Field, field_validator, ConfigDict
from typing_extensions import override

from .InvoiceProfile import InvoiceProfile
from .XMLBaseModel import XMLBaseModel
from .namespaces import NAMESPACES, RAM


class TradeSettlementLineMonetarySummation(XMLBaseModel):
    """Represents monetary summation for a trade settlement line.

    This class models the line total amount and its currency according to
    UN/CEFACT standards.

    Attributes:
        line_total_amount: Total amount for the line item
        currency_code: Currency code for the amount (ISO 4217)
    """

    model_config = ConfigDict(
        validate_assignment=True,
        strict=True
    )

    line_total_amount: float = Field(
        ...,
        description="Total amount for the line item",
        examples=["100.00", "1234.56"]
    )

    currency_code: Optional[str] = Field(
        default=None,
        description="Currency code (ISO 4217)",
        min_length=3,
        max_length=3,
        pattern=r'^[A-Z]{3}$',
        examples=["EUR", "USD", "GBP"]
    )

    @field_validator('line_total_amount')
    def validate_amount(cls, v: float) -> float:
        """Validates the line total amount.

        Args:
            v: The amount to validate

        Returns:
            float: The validated amount

        Raises:
            ValueError: If the amount is invalid
        """
        # Check if amount has more than 2 decimal places
        if abs(round(v, 2) - v) > 1e-10:
            raise ValueError("Amount must have at most 2 decimal places")

        # Check if amount is negative
        if v < 0:
            raise ValueError("Amount cannot be negative")

        return round(v, 2)  # Ensure exactly 2 decimal places

    @field_validator('currency_code')
    def validate_currency(cls, v: Optional[str]) -> Optional[str]:
        """Validates the currency code.

        Args:
            v: The currency code to validate

        Returns:
            Optional[str]: The validated currency code

        Raises:
            ValueError: If the currency code is invalid
        """
        if v is not None:
            return v.upper()
        return v

    @override
    def to_xml(self, element_name: str, _profile: InvoiceProfile) -> ET.Element:
        """Converts the line monetary summation to XML representation.

        Creates an XML element representing the line total according to
        the Cross Industry Invoice (CII) XML schema.

        Args:
            element_name: The name to use for the root XML element
            _profile: The invoice profile (unused in this class)

        Returns:
            ET.Element: An XML element representing the line monetary summation

        Example:
            ```xml
            <ram:SpecifiedTradeSettlementLineMonetarySummation>
                <ram:LineTotalAmount currencyID="EUR">100.00</ram:LineTotalAmount>
            </ram:SpecifiedTradeSettlementLineMonetarySummation>
            ```
        """
        root = ET.Element(f"{{{NAMESPACES[RAM]}}}{element_name}")

        # LineTotalAmount with proper formatting
        attrib = {"currencyID": self.currency_code} if self.currency_code else {}
        ET.SubElement(
            root,
            f"{{{NAMESPACES[RAM]}}}LineTotalAmount",
            attrib=attrib
        ).text = f"{self.line_total_amount:.2f}"

        return root

    def __str__(self) -> str:
        """Returns a human-readable string representation.

        Returns:
            str: Description of the line monetary summation
        """
        amount = f"{self.line_total_amount:.2f}"
        if self.currency_code:
            return f"{amount} {self.currency_code}"
        return amount

    def __repr__(self) -> str:
        """Returns a detailed string representation.

        Returns:
            str: Detailed representation of the line monetary summation
        """
        currency_str = f", currency_code='{self.currency_code}'" if self.currency_code else ""
        return f"TradeSettlementLineMonetarySummation(line_total_amount={self.line_total_amount:.2f}{currency_str})"