from typing import Optional
from decimal import Decimal
from lxml import etree as ET

from pydantic import Field, field_validator
from typing_extensions import override

from .AllowanceChargeReasonCode import AllowanceChargeReasonCode
from .Indicator import Indicator
from .InvoiceProfile import InvoiceProfile
from .TradeTax import TradeTax
from .XMLBaseModel import XMLBaseModel
from .namespaces import NAMESPACES, RAM


class TradeAllowanceCharge(XMLBaseModel):
    """Represents a trade allowance or charge according to UN/CEFACT standards.
    
    This class models allowances and charges applied to trade documents,
    particularly in electronic invoices. It supports both percentage-based
    and fixed-amount calculations.

    Attributes:
        charge_indicator (Indicator): Indicates if this is a charge (True) or
            allowance (False)
        calculation_percent (Optional[float]): Percentage rate used for calculation
        basis_amount (Optional[float]): Base amount for percentage calculations
        actual_amount (float): The actual amount of the allowance or charge
        reason_code (Optional[AllowanceChargeReasonCode]): Standardized reason code
        reason (Optional[str]): Textual description of the reason
        category_trade_tax (TradeTax): Tax category applying to this allowance/charge
    """

    charge_indicator: Indicator = Field(
        ...,
        description="True for charges, False for allowances"
    )
    calculation_percent: Optional[float] = Field(
        default=None,
        description="Percentage rate used for calculation",
        ge=0,  # Greater than or equal to 0
        le=100  # Less than or equal to 100
    )
    basis_amount: Optional[float] = Field(
        default=None,
        description="Base amount for percentage calculations",
        ge=0  # Greater than or equal to 0
    )
    actual_amount: float = Field(
        ...,
        description="The actual amount of the allowance or charge",
        exclude=False,
        ge=0
    )
    reason_code: Optional[AllowanceChargeReasonCode] = Field(
        default=None,
        description="Standardized reason code for the allowance or charge"
    )
    reason: Optional[str] = Field(
        default=None,
        description="Textual description of the reason",
        max_length=512
    )
    category_trade_tax: TradeTax = Field(
        ...,
        description="Tax category applying to this allowance or charge"
    )

    @field_validator('actual_amount')
    def validate_actual_amount(cls, v: float) -> float:
        """Validates the actual amount.

        Args:
            v: The amount to validate

        Returns:
            float: The validated amount

        Raises:
            ValueError: If amount is negative
        """
        if v < 0:
            raise ValueError("Actual amount cannot be negative")
        return v

    @field_validator('calculation_percent')
    def validate_calculation_percent(cls, v: Optional[float]) -> Optional[float]:
        """Validates the calculation percentage if provided.

        Args:
            v: The percentage to validate

        Returns:
            Optional[float]: The validated percentage

        Raises:
            ValueError: If percentage is invalid
        """
        if v is not None and not 0 <= v <= 100:
            raise ValueError("Calculation percentage must be between 0 and 100")
        return v

    def calculate_tax_amount(self) -> float:
        """Calculates the tax amount for this allowance or charge.

        Returns:
            float: The calculated tax amount
        """
        return round(self.actual_amount * (self.category_trade_tax.rate_applicable_percent / 100), 2)

    @override
    def to_xml(self, element_name: str, profile: InvoiceProfile) -> ET.Element:
        """Converts the allowance/charge to its XML representation.

        Creates an XML element representing this allowance or charge according to
        the Cross Industry Invoice (CII) XML schema.

        Args:
            element_name: The name to use for the root XML element
            profile: The invoice profile containing serialization settings

        Returns:
            ET.Element: An XML element representing this allowance/charge

        Example:
            ```xml
            <ram:AppliedTradeAllowanceCharge>
                <ram:ChargeIndicator>
                    <udt:Indicator>false</udt:Indicator>
                </ram:ChargeIndicator>
                <ram:CalculationPercent>10.0</ram:CalculationPercent>
                <ram:ActualAmount>100.00</ram:ActualAmount>
                <ram:ReasonCode>95</ram:ReasonCode>
                <ram:Reason>Volume discount</ram:Reason>
                <!-- CategoryTradeTax elements -->
            </ram:AppliedTradeAllowanceCharge>
            ```
        """
        root = ET.Element(f"{{{NAMESPACES[RAM]}}}{element_name}")

        # ChargeIndicator
        root.append(self.charge_indicator.to_xml("ChargeIndicator", profile))

        # CalculationPercent
        if self.calculation_percent is not None:
            ET.SubElement(root, f"{{{NAMESPACES[RAM]}}}CalculationPercent").text = str(self.calculation_percent)

        # BasisAmount
        if self.basis_amount is not None:
            ET.SubElement(root, f"{{{NAMESPACES[RAM]}}}BasisAmount").text = str(self.basis_amount)

        # ActualAmount
        ET.SubElement(root, f"{{{NAMESPACES[RAM]}}}ActualAmount").text = str(self.actual_amount)

        # ReasonCode
        if self.reason_code:
            ET.SubElement(root, f"{{{NAMESPACES[RAM]}}}ReasonCode").text = str(self.reason_code.value)

        # Reason
        if self.reason:
            ET.SubElement(root, f"{{{NAMESPACES[RAM]}}}Reason").text = self.reason

        # CategoryTradeTax
        root.append(self.category_trade_tax.to_xml("CategoryTradeTax", profile))

        return root

    def __str__(self) -> str:
        """Returns a human-readable string representation.

        Returns:
            str: Description of the allowance/charge
        """
        type_str = "Charge" if self.charge_indicator.value else "Allowance"
        amount_str = f"{self.actual_amount:.2f}"
        reason_str = f" ({self.reason})" if self.reason else ""
        return f"{type_str}: {amount_str}{reason_str}"