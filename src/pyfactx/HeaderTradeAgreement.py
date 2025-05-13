from typing import Optional
from xml.etree.ElementTree import Element, SubElement

from pydantic import Field
from typing_extensions import override

from .InvoiceProfile import InvoiceProfile
from .ReferencedDocument import ReferencedDocument
from .TradeParty import TradeParty
from .XMLBaseModel import XMLBaseModel
from .namespaces import RAM


class HeaderTradeAgreement(XMLBaseModel):
    buyer_reference: Optional[str] = Field(default=None)
    seller_trade_party: TradeParty = Field(...)
    buyer_trade_party: TradeParty = Field(...)
    seller_tax_representative_trade_party: Optional[TradeParty] = Field(default=None)
    buyer_order_referenced_document: Optional[ReferencedDocument] = Field(default=None)
    contract_referenced_document: Optional[ReferencedDocument] = Field(default=None)

    @override
    def to_xml(self, element_name: str, profile: InvoiceProfile) -> Element:
        root = Element(f"{RAM}:{element_name}")

        # BuyerReference
        if self.buyer_reference:
            SubElement(root, f"{RAM}:BuyerReference").text = self.buyer_reference

        # SellerTradeParty
        root.append(self.seller_trade_party.to_xml("SellerTradeParty", profile))

        # BuyerTradeParty
        root.append(self.buyer_trade_party.to_xml("BuyerTradeParty", profile))

        if profile != InvoiceProfile.MINIMUM:
            # SellerTaxRepresentativeTradeParty
            if self.seller_tax_representative_trade_party:
                root.append(
                    self.seller_tax_representative_trade_party.to_xml("SellerTaxRepresentativeTradeParty", profile))

        # BuyerOrderReferencedDocument
        if self.buyer_order_referenced_document:
            root.append(self.buyer_order_referenced_document.to_xml("BuyerOrderReferencedDocument", profile))

        if profile != InvoiceProfile.MINIMUM:
            # ContractReferencedDocument
            if self.contract_referenced_document:
                root.append(self.contract_referenced_document.to_xml("ContractReferencedDocument", profile))

        return root
