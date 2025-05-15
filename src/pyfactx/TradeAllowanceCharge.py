from typing import Optional, override
from lxml import etree as ET

from pydantic import Field

from .AllowanceChargeReasonCode import AllowanceChargeReasonCode
from .Indicator import Indicator
from .InvoiceProfile import InvoiceProfile
from .TradeTax import TradeTax
from .XMLBaseModel import XMLBaseModel
from .namespaces import NAMESPACES, RAM


class TradeAllowanceCharge(XMLBaseModel):
    charge_indicator: Indicator = Field(...)
    calculation_percent: Optional[float] = Field(default=None)
    basis_amount: Optional[float] = Field(default=None)
    actual_amount: float = Field(...)
    reason_code: Optional[AllowanceChargeReasonCode] = Field(default=None)
    reason: Optional[str] = Field(default=None)
    category_trade_tax: TradeTax = Field(...)

    @override
    def to_xml(self, element_name: str, profile: InvoiceProfile) -> ET.Element:
        root = ET.Element(f"{{{NAMESPACES[RAM]}}}{element_name}")

        # ChargeIndicator
        root.append(self.charge_indicator.to_xml("ChargeIndicator", profile))

        # CalculationPercent
        if self.calculation_percent:
            ET.SubElement(root, f"{{{NAMESPACES[RAM]}}}CalculationPercent").text = str(self.calculation_percent)

        # BasisAmount
        if self.basis_amount:
            ET.SubElement(root, f"{{{NAMESPACES[RAM]}}}BasisAmount").text = str(self.basis_amount)

        # ActualAmount
        ET.SubElement(root, f"{{{NAMESPACES[RAM]}}}ActualAmount").text = str(self.actual_amount)

        # ReasonCode
        if self.reason_code:
            ET.SubElement(root, f"{{{NAMESPACES[RAM]}}}ReasonCode").text = self.reason_code.value

        # Reason
        if self.reason:
            ET.SubElement(root, f"{{{NAMESPACES[RAM]}}}Reason").text = self.reason

        # CategoryTradeTax
        root.append(self.category_trade_tax.to_xml("CategoryTradeTax", profile))

        return root
