from typing import Optional, ClassVar
from lxml import etree as ET
from pydantic import Field, model_validator, ConfigDict
from typing_extensions import override

from .InvoiceProfile import InvoiceProfile
from .ProcuringProject import ProcuringProject
from .ReferencedDocument import ReferencedDocument
from .TradeParty import TradeParty
from .XMLBaseModel import XMLBaseModel
from .namespaces import NAMESPACES, RAM


class HeaderTradeAgreement(XMLBaseModel):
    """Represents the trade agreement header section of a Factur-X document."""

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        validate_assignment=True
    )

    buyer_reference: Optional[str] = Field(
        default=None,
        description="Buyer's internal reference number"
    )
    
    seller_trade_party: TradeParty = Field(
        ...,
        description="Information about the seller party"
    )
    
    buyer_trade_party: TradeParty = Field(
        ...,
        description="Information about the buyer party"
    )
    
    seller_tax_representative_trade_party: Optional[TradeParty] = Field(
        default=None,
        description="Tax representative details if applicable"
    )
    
    seller_order_referenced_document: Optional[ReferencedDocument] = Field(
        default=None,
        description="Seller's order reference document (EN16931 and above)"
    )
    
    buyer_order_referenced_document: Optional[ReferencedDocument] = Field(
        default=None,
        description="Buyer's order reference document"
    )
    
    contract_referenced_document: Optional[ReferencedDocument] = Field(
        default=None,
        description="Contract reference document"
    )
    
    additional_referenced_documents: Optional[list[ReferencedDocument]] = Field(
        default=None,
        description="Additional reference documents (EN16931 and above)"
    )
    
    specified_procuring_project: Optional[ProcuringProject] = Field(
        default=None,
        description="Project details (EN16931 and above)"
    )

    @override
    def to_xml(self, element_name: str, profile: InvoiceProfile) -> ET.Element:
        """Converts the trade agreement to XML format.
        
        Args:
            element_name (str): Name of the root XML element
            profile (InvoiceProfile): The Factur-X profile being used

        Returns:
            ET.Element: The XML element containing the trade agreement data
        """
        root = ET.Element(f"{{{NAMESPACES[RAM]}}}{element_name}")

        # BuyerReference (optional)
        if self.buyer_reference:
            buyer_ref = ET.SubElement(root, f"{{{NAMESPACES[RAM]}}}BuyerReference")
            buyer_ref.text = self.buyer_reference

        # SellerTradeParty (required)
        seller_party = self.seller_trade_party.to_xml("SellerTradeParty", profile)
        root.append(seller_party)

        # BuyerTradeParty (required)
        buyer_party = self.buyer_trade_party.to_xml("BuyerTradeParty", profile)
        root.append(buyer_party)

        # SellerTaxRepresentativeTradeParty (optional, BASICWL and above)
        if profile >= InvoiceProfile.BASICWL and self.seller_tax_representative_trade_party:
            tax_rep = self.seller_tax_representative_trade_party.to_xml(
                "SellerTaxRepresentativeTradeParty", 
                profile
            )
            root.append(tax_rep)

        # SellerOrderReferencedDocument (optional, EN16931 and above)
        if profile >= InvoiceProfile.EN16931 and self.seller_order_referenced_document:
            seller_order = self.seller_order_referenced_document.to_xml(
                "SellerOrderReferencedDocument",
                profile
            )
            root.append(seller_order)

        # BuyerOrderReferencedDocument (optional)
        if self.buyer_order_referenced_document:
            buyer_order = self.buyer_order_referenced_document.to_xml(
                "BuyerOrderReferencedDocument",
                profile
            )
            root.append(buyer_order)

        # ContractReferencedDocument (optional, above MINIMUM)
        if profile > InvoiceProfile.MINIMUM and self.contract_referenced_document:
            contract = self.contract_referenced_document.to_xml(
                "ContractReferencedDocument",
                profile
            )
            root.append(contract)

        # AdditionalReferencedDocument (optional, EN16931 and above)
        if profile >= InvoiceProfile.EN16931 and self.additional_referenced_documents:
            for doc in self.additional_referenced_documents:
                additional = doc.to_xml("AdditionalReferencedDocument", profile)
                root.append(additional)

        # SpecifiedProcuringProject (optional, EN16931 and above)
        if profile >= InvoiceProfile.EN16931 and self.specified_procuring_project:
            project = self.specified_procuring_project.to_xml(
                "SpecifiedProcuringProject",
                profile
            )
            root.append(project)

        return root