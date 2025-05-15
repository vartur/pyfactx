from typing import Optional, override
from lxml import etree as ET

from pydantic import Field

from .InvoiceProfile import InvoiceProfile
from .ProductCharacteristic import ProductCharacteristic
from .ProductClassification import ProductClassification
from .TradeCountry import TradeCountry
from .XMLBaseModel import XMLBaseModel
from .namespaces import NAMESPACES, RAM


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
    def to_xml(self, element_name: str, profile: InvoiceProfile) -> ET.Element:
        root = ET.Element(f"{{{NAMESPACES[RAM]}}}{element_name}")

        # GlobalID
        if self.global_id:
            ET.SubElement(root, f"{{{NAMESPACES[RAM]}}}GlobalID").text = self.global_id

        if profile >= InvoiceProfile.EN16931:
            # SellerAssignedID
            if self.seller_assigned_id:
                ET.SubElement(root, f"{{{NAMESPACES[RAM]}}}SellerAssignedID").text = self.seller_assigned_id

            # BuyerAssignedID
            if self.buyer_assigned_id:
                ET.SubElement(root, f"{{{NAMESPACES[RAM]}}}BuyerAssignedID").text = self.buyer_assigned_id

        # Name
        ET.SubElement(root, f"{{{NAMESPACES[RAM]}}}Name").text = self.name

        if profile >= InvoiceProfile.EN16931:
            # Description
            if self.description:
                ET.SubElement(root, f"{{{NAMESPACES[RAM]}}}Description").text = self.description

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
