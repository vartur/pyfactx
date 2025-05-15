from typing import Optional, override
from lxml import etree as ET

from pydantic import Field

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
    applicable_trade_tax: TradeTax = Field(...)
    billing_specified_period: Optional[SpecifiedPeriod] = Field(default=None)
    specified_trade_allowance_charges: Optional[list[TradeAllowanceCharge]] = Field(default=None)
    specified_trade_settlement_line_monetary_summation: TradeSettlementLineMonetarySummation = Field(...)
    additional_referenced_document: Optional[ReferencedDocument] = Field(default=None)  # From EN16931
    receivable_specified_trade_accounting_account: Optional[TradeAccountingAccount] = Field(
        default=None)  # From EN16931

    @override
    def to_xml(self, element_name: str, profile: InvoiceProfile) -> ET.Element:
        root = ET.Element(f"{{{NAMESPACES[RAM]}}}{element_name}")

        # ApplicableTradeTax
        root.append(self.applicable_trade_tax.to_xml("ApplicableTradeTax", profile))

        # BillingSpecifiedPeriod
        if self.billing_specified_period:
            root.append(self.billing_specified_period.to_xml("BillingSpecifiedPeriod", profile))

        # SpecifiedTradeAllowanceCharges
        if self.specified_trade_allowance_charges:
            for trade_allowance in self.specified_trade_allowance_charges:
                root.append(trade_allowance.to_xml("SpecifiedTradeAllowanceCharge", profile))

        # SpecifiedTradeSettlementLineMonetarySummation
        root.append(self.specified_trade_settlement_line_monetary_summation.to_xml(
            "SpecifiedTradeSettlementLineMonetarySummation", profile))

        if profile >= InvoiceProfile.EN16931:
            # AdditionalReferencedDocument
            if self.additional_referenced_document:
                root.append(self.additional_referenced_document.to_xml("AdditionalReferencedDocument", profile))

            # ReceivableSpecifiedTradeAccountingAccount
            if self.receivable_specified_trade_accounting_account:
                root.append(self.receivable_specified_trade_accounting_account.to_xml(
                    "ReceivableSpecifiedTradeAccountingAccount", profile))

        return root
