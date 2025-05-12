from typing import Optional
from xml.etree.ElementTree import Element, SubElement

from pydantic import BaseModel, Field

from .CreditorFinancialAccount import CreditorFinancialAccount
from .DebtorFinancialAccount import DebtorFinancialAccount
from .InvoiceProfile import InvoiceProfile
from .PaymentMeansCode import PaymentMeansCode
from .namespaces import RAM


class TradeSettlementPaymentMeans(BaseModel):
    payment_means_code: PaymentMeansCode = Field(...)
    payer_party_debtor_financial_account: Optional[DebtorFinancialAccount] = Field(default=None)
    payee_party_creditor_financial_account: Optional[CreditorFinancialAccount] = Field(default=None)

    def to_xml(self, element_name: str, profile: InvoiceProfile = InvoiceProfile.MINIMUM) -> Element:
        root = Element(f"{RAM}:{element_name}")

        # TypeCode
        SubElement(root, f"{RAM}:TypeCode").text = self.payment_means_code.value()

        # PayerPartyDebtorFinancialAccount
        if self.payer_party_debtor_financial_account:
            root.append(self.payer_party_debtor_financial_account.to_xml("PayerPartyDebtorFinancialAccount", profile))

        # PayeePartyCreditorFinancialAccount
        if self.payee_party_creditor_financial_account:
            root.append(
                self.payee_party_creditor_financial_account.to_xml("PayeePartyCreditorFinancialAccount", profile))

        return root
