from typing import Optional, override
from lxml import etree as ET

from pydantic import Field

from .namespaces import NAMESPACES, RAM
from .InvoiceProfile import InvoiceProfile
from .TradeAllowanceCharge import TradeAllowanceCharge
from .UnitCode import UnitCode
from .XMLBaseModel import XMLBaseModel


class TradePrice(XMLBaseModel):
    charge_amount: float = Field(...)
    quantity: Optional[float] = Field(default=None)
    unit: Optional[UnitCode] = Field(default=None)
    applied_trade_allowance_charge: Optional[TradeAllowanceCharge] = Field(default=None)

    @override
    def to_xml(self, element_name: str, profile: InvoiceProfile) -> ET.Element:
        root = ET.Element(f"{{{NAMESPACES[RAM]}}}{element_name}")

        # ChargeAmount
        ET.SubElement(root, f"{{{NAMESPACES[RAM]}}}ChargeAmount").text = str(self.charge_amount)

        # BasisQuantity
        if self.quantity:
            attrib = {"unitCode": self.unit} if self.unit else {}
            ET.SubElement(root, f"{{{NAMESPACES[RAM]}}}BasisQuantity", attrib=attrib).text = str(self.quantity)

        # AppliedTradeAllowanceCharge
        if self.applied_trade_allowance_charge:
            root.append(self.applied_trade_allowance_charge.to_xml("AppliedTradeAllowanceCharge", profile))

        return root
