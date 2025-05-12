from pydantic import BaseModel, Field
from .HeaderTradeAgreement import HeaderTradeAgreement
from .HeaderTradeDelivery import HeaderTradeDelivery
from .HeaderTradeSettlement import HeaderTradeSettlement


class SupplyChainTradeTransaction(BaseModel):
    applicable_header_trade_agreement: HeaderTradeAgreement = Field(...)
    applicable_header_trade_delivery: HeaderTradeDelivery = Field(...)
    applicable_header_trade_settlement: HeaderTradeSettlement = Field(...)

    def to_xml(self):
        return f'''<rsm:SupplyChainTradeTransaction>
                {self.applicable_header_trade_agreement.to_xml()}
                {self.applicable_header_trade_delivery.to_xml()}
                {self.applicable_header_trade_settlement.to_xml()}
                </rsm:SupplyChainTradeTransaction>'''
