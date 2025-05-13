from typing import Optional
from xml.etree.ElementTree import Element, SubElement

from pydantic import BaseModel, Field

from .AllowanceChargeReasonCode import AllowanceChargeReasonCode
from .Indicator import Indicator
from .InvoiceProfile import InvoiceProfile
from .TradeTax import TradeTax
from .namespaces import RAM


class TradeAllowanceCharge(BaseModel):
    charge_indicator: Indicator = Field(...)
    calculation_percent: Optional[float] = Field(default=None)
    basis_amount: Optional[float] = Field(default=None)
    actual_amount: float = Field(...)
    reason_code: Optional[AllowanceChargeReasonCode] = Field(default=None)
    reason: Optional[str] = Field(default=None)
    category_trade_tax: TradeTax = Field(...)

    def to_xml(self, element_name: str, profile: InvoiceProfile) -> Element:
        root = Element(f"{RAM}:{element_name}")

        # ChargeIndicator
        root.append(self.charge_indicator.to_xml("ChargeIndicator", profile))

        # CalculationPercent
        if self.calculation_percent:
            SubElement(root, f"{RAM}:CalculationPercent").text = str(self.calculation_percent)

        # BasisAmount
        if self.basis_amount:
            SubElement(root, f"{RAM}:BasisAmount").text = str(self.basis_amount)

        # ActualAmount
        SubElement(root, f"{RAM}:ActualAmount").text = str(self.actual_amount)

        # ReasonCode
        if self.reason_code:
            SubElement(root, f"{RAM}:ReasonCode").text = self.reason_code.value

        # Reason
        if self.reason:
            SubElement(root, f"{RAM}:Reason").text = self.reason

        # CategoryTradeTax
        root.append(self.category_trade_tax.to_xml("CategoryTradeTax", profile))

        return root
