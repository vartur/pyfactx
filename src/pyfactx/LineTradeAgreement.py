from typing import Optional, override
from xml.etree.ElementTree import Element

from pydantic import Field

from .InvoiceProfile import InvoiceProfile
from .TradePrice import TradePrice
from .XMLBaseModel import XMLBaseModel
from .namespaces import RAM


class LineTradeAgreement(XMLBaseModel):
    gross_price_product_trade_price: Optional[TradePrice] = Field(default=None)
    net_price_product_trade_price: TradePrice = Field(...)

    @override
    def to_xml(self, element_name: str, profile: InvoiceProfile) -> Element:
        root = Element(f"{RAM}:{element_name}")

        # GrossPriceProductTradePrice
        if self.gross_price_product_trade_price:
            root.append(self.gross_price_product_trade_price.to_xml("GrossPriceProductTradePrice", profile))

        # NetPriceProductTradePrice
        root.append(self.net_price_product_trade_price.to_xml("NetPriceProductTradePrice", profile))

        return root
