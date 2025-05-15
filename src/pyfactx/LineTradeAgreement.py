from typing import Optional, override
from xml.etree.ElementTree import Element

from pydantic import Field

from .InvoiceProfile import InvoiceProfile
from .ReferencedDocument import ReferencedDocument
from .TradePrice import TradePrice
from .XMLBaseModel import XMLBaseModel
from .namespaces import RAM


class LineTradeAgreement(XMLBaseModel):
    buyer_order_referenced_document: Optional[ReferencedDocument] = Field(default=None)  # From EN16931
    gross_price_product_trade_price: Optional[TradePrice] = Field(default=None)
    net_price_product_trade_price: TradePrice = Field(...)

    @override
    def to_xml(self, element_name: str, profile: InvoiceProfile) -> Element:
        root = Element(f"{RAM}:{element_name}")

        if profile >= InvoiceProfile.EN16931:
            # BuyerOrderReferencedDocument
            if self.buyer_order_referenced_document:
                root.append(self.buyer_order_referenced_document.to_xml("BuyerOrderReferencedDocument", profile))

        # GrossPriceProductTradePrice
        if self.gross_price_product_trade_price:
            root.append(self.gross_price_product_trade_price.to_xml("GrossPriceProductTradePrice", profile))

        # NetPriceProductTradePrice
        root.append(self.net_price_product_trade_price.to_xml("NetPriceProductTradePrice", profile))

        return root
