from typing import Optional
from xml.etree.ElementTree import Element, SubElement

from pydantic import BaseModel, Field

from .InvoiceProfile import InvoiceProfile
from .TradeAllowanceCharge import TradeAllowanceCharge
from .UnitCode import UnitCode
from namespaces import RAM


class TradePrice(BaseModel):
    charge_amount: float = Field(...)
    quantity: Optional[float] = Field(default=None)
    unit: Optional[UnitCode] = Field(default=None)
    applied_trade_allowance_charge: Optional[TradeAllowanceCharge] = Field(default=None)

    def to_xml(self, element_name: str, profile: InvoiceProfile) -> Element:
        root = Element(f"{RAM}:{element_name}")

        # ChargeAmount
        SubElement(root, f"{RAM}:ChargeAmount").text = str(self.charge_amount)

        # BasisQuantity
        if self.quantity:
            attrib = {"unitCode": self.unit} if self.unit else {}
            SubElement(root, f"{RAM}:BasisQuantity", attrib=attrib).text = str(self.quantity)

        # AppliedTradeAllowanceCharge
        if self.applied_trade_allowance_charge:
            root.append(self.applied_trade_allowance_charge.to_xml("AppliedTradeAllowanceCharge", profile))

        return root
