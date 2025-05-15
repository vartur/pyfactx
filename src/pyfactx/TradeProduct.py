from typing import Optional, override
from xml.etree.ElementTree import Element, SubElement

from pydantic import Field

from .InvoiceProfile import InvoiceProfile
from .ProductCharacteristic import ProductCharacteristic
from .ProductClassification import ProductClassification
from .TradeCountry import TradeCountry
from .XMLBaseModel import XMLBaseModel
from .namespaces import RAM


class TradeProduct(XMLBaseModel):
    global_id: Optional[str] = Field(default=None)
    seller_assigned_id: Optional[str] = Field(default=None)  # From EN16931
    buyer_assigned_id: Optional[str] = Field(default=None)  # From EN16931
    name: str = Field(...)
    description: Optional[str] = Field(default=None)  # From EN16931
    applicable_product_characteristics: Optional[list[ProductCharacteristic]] = Field(default=None)  # From EN16931
    designated_product_classifications: Optional[list[ProductClassification]] = Field(default=None)  # From EN16931
    origin_trade_country: Optional[TradeCountry] = Field(default=None)  # From EN16931

    @override
    def to_xml(self, element_name: str, profile: InvoiceProfile) -> Element:
        root = Element(f"{RAM}:{element_name}")

        # GlobalID
        if self.global_id:
            SubElement(root, f"{RAM}:GlobalID").text = self.global_id

        if profile >= InvoiceProfile.EN16931:
            # SellerAssignedID
            if self.seller_assigned_id:
                SubElement(root, f"{RAM}:SellerAssignedID").text = self.seller_assigned_id

            # BuyerAssignedID
            if self.buyer_assigned_id:
                SubElement(root, f"{RAM}:BuyerAssignedID").text = self.buyer_assigned_id

        # Name
        SubElement(root, f"{RAM}:Name").text = self.name

        if profile >= InvoiceProfile.EN16931:
            # Description
            if self.description:
                SubElement(root, f"{RAM}:Description").text = self.description

            # ApplicableProductCharacteristic
            if self.applicable_product_characteristics:
                for characteristic in self.applicable_product_characteristics:
                    root.append(characteristic.to_xml("ApplicableProductCharacteristic", profile))

            # DesignatedProductClassification
            if self.designated_product_classifications:
                for classification in self.designated_product_classifications:
                    root.append(classification.to_xml("DesignatedProductClassification", profile))

            # OriginTradeCountry
            if self.origin_trade_country:
                root.append(self.origin_trade_country.to_xml("OriginTradeCountry", profile))

        return root
