from typing import Optional
from lxml import etree as ET

from pydantic import Field
from typing_extensions import override

from .InvoiceProfile import InvoiceProfile
from .ProcuringProject import ProcuringProject
from .ReferencedDocument import ReferencedDocument
from .TradeParty import TradeParty
from .XMLBaseModel import XMLBaseModel
from .namespaces import NAMESPACES, RAM


class HeaderTradeAgreement(XMLBaseModel):
    buyer_reference: Optional[str] = Field(default=None)
    seller_trade_party: TradeParty = Field(...)
    buyer_trade_party: TradeParty = Field(...)
    seller_tax_representative_trade_party: Optional[TradeParty] = Field(default=None)
    seller_order_referenced_document: Optional[ReferencedDocument] = Field(default=None)  # From EN16931
    buyer_order_referenced_document: Optional[ReferencedDocument] = Field(default=None)
    contract_referenced_document: Optional[ReferencedDocument] = Field(default=None)
    additional_referenced_documents: Optional[list[ReferencedDocument]] = Field(default=None)  # From EN16931
    specified_procuring_project: Optional[ProcuringProject] = Field(default=None)  # From EN16931

    @override
    def to_xml(self, element_name: str, profile: InvoiceProfile) -> ET.Element:
        root = ET.Element(f"{{{NAMESPACES[RAM]}}}{element_name}")

        # BuyerReference
        if self.buyer_reference:
            ET.SubElement(root, f"{{{NAMESPACES[RAM]}}}BuyerReference").text = self.buyer_reference

        # SellerTradeParty
        root.append(self.seller_trade_party.to_xml("SellerTradeParty", profile))

        # BuyerTradeParty
        root.append(self.buyer_trade_party.to_xml("BuyerTradeParty", profile))

        if profile >= InvoiceProfile.BASICWL:
            # SellerTaxRepresentativeTradeParty
            if self.seller_tax_representative_trade_party:
                root.append(
                    self.seller_tax_representative_trade_party.to_xml("SellerTaxRepresentativeTradeParty", profile))

        if profile >= InvoiceProfile.EN16931:
            # SellerOrderReferencedDocument
            if self.seller_order_referenced_document:
                root.append(self.seller_order_referenced_document.to_xml("SellerOrderReferencedDocument", profile))

        # BuyerOrderReferencedDocument
        if self.buyer_order_referenced_document:
            root.append(self.buyer_order_referenced_document.to_xml("BuyerOrderReferencedDocument", profile))

        if profile != InvoiceProfile.MINIMUM:
            # ContractReferencedDocument
            if self.contract_referenced_document:
                root.append(self.contract_referenced_document.to_xml("ContractReferencedDocument", profile))

        if profile >= InvoiceProfile.EN16931:
            # AdditionalReferencedDocument
            if self.additional_referenced_documents:
                for doc in self.additional_referenced_documents:
                    root.append(doc.to_xml("AdditionalReferencedDocument", profile))

            # SpecifiedProcuringProject
            if self.specified_procuring_project:
                root.append(self.specified_procuring_project.to_xml("SpecifiedProcuringProject", profile))

        return root
