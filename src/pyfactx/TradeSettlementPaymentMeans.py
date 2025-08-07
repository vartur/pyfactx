from typing import Optional, override
from lxml import etree as ET

from pydantic import Field, field_validator, ConfigDict

from .CreditorFinancialAccount import CreditorFinancialAccount
from .CreditorFinancialInstitution import CreditorFinancialInstitution
from .DebtorFinancialAccount import DebtorFinancialAccount
from .InvoiceProfile import InvoiceProfile
from .PaymentMeansCode import PaymentMeansCode
from .TradeSettlementFinancialCard import TradeSettlementFinancialCard
from .XMLBaseModel import XMLBaseModel
from .namespaces import NAMESPACES, RAM


class TradeSettlementPaymentMeans(XMLBaseModel):
    """Represents payment means information for trade settlement.

    This class models the payment methods and related financial information
    according to UN/CEFACT standards.

    Attributes:
        payment_means_code: Code specifying the payment means
        information: Additional payment information
        applicable_trade_settlement_financial_card: Card payment details
        payer_party_debtor_financial_account: Debtor's account information
        payee_party_creditor_financial_account: Creditor's account information
        payee_specified_creditor_financial_institution: Creditor's bank details
    """

    model_config = ConfigDict(
        validate_assignment=True,
        strict=True
    )

    payment_means_code: PaymentMeansCode = Field(
        ...,
        description="Code specifying the payment means"
    )

    information: Optional[str] = Field(
        default=None,
        description="Additional payment information",
        max_length=512,  # Common limit for payment information
        examples=["Payment reference: INV-2025-001"]
    )

    applicable_trade_settlement_financial_card: Optional[TradeSettlementFinancialCard] = Field(
        default=None,
        description="Card payment details"
    )

    payer_party_debtor_financial_account: Optional[DebtorFinancialAccount] = Field(
        default=None,
        description="Debtor's account information"
    )

    payee_party_creditor_financial_account: Optional[CreditorFinancialAccount] = Field(
        default=None,
        description="Creditor's account information"
    )

    payee_specified_creditor_financial_institution: Optional[CreditorFinancialInstitution] = Field(
        default=None,
        description="Creditor's bank details"
    )

    @field_validator('information')
    def validate_information(cls, v: Optional[str]) -> Optional[str]:
        """Validates the payment information text.

        Args:
            v: The information text to validate

        Returns:
            Optional[str]: The validated information text

        Raises:
            ValueError: If the text is invalid
        """
        if v is not None:
            v = v.strip()
            if not v:
                return None

            # Check for invalid characters
            if any(char in v for char in '<>&'):
                raise ValueError("Information text cannot contain XML special characters")

        return v

    def validate_payment_details(self) -> None:
        """Validates the consistency of payment details based on payment means code.

        Raises:
            ValueError: If the payment details are inconsistent
        """
        code = self.payment_means_code

        # Credit card payment validation
        if code in [PaymentMeansCode.CREDIT_CARD, PaymentMeansCode.DEBIT_CARD]:
            if not self.applicable_trade_settlement_financial_card:
                raise ValueError(f"Card details required for payment means code {code}")

        # Bank transfer validation
        if code in [PaymentMeansCode.CREDIT_TRANSFER, PaymentMeansCode.SEPA_CREDIT_TRANSFER]:
            if not self.payee_party_creditor_financial_account:
                raise ValueError(f"Creditor account details required for payment means code {code}")

    @override
    def to_xml(self, element_name: str, profile: InvoiceProfile) -> ET.Element:
        """Converts the payment means information to XML representation.

        Creates an XML element representing the payment means according to
        the Cross Industry Invoice (CII) XML schema.

        Args:
            element_name: The name to use for the root XML element
            profile: The invoice profile containing serialization settings

        Returns:
            ET.Element: An XML element representing the payment means

        Example:
            ```xml
            <ram:SpecifiedTradeSettlementPaymentMeans>
                <ram:TypeCode>30</ram:TypeCode>
                <ram:Information>Payment reference: INV-2025-001</ram:Information>
                <!-- Additional financial details elements -->
            </ram:SpecifiedTradeSettlementPaymentMeans>
            ```
        """
        # Validate payment details before XML generation
        self.validate_payment_details()

        root = ET.Element(f"{{{NAMESPACES[RAM]}}}{element_name}")

        # TypeCode
        ET.SubElement(
            root,
            f"{{{NAMESPACES[RAM]}}}TypeCode"
        ).text = str(self.payment_means_code.value)

        if profile >= InvoiceProfile.EN16931:
            # Information
            if self.information:
                ET.SubElement(
                    root,
                    f"{{{NAMESPACES[RAM]}}}Information"
                ).text = self.information

            # ApplicableTradeSettlementFinancialCard
            if self.applicable_trade_settlement_financial_card:
                root.append(
                    self.applicable_trade_settlement_financial_card.to_xml(
                        "ApplicableTradeSettlementFinancialCard",
                        profile
                    )
                )

        # PayerPartyDebtorFinancialAccount
        if self.payer_party_debtor_financial_account:
            root.append(
                self.payer_party_debtor_financial_account.to_xml(
                    "PayerPartyDebtorFinancialAccount",
                    profile
                )
            )

        # PayeePartyCreditorFinancialAccount
        if self.payee_party_creditor_financial_account:
            root.append(
                self.payee_party_creditor_financial_account.to_xml(
                    "PayeePartyCreditorFinancialAccount",
                    profile
                )
            )

        if profile >= InvoiceProfile.EN16931:
            # PayeeSpecifiedCreditorFinancialInstitution
            if self.payee_specified_creditor_financial_institution:
                root.append(
                    self.payee_specified_creditor_financial_institution.to_xml(
                        "PayeeSpecifiedCreditorFinancialInstitution",
                        profile
                    )
                )

        return root

    def __str__(self) -> str:
        """Returns a human-readable string representation.

        Returns:
            str: Description of the payment means
        """
        parts = [f"Payment Method: {self.payment_means_code.name}"]
        if self.information:
            parts.append(f"Info: {self.information}")
        return " | ".join(parts)