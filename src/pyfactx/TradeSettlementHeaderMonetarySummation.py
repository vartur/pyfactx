from typing import Optional, override
from typing import Optional, override

from lxml import etree as ET
from pydantic import Field, ConfigDict, model_validator
from typing_extensions import Annotated

from .InvoiceProfile import InvoiceProfile
from .XMLBaseModel import XMLBaseModel
from .namespaces import NAMESPACES, RAM


class TradeSettlementHeaderMonetarySummation(XMLBaseModel):
    """Represents monetary summation for trade settlement header.
    
    This class models the various amounts and totals in an invoice according to
    UN/CEFACT standards, ensuring mathematical consistency between values.
    
    Attributes:
        line_total_amount: Sum of line amounts
        charge_total_amount: Sum of charges
        allowance_total_amount: Sum of allowances
        tax_basis_total_amount: Total amount subject to tax
        tax_total_amount: Total tax amount
        rounding_amount: Rounding adjustment
        tax_currency_code: Currency for tax amounts
        grand_total_amount: Total amount including taxes
        total_prepaid_amount: Total prepaid amount
        due_payable_amount: Final amount due
    """

    model_config = ConfigDict(
        validate_assignment=True,
        strict=True
    )

    line_total_amount: Optional[Annotated[
        float,
        Field(
            description="Sum of line amounts"
        )
    ]] = None

    charge_total_amount: Optional[Annotated[
        float,
        Field(
            description="Sum of charges",
            ge=0
        )
    ]] = None

    allowance_total_amount: Optional[Annotated[
        float,
        Field(
            description="Sum of allowances",
            ge=0
        )
    ]] = None

    tax_basis_total_amount: Annotated[
        float,
        Field(
            description="Total amount subject to tax",
            ge=0
        )
    ]

    tax_total_amount: Optional[Annotated[
        float,
        Field(
            description="Total tax amount",
            ge=0
        )
    ]] = None

    rounding_amount: Optional[Annotated[
        float,
        Field(
            description="Rounding adjustment")
    ]] = None

    tax_currency_code: Optional[str] = Field(
        default="EUR",
        description="Currency code for tax amounts",
        min_length=3,
        max_length=3,
        pattern=r'^[A-Z]{3}$'
    )

    grand_total_amount: Annotated[
        float,
        Field(
            description="Total amount including taxes",
        )
    ]

    total_prepaid_amount: Optional[Annotated[
        float,
        Field(
            description="Total prepaid amount",
            ge=0
        )
    ]] = None

    due_payable_amount: Annotated[
        float,
        Field(
            description="Final amount due",
        )
    ]

    @model_validator(mode='after')
    def validate_amounts(self) -> 'TradeSettlementHeaderMonetarySummation':
        """Validates the mathematical consistency of all amounts.
        
        Returns:
            self: The validated instance
            
        Raises:
            ValueError: If amounts are mathematically inconsistent
        """
        # Calculate tax basis total if line items are present
        if all(x is not None for x in [self.line_total_amount, self.charge_total_amount, self.allowance_total_amount]):
            expected_tax_basis = (
                    self.line_total_amount +
                    (self.charge_total_amount or 0) -
                    (self.allowance_total_amount or 0)
            )
            if abs(expected_tax_basis - self.tax_basis_total_amount) > 0.02:
                raise ValueError(
                    "Tax basis total amount must equal: line total + charges - allowances"
                )

        # Calculate grand total
        expected_grand_total = (
                self.tax_basis_total_amount +
                (self.tax_total_amount or 0) +
                (self.rounding_amount or 0)
        )
        if abs(expected_grand_total - self.grand_total_amount) > 0.02:
            raise ValueError(
                "Grand total must equal: tax basis + tax total + rounding amount"
            )

        # Calculate due payable amount
        expected_due_payable = (
                self.grand_total_amount -
                (self.total_prepaid_amount or 0)
        )
        if abs(expected_due_payable - self.due_payable_amount) > 0.02:
            raise ValueError(
                "Due payable amount must equal: grand total - prepaid amount"
            )

        return self

    @override
    def to_xml(self, element_name: str, profile: InvoiceProfile) -> ET.Element:
        """Converts the monetary summation to XML representation.

        Args:
            element_name: The name to use for the root XML element
            profile: The invoice profile containing serialization settings

        Returns:
            ET.Element: An XML element representing the monetary summation
        """
        root = ET.Element(f"{{{NAMESPACES[RAM]}}}{element_name}")

        if profile >= InvoiceProfile.BASICWL:
            # LineTotalAmount
            if self.line_total_amount is not None:
                ET.SubElement(
                    root,
                    f"{{{NAMESPACES[RAM]}}}LineTotalAmount"
                ).text = f"{self.line_total_amount:.2f}"

            # ChargeTotalAmount
            if self.charge_total_amount is not None:
                ET.SubElement(
                    root,
                    f"{{{NAMESPACES[RAM]}}}ChargeTotalAmount"
                ).text = f"{self.charge_total_amount:.2f}"

            # AllowanceTotalAmount
            if self.allowance_total_amount is not None:
                ET.SubElement(
                    root,
                    f"{{{NAMESPACES[RAM]}}}AllowanceTotalAmount"
                ).text = f"{self.allowance_total_amount:.2f}"

        # TaxBasisTotalAmount
        ET.SubElement(
            root,
            f"{{{NAMESPACES[RAM]}}}TaxBasisTotalAmount"
        ).text = f"{self.tax_basis_total_amount:.2f}"

        # TaxTotalAmount
        if self.tax_total_amount is not None:
            attrib = {"currencyID": self.tax_currency_code} if self.tax_currency_code else {}
            ET.SubElement(
                root,
                f"{{{NAMESPACES[RAM]}}}TaxTotalAmount",
                attrib=attrib
            ).text = f"{self.tax_total_amount:.2f}"

        if profile >= InvoiceProfile.EN16931:
            if self.rounding_amount is not None:
                ET.SubElement(
                    root,
                    f"{{{NAMESPACES[RAM]}}}RoundingAmount"
                ).text = f"{self.rounding_amount:.2f}"

        # GrandTotalAmount
        ET.SubElement(
            root,
            f"{{{NAMESPACES[RAM]}}}GrandTotalAmount"
        ).text = f"{self.grand_total_amount:.2f}"

        if profile >= InvoiceProfile.BASICWL:
            # TotalPrepaidAmount
            if self.total_prepaid_amount is not None:
                ET.SubElement(
                    root,
                    f"{{{NAMESPACES[RAM]}}}TotalPrepaidAmount"
                ).text = f"{self.total_prepaid_amount:.2f}"

        # DuePayableAmount
        ET.SubElement(
            root,
            f"{{{NAMESPACES[RAM]}}}DuePayableAmount"
        ).text = f"{self.due_payable_amount:.2f}"

        return root

    def __str__(self) -> str:
        """Returns a human-readable string representation.

        Returns:
            str: Description of the monetary summation
        """
        parts = [
            f"Tax Basis: {self.tax_basis_total_amount:.2f}",
            f"Grand Total: {self.grand_total_amount:.2f}",
            f"Due: {self.due_payable_amount:.2f}"
        ]
        return " | ".join(parts)
