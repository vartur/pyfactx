from typing import Optional, override
from lxml import etree as ET

from pydantic import Field

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
from .XMLBaseModel import XMLBaseModel
from .namespaces import NAMESPACES, RAM


class HeaderTradeSettlement(XMLBaseModel):
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

    @override
    def to_xml(self, element_name: str, profile: InvoiceProfile) -> ET.Element:
        root = ET.Element(f"{{{NAMESPACES[RAM]}}}{element_name}")

        if profile >= InvoiceProfile.BASICWL:
            # CreditorReferenceID
            if self.creditor_reference_id:
                ET.SubElement(root, f"{{{NAMESPACES[RAM]}}}CreditorReferenceID").text = self.creditor_reference_id

            # PaymentReference
            if self.payment_reference:
                ET.SubElement(root, f"{{{NAMESPACES[RAM]}}}PaymentReference").text = self.payment_reference

            # TaxCurrencyCode
            if self.tax_currency_code:
                ET.SubElement(root, f"{{{NAMESPACES[RAM]}}}TaxCurrencyCode").text = self.tax_currency_code

        # InvoiceCurrencyCode
        ET.SubElement(root, f"{{{NAMESPACES[RAM]}}}InvoiceCurrencyCode").text = self.invoice_currency_code

        if profile >= InvoiceProfile.BASICWL:
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
                root.append(self.specified_trade_payment_terms.to_xml("SpecifiedTradePaymentTerms", profile))

        # SpecifiedTradeSettlementHeaderMonetarySummation
        root.append(self.specified_trade_settlement_header_monetary_summation.to_xml(
            "SpecifiedTradeSettlementHeaderMonetarySummation", profile))

        if profile >= InvoiceProfile.BASICWL:
            # InvoiceReferencedDocument
            if self.invoice_referenced_documents:
                for ref_doc in self.invoice_referenced_documents:
                    root.append(ref_doc.to_xml("InvoiceReferencedDocument", profile))

            # ReceivableSpecifiedTradeAccountingAccount
            if self.receivable_specified_trade_accounting_account:
                root.append(self.receivable_specified_trade_accounting_account.to_xml(
                    "ReceivableSpecifiedTradeAccountingAccount", profile))

        return root
