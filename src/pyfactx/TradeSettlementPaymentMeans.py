from typing import Optional
from lxml import etree as ET

from pydantic import Field
from typing_extensions import override

from .CreditorFinancialAccount import CreditorFinancialAccount
from .CreditorFinancialInstitution import CreditorFinancialInstitution
from .DebtorFinancialAccount import DebtorFinancialAccount
from .InvoiceProfile import InvoiceProfile
from .PaymentMeansCode import PaymentMeansCode
from .TradeSettlementFinancialCard import TradeSettlementFinancialCard
from .XMLBaseModel import XMLBaseModel
from .namespaces import NAMESPACES, RAM


class TradeSettlementPaymentMeans(XMLBaseModel):
    payment_means_code: PaymentMeansCode = Field(...)
    information: Optional[str] = Field(default=None)  # From EN16931
    applicable_trade_settlement_financial_card: Optional[TradeSettlementFinancialCard] = Field(
        default=None)  # From EN16931
    payer_party_debtor_financial_account: Optional[DebtorFinancialAccount] = Field(default=None)
    payee_party_creditor_financial_account: Optional[CreditorFinancialAccount] = Field(default=None)
    payee_specified_creditor_financial_institution: Optional[CreditorFinancialInstitution] = Field(
        default=None)  # From EN16931

    @override
    def to_xml(self, element_name: str, profile: InvoiceProfile) -> ET.Element:
        root = ET.Element(f"{{{NAMESPACES[RAM]}}}{element_name}")

        # TypeCode
        ET.SubElement(root, f"{{{NAMESPACES[RAM]}}}TypeCode").text = str(self.payment_means_code.value)

        if profile >= InvoiceProfile.EN16931:
            # Information
            if self.information:
                ET.SubElement(root, f"{{{NAMESPACES[RAM]}}}Information").text = self.information

            # ApplicableTradeSettlementFinancialCard
            if self.applicable_trade_settlement_financial_card:
                root.append(
                    self.applicable_trade_settlement_financial_card.to_xml("ApplicableTradeSettlementFinancialCard",
                                                                           profile))

        # PayerPartyDebtorFinancialAccount
        if self.payer_party_debtor_financial_account:
            root.append(self.payer_party_debtor_financial_account.to_xml("PayerPartyDebtorFinancialAccount", profile))

        # PayeePartyCreditorFinancialAccount
        if self.payee_party_creditor_financial_account:
            root.append(
                self.payee_party_creditor_financial_account.to_xml("PayeePartyCreditorFinancialAccount", profile))

        if profile >= InvoiceProfile.EN16931:
            # PayeeSpecifiedCreditorFinancialInstitution
            if self.payee_specified_creditor_financial_institution:
                root.append(self.payee_specified_creditor_financial_institution.to_xml(
                    "PayeeSpecifiedCreditorFinancialInstitution", profile))

        return root
