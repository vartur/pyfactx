from lxml import etree as ET

from pydantic import Field
from typing_extensions import override, Optional

from .HeaderTradeAgreement import HeaderTradeAgreement
from .HeaderTradeDelivery import HeaderTradeDelivery
from .HeaderTradeSettlement import HeaderTradeSettlement
from .InvoiceProfile import InvoiceProfile
from .SupplyChainTradeLineItem import SupplyChainTradeLineItem
from .XMLBaseModel import XMLBaseModel
from .namespaces import NAMESPACES, RSM


class SupplyChainTradeTransaction(XMLBaseModel):
    included_supply_chain_trade_line_items: Optional[list[SupplyChainTradeLineItem]] = Field(
        default=None)  # Mandatory from BASIC
    applicable_header_trade_agreement: HeaderTradeAgreement = Field(...)
    applicable_header_trade_delivery: HeaderTradeDelivery = Field(...)
    applicable_header_trade_settlement: HeaderTradeSettlement = Field(...)

    @override
    def to_xml(self, element_name: str, profile: InvoiceProfile) -> ET.Element:
        root = ET.Element(f"{{{NAMESPACES[RSM]}}}{element_name}")

        if profile >= InvoiceProfile.BASIC:
            # IncludedSupplyChainTradeLineItems
            if self.included_supply_chain_trade_line_items:
                for line_item in self.included_supply_chain_trade_line_items:
                    root.append(line_item.to_xml("IncludedSupplyChainTradeLineItem", profile))

        # ApplicableHeaderTradeAgreement
        root.append(self.applicable_header_trade_agreement.to_xml("ApplicableHeaderTradeAgreement", profile))

        # ApplicableHeaderTradeDelivery
        root.append(self.applicable_header_trade_delivery.to_xml("ApplicableHeaderTradeDelivery", profile))

        # ApplicableHeaderTradeSettlement
        root.append(self.applicable_header_trade_settlement.to_xml("ApplicableHeaderTradeSettlement", profile))

        return root
