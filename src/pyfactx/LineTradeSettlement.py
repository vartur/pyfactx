from typing import Optional, override
from xml.etree.ElementTree import Element

from pydantic import Field

from .InvoiceProfile import InvoiceProfile
from .SpecifiedPeriod import SpecifiedPeriod
from .TradeAllowanceCharge import TradeAllowanceCharge
from .TradeSettlementLineMonetarySummation import TradeSettlementLineMonetarySummation
from .TradeTax import TradeTax
from .XMLBaseModel import XMLBaseModel
from .namespaces import RAM


class LineTradeSettlement(XMLBaseModel):
    applicable_trade_tax: TradeTax = Field(...)
    billing_specified_period: Optional[SpecifiedPeriod] = Field(default=None)
    specified_trade_allowance_charges: Optional[list[TradeAllowanceCharge]] = Field(default=None)
    specified_trade_settlement_line_monetary_summation: TradeSettlementLineMonetarySummation = Field(...)

    @override
    def to_xml(self, element_name: str, profile: InvoiceProfile) -> Element:
        root = Element(f"{RAM}:{element_name}")

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

        return root
