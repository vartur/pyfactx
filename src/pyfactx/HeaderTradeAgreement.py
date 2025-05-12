from typing import Optional

from pydantic import BaseModel, Field

from .InvoiceProfile import InvoiceProfile
from .TradeParty import TradeParty


class HeaderTradeAgreement(BaseModel):
    buyer_reference: Optional[str] = Field(default=None)
    seller_trade_party: TradeParty = Field(...)
    buyer_trade_party: TradeParty = Field(...)
    seller_tax_representative_trade_party: Optional[TradeParty] = Field(default=None)
    buyer_order_referenced_document: Optional[str] = Field(default=None)
    contract_referenced_document: Optional[str] = Field(default=None)

    def to_xml(self, profile: InvoiceProfile = InvoiceProfile.MINIMUM):
        xml_string = "<ram:ApplicableHeaderTradeAgreement>"

        if self.buyer_reference is not None:
            xml_string += f"<ram:BuyerReference>{self.buyer_reference}</ram:BuyerReference>"

        xml_string += f"<ram:SellerTradeParty>{self.seller_trade_party.to_xml(profile)}</ram:SellerTradeParty>"
        xml_string += f"<ram:BuyerTradeParty>{self.buyer_trade_party.to_xml(profile)}</ram:BuyerTradeParty>"

        if profile != InvoiceProfile.MINIMUM:
            if self.seller_tax_representative_trade_party is not None:
                xml_string += f"<ram:SellerTaxRepresentativeTradeParty>{self.seller_tax_representative_trade_party.to_xml(profile)}</ram:SellerTaxRepresentativeTradeParty>"

        if self.buyer_order_referenced_document is not None:
            xml_string += f'''<ram:BuyerOrderReferencedDocument>
                                    <ram:IssuerAssignedID>{self.buyer_order_referenced_document}</ram:IssuerAssignedID>
                                </ram:BuyerOrderReferencedDocument>'''

        if profile != InvoiceProfile.MINIMUM:
            if self.contract_referenced_document is not None:
                xml_string += f'''<ram:ContractReferencedDocument>
                                                    <ram:IssuerAssignedID>{self.contract_referenced_document}</ram:IssuerAssignedID>
                                                </ram:ContractReferencedDocument>'''

        xml_string += "</ram:ApplicableHeaderTradeAgreement>"
        return xml_string
