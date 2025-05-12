from typing import Optional

from pydantic import BaseModel, Field

from .InvoiceProfile import InvoiceProfile
from .TradeParty import TradeParty


class HeaderTradeDelivery(BaseModel):
    ship_to_trade_party: Optional[TradeParty] = Field(default=None)
    actual_delivery_supply_chain_event: Optional[str] = Field(default=None)  # delivery date YYYYMMDD
    despatch_advice_referenced_document: Optional[str] = Field(default=None)

    def to_xml(self, profile: InvoiceProfile = InvoiceProfile.MINIMUM):
        if profile == InvoiceProfile.MINIMUM:
            return "<ram:ApplicableHeaderTradeDelivery/>"

        xml_string = "<ram:ApplicableHeaderTradeDelivery>"
        if self.ship_to_trade_party is not None:
            xml_string += f'''<ram:ShipToTradeParty>
                                {self.ship_to_trade_party.to_xml(profile)}
                                </ram:ShipToTradeParty>'''

        if self.actual_delivery_supply_chain_event:
            xml_string += f'''<ram:ActualDeliverySupplyChainEvent>
                                    <ram:OccurrenceDateTime>
                                        <udt:DateTimeString format="102">{self.actual_delivery_supply_chain_event}</udt:DateTimeString>
                                    </ram:OccurrenceDateTime>
                                </ram:ActualDeliverySupplyChainEvent>'''

        if self.despatch_advice_referenced_document is not None:
            xml_string += f'''<ram:DespatchAdviceReferencedDocument>
                                    <ram:IssuerAssignedID>{self.despatch_advice_referenced_document}</ram:IssuerAssignedID>
                                </ram:DespatchAdviceReferencedDocument>'''

        xml_string += "</ram:ApplicableHeaderTradeDelivery>"

        return xml_string
