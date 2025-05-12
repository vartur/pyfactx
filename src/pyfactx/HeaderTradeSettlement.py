from typing import Optional

from pydantic import BaseModel, Field

from .InvoiceProfile import InvoiceProfile
from .TradeParty import TradeParty
from .TradeSettlementHeaderMonetarySummation import TradeSettlementHeaderMonetarySummation
from .TradeSettlementPaymentMeans import TradeSettlementPaymentMeans
from .TradeTax import TradeTax


class HeaderTradeSettlement(BaseModel):
    creditor_reference_id: Optional[str] = Field(default=None)
    payment_reference: Optional[str] = Field(default=None)
    tax_currency_code: Optional[str] = Field(default=None)
    invoice_currency_code: str = Field(...)
    payee_trade_party: Optional[TradeParty] = Field(default=None)
    specified_trade_settlement_payment_means: Optional[list[TradeSettlementPaymentMeans]] = Field(default=None)
    applicable_trade_tax: list[TradeTax] = Field(...)
    specified_trade_settlement_header_monetary_summation: TradeSettlementHeaderMonetarySummation = Field(...)

    def to_xml(self, profile: InvoiceProfile = InvoiceProfile.MINIMUM):
        if profile == InvoiceProfile.MINIMUM:
            return f'''<ram:ApplicableHeaderTradeSettlement>
                            <ram:InvoiceCurrencyCode>{self.invoice_currency_code}</ram:InvoiceCurrencyCode>
                            {self.specified_trade_settlement_header_monetary_summation.to_xml()}
                        </ram:ApplicableHeaderTradeSettlement>'''

        xml_string = "<ram:ApplicableHeaderTradeSettlement>"



        xml_string += "</ram:ApplicableHeaderTradeSettlement>"
        return xml_string