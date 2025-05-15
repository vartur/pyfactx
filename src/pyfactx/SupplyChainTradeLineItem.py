from lxml import etree as ET

from pydantic import Field
from typing_extensions import override

from .DocumentLineDocument import DocumentLineDocument
from .InvoiceProfile import InvoiceProfile
from .LineTradeAgreement import LineTradeAgreement
from .LineTradeDelivery import LineTradeDelivery
from .LineTradeSettlement import LineTradeSettlement
from .TradeProduct import TradeProduct
from .XMLBaseModel import XMLBaseModel
from .namespaces import NAMESPACES, RAM


class SupplyChainTradeLineItem(XMLBaseModel):
    associated_document_line_document: DocumentLineDocument = Field(...)
    specified_trade_product: TradeProduct = Field(...)
    specified_line_trade_agreement: LineTradeAgreement = Field(...)
    specified_line_trade_delivery: LineTradeDelivery = Field(...)
    specified_line_trade_settlement: LineTradeSettlement = Field(...)

    @override
    def to_xml(self, element_name: str, profile: InvoiceProfile) -> ET.Element:
        root = ET.Element(f"{{{NAMESPACES[RAM]}}}{element_name}")

        # AssociatedDocumentLineDocument
        root.append(self.associated_document_line_document.to_xml("AssociatedDocumentLineDocument", profile))

        # SpecifiedTradeProduct
        root.append(self.specified_trade_product.to_xml("SpecifiedTradeProduct", profile))

        # SpecifiedLineTradeAgreement
        root.append(self.specified_line_trade_agreement.to_xml("SpecifiedLineTradeAgreement", profile))

        # SpecifiedLineTradeDelivery
        root.append(self.specified_line_trade_delivery.to_xml("SpecifiedLineTradeDelivery", profile))

        # SpecifiedLineTradeSettlement
        root.append(self.specified_line_trade_settlement.to_xml("SpecifiedLineTradeSettlement", profile))

        return root
