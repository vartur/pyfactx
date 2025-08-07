from typing import Optional, List, override
from lxml import etree as ET

from pydantic import Field, field_validator, ConfigDict

from .InvoiceProfile import InvoiceProfile
from .ReferencedDocument import ReferencedDocument
from .SpecifiedPeriod import SpecifiedPeriod
from .TradeAccountingAccount import TradeAccountingAccount
from .TradeAllowanceCharge import TradeAllowanceCharge
from .TradeSettlementLineMonetarySummation import TradeSettlementLineMonetarySummation
from .TradeTax import TradeTax
from .XMLBaseModel import XMLBaseModel
from .namespaces import NAMESPACES, RAM


class LineTradeSettlement(XMLBaseModel):
    """Represents settlement details for an invoice line item.

    This class models the trade settlement information according to Factur-X standards,
    including tax, allowances, charges, and monetary summation for individual line items.

    Attributes:
        applicable_trade_tax: Tax details applicable to this line item.
        billing_specified_period: Time period for which the billing applies.
        specified_trade_allowance_charges: List of allowances or charges.
        specified_trade_settlement_line_monetary_summation: Monetary totals for the line.
        additional_referenced_document: Additional document references (EN16931+).
        receivable_specified_trade_accounting_account: Accounting details (EN16931+).

    Examples:
        >>> settlement = LineTradeSettlement(
        ...     applicable_trade_tax=TradeTax(rate=20.0),
        ...     specified_trade_settlement_line_monetary_summation=
        ...         TradeSettlementLineMonetarySummation(line_total=100.0)
        ... )
    """

    model_config = ConfigDict(
        validate_assignment=True,
        arbitrary_types_allowed=True
    )

    applicable_trade_tax: TradeTax = Field(
        ...,
        description="Tax information for the line item"
    )

    billing_specified_period: Optional[SpecifiedPeriod] = Field(
        default=None,
        description="Time period for which the billing applies"
    )

    specified_trade_allowance_charges: Optional[List[TradeAllowanceCharge]] = Field(
        default=None,
        description="Allowances and charges applied to the line item"
    )

    specified_trade_settlement_line_monetary_summation: TradeSettlementLineMonetarySummation = Field(
        ...,
        description="Monetary totals for the line item"
    )

    additional_referenced_document: Optional[ReferencedDocument] = Field(
        default=None,
        description="Additional document references (EN16931+ only)"
    )

    receivable_specified_trade_accounting_account: Optional[TradeAccountingAccount] = Field(
        default=None,
        description="Accounting details (EN16931+ only)"
    )

    @field_validator('specified_trade_allowance_charges')
    def validate_allowance_charges(cls, value: Optional[List[TradeAllowanceCharge]]) -> Optional[List[TradeAllowanceCharge]]:
        """Validates the list of allowances and charges.

        Args:
            value: List of allowances and charges to validate

        Returns:
            The validated list of allowances and charges

        Raises:
            ValueError: If validation fails
        """
        if value is not None:
            # Remove empty lists
            if len(value) == 0:
                return None
            
            # Validate total impact
            total_impact = sum(
                charge.actual_amount for charge in value 
                if charge.actual_amount is not None
            )
            if total_impact < -1e12 or total_impact > 1e12:
                raise ValueError("Total allowances and charges amount is outside reasonable limits")
        return value

    @override
    def to_xml(self, element_name: str, profile: InvoiceProfile) -> ET.Element:
        """Converts the trade settlement to XML format.

        Creates an XML element representing the line trade settlement according to
        the Factur-X specification and the given profile level.

        Args:
            element_name: Name of the root XML element
            profile: Factur-X profile determining required elements

        Returns:
            ET.Element: XML element containing the settlement data

        Raises:
            ValueError: If required elements are missing for the specified profile
        """
        root = ET.Element(f"{{{NAMESPACES[RAM]}}}{element_name}")

        # Required elements
        root.append(
            self.applicable_trade_tax.to_xml("ApplicableTradeTax", profile)
        )

        root.append(
            self.specified_trade_settlement_line_monetary_summation.to_xml(
                "SpecifiedTradeSettlementLineMonetarySummation",
                profile
            )
        )

        # Optional elements
        if self.billing_specified_period:
            root.append(
                self.billing_specified_period.to_xml("BillingSpecifiedPeriod", profile)
            )

        if self.specified_trade_allowance_charges:
            for trade_allowance in self.specified_trade_allowance_charges:
                root.append(
                    trade_allowance.to_xml("SpecifiedTradeAllowanceCharge", profile)
                )

        # EN16931 and higher profile elements
        if profile >= InvoiceProfile.EN16931:
            if self.additional_referenced_document:
                root.append(
                    self.additional_referenced_document.to_xml(
                        "AdditionalReferencedDocument",
                        profile
                    )
                )

            if self.receivable_specified_trade_accounting_account:
                root.append(
                    self.receivable_specified_trade_accounting_account.to_xml(
                        "ReceivableSpecifiedTradeAccountingAccount",
                        profile
                    )
                )

        return root

    def __str__(self) -> str:
        """Returns a string representation of the trade settlement.

        Returns:
            str: Settlement details in readable format
        """
        parts = [
            f"Tax: {self.applicable_trade_tax}",
            f"Totals: {self.specified_trade_settlement_line_monetary_summation}"
        ]
        
        if self.billing_specified_period:
            parts.append(f"Period: {self.billing_specified_period}")
        
        if self.specified_trade_allowance_charges:
            charges = len(self.specified_trade_allowance_charges)
            parts.append(f"Allowances/Charges: {charges}")
            
        return " | ".join(parts)

    def validate_totals(self) -> bool:
        """Validates that all monetary amounts are consistent.

        Returns:
            bool: True if all totals are consistent, False otherwise
        """
        summation = self.specified_trade_settlement_line_monetary_summation
        
        # Basic validation of line totals
        if hasattr(summation, 'line_total'):
            charges_total = 0
            if self.specified_trade_allowance_charges:
                charges_total = sum(
                    charge.actual_amount for charge in self.specified_trade_allowance_charges 
                    if charge.actual_amount is not None
                )
            
            # Allow for small rounding differences
            return abs(summation.line_total + charges_total) < 0.01
            
        return True