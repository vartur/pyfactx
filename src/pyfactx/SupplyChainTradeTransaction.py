from xml.etree.ElementTree import Element

from pydantic import BaseModel, Field

from .HeaderTradeAgreement import HeaderTradeAgreement
from .HeaderTradeDelivery import HeaderTradeDelivery
from .HeaderTradeSettlement import HeaderTradeSettlement
from .InvoiceProfile import InvoiceProfile
from .namespaces import RSM

class SupplyChainTradeTransaction(BaseModel):
    applicable_header_trade_agreement: HeaderTradeAgreement = Field(...)
    applicable_header_trade_delivery: HeaderTradeDelivery = Field(...)
    applicable_header_trade_settlement: HeaderTradeSettlement = Field(...)

    def to_xml(self, element_name: str, profile: InvoiceProfile) -> Element:
        root = Element(f"{RSM}:{element_name}")

        # ApplicableHeaderTradeAgreement
        root.append(self.applicable_header_trade_agreement.to_xml("ApplicableHeaderTradeAgreement", profile))

        # ApplicableHeaderTradeDelivery
        root.append(self.applicable_header_trade_delivery.to_xml("ApplicableHeaderTradeDelivery", profile))

        # ApplicableHeaderTradeSettlement
        root.append(self.applicable_header_trade_settlement.to_xml("ApplicableHeaderTradeSettlement", profile))

        return root
