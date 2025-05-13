from typing import Optional, override
from xml.etree.ElementTree import Element

from pydantic import Field

from .InvoiceProfile import InvoiceProfile
from .ReferencedDocument import ReferencedDocument
from .SupplyChainEvent import SupplyChainEvent
from .TradeParty import TradeParty
from .XMLBaseModel import XMLBaseModel
from .namespaces import RAM


class HeaderTradeDelivery(XMLBaseModel):
    ship_to_trade_party: Optional[TradeParty] = Field(default=None)
    actual_delivery_supply_chain_event: Optional[SupplyChainEvent] = Field(default=None)
    despatch_advice_referenced_document: Optional[ReferencedDocument] = Field(default=None)

    @override
    def to_xml(self, element_name: str, profile: InvoiceProfile) -> Element:
        root = Element(f"{RAM}:{element_name}")

        if profile != InvoiceProfile.MINIMUM:
            # ShipToTradeParty
            if self.ship_to_trade_party:
                root.append(self.ship_to_trade_party.to_xml("ShipToTradeParty", profile))

            # ActualDeliverySupplyChainEvent
            if self.actual_delivery_supply_chain_event:
                root.append(self.actual_delivery_supply_chain_event.to_xml("ActualDeliverySupplyChainEvent", profile))

            # DespatchAdviceReferencedDocument
            if self.despatch_advice_referenced_document:
                root.append(
                    self.despatch_advice_referenced_document.to_xml("DespatchAdviceReferencedDocument", profile))

        return root
