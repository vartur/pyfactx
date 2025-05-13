from pydantic import BaseModel, Field

from .DocumentLineDocument import DocumentLineDocument
from .TradeProduct import TradeProduct


class SupplyChainTradeLineItem(BaseModel):
    associated_document_line_document: DocumentLineDocument = Field(...)
    specified_trade_product: TradeProduct = Field(...)