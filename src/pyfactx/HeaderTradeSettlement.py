from typing import Optional
from xml.etree.ElementTree import Element, SubElement

from pydantic import BaseModel, Field

from .InvoiceProfile import InvoiceProfile
from .ReferencedDocument import ReferencedDocument
from .SpecifiedPeriod import SpecifiedPeriod
from .TradeAccountingAccount import TradeAccountingAccount
from .TradeAllowanceCharge import TradeAllowanceCharge
from .TradeParty import TradeParty
from .TradePaymentTerms import TradePaymentTerms
from .TradeSettlementHeaderMonetarySummation import TradeSettlementHeaderMonetarySummation
from .TradeSettlementPaymentMeans import TradeSettlementPaymentMeans
from .TradeTax import TradeTax
from .namespaces import RAM


class HeaderTradeSettlement(BaseModel):
    creditor_reference_id: Optional[str] = Field(default=None)
    payment_reference: Optional[str] = Field(default=None)
    tax_currency_code: Optional[str] = Field(default=None)
    invoice_currency_code: str = Field(...)
    payee_trade_party: Optional[TradeParty] = Field(default=None)
    specified_trade_settlement_payment_means: Optional[list[TradeSettlementPaymentMeans]] = Field(default=None)
    applicable_trade_tax: Optional[list[TradeTax]] = Field(default=None)
    billing_specified_period: Optional[SpecifiedPeriod] = Field(default=None)
    specified_trade_allowance_charge: Optional[list[TradeAllowanceCharge]] = Field(default=None)
    specified_trade_payment_terms: Optional[TradePaymentTerms] = Field(default=None)
    specified_trade_settlement_header_monetary_summation: TradeSettlementHeaderMonetarySummation = Field(...)
    invoice_referenced_documents: Optional[list[ReferencedDocument]] = Field(default=None)
    receivable_specified_trade_accounting_account: Optional[TradeAccountingAccount] = Field(default=None)

    def to_xml(self, element_name: str, profile: InvoiceProfile = InvoiceProfile.MINIMUM) -> Element:
        root = Element(f"{RAM}:{element_name}")

        if profile != InvoiceProfile.MINIMUM:
            # CreditorReferenceID
            if self.creditor_reference_id:
                SubElement(root, f"{RAM}:CreditorReferenceID").text = self.creditor_reference_id

            # PaymentReference
            if self.payment_reference:
                SubElement(root, f"{RAM}:PaymentReference").text = self.payment_reference

            # TaxCurrencyCode
            if self.tax_currency_code:
                SubElement(root, f"{RAM}:TaxCurrencyCode").text = self.tax_currency_code

        # InvoiceCurrencyCode
        SubElement(root, f"{RAM}:InvoiceCurrencyCode").text = self.invoice_currency_code

        if profile != InvoiceProfile.MINIMUM:
            # PayeeTradeParty
            if self.payee_trade_party:
                root.append(self.payee_trade_party.to_xml("PayeeTradeParty", profile))

            # SpecifiedTradeSettlementPaymentMeans
            if self.specified_trade_settlement_payment_means:
                for payment_means in self.specified_trade_settlement_payment_means:
                    root.append(payment_means.to_xml("SpecifiedTradeSettlementPaymentMeans", profile))

            # ApplicableTradeTax
            if self.applicable_trade_tax:
                for trade_tax in self.applicable_trade_tax:
                    root.append(trade_tax.to_xml("ApplicableTradeTax", profile))

            # BillingSpecifiedPeriod
            if self.billing_specified_period:
                root.append(self.billing_specified_period.to_xml("BillingSpecifiedPeriod", profile))

            # SpecifiedTradeAllowanceCharge
            if self.specified_trade_allowance_charge:
                for trade_allowance_charge in self.specified_trade_allowance_charge:
                    root.append(trade_allowance_charge.to_xml("SpecifiedTradeAllowanceCharge", profile))

            # SpecifiedTradePaymentTerms
            if self.specified_trade_payment_terms:
                root.append(self.specified_trade_payment_terms.to_xml("SpecifiedTradePaymentTerms"))

        # SpecifiedTradeSettlementHeaderMonetarySummation
        root.append(self.specified_trade_settlement_header_monetary_summation.to_xml(
            "SpecifiedTradeSettlementHeaderMonetarySummation",
            tax_currency_code=(self.tax_currency_code if self.tax_currency_code else self.invoice_currency_code),
            profile=profile))

        if profile != InvoiceProfile.MINIMUM:
            # InvoiceReferencedDocument
            if self.invoice_referenced_documents:
                for ref_doc in self.invoice_referenced_documents:
                    root.append(ref_doc.to_xml("InvoiceReferencedDocument", profile))

            # ReceivableSpecifiedTradeAccountingAccount
            if self.receivable_specified_trade_accounting_account:
                root.append(self.receivable_specified_trade_accounting_account.to_xml(
                    "ReceivableSpecifiedTradeAccountingAccount", profile))

        return root
