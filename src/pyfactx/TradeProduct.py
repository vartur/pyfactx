from typing import Optional, override, List
from lxml import etree as ET

from pydantic import Field, field_validator, ConfigDict

from .InvoiceProfile import InvoiceProfile
from .ProductCharacteristic import ProductCharacteristic
from .ProductClassification import ProductClassification
from .TradeCountry import TradeCountry
from .XMLBaseModel import XMLBaseModel
from .namespaces import NAMESPACES, RAM


class TradeProduct(XMLBaseModel):
    """Represents a trade product according to UN/CEFACT standards.

    This class models product information including identifiers, descriptions,
    characteristics, classifications, and origin information.

    Attributes:
        global_id: Global product identifier (e.g., GTIN)
        seller_assigned_id: Product ID assigned by the seller
        buyer_assigned_id: Product ID assigned by the buyer
        name: Product name
        description: Detailed product description
        applicable_product_characteristics: List of product characteristics
        designated_product_classifications: List of product classifications
        origin_trade_country: Country of origin
    """

    model_config = ConfigDict(
        validate_assignment=True,
        strict=True
    )

    global_id: Optional[str] = Field(
        default=None,
        description="Global product identifier (e.g., GTIN)",
        max_length=50,
        pattern=r'^[A-Za-z0-9\-_]+$'
    )

    seller_assigned_id: Optional[str] = Field(
        default=None,
        description="Product ID assigned by the seller",
        max_length=50,
        pattern=r'^[A-Za-z0-9\-_]+$'
    )

    buyer_assigned_id: Optional[str] = Field(
        default=None,
        description="Product ID assigned by the buyer",
        max_length=50,
        pattern=r'^[A-Za-z0-9\-_]+$'
    )

    name: str = Field(
        ...,
        description="Product name",
        min_length=1,
        max_length=256
    )

    description: Optional[str] = Field(
        default=None,
        description="Detailed product description",
        max_length=512
    )

    applicable_product_characteristics: Optional[List[ProductCharacteristic]] = Field(
        default=None,
        description="List of product characteristics",
        max_length=100  # Reasonable limit for characteristics
    )

    designated_product_classifications: Optional[List[ProductClassification]] = Field(
        default=None,
        description="List of product classifications",
        max_length=100  # Reasonable limit for classifications
    )

    origin_trade_country: Optional[TradeCountry] = Field(
        default=None,
        description="Country of origin"
    )

    @field_validator('name')
    def validate_name(cls, v: str) -> str:
        """Validates the product name.

        Args:
            v: The name to validate

        Returns:
            str: The validated name

        Raises:
            ValueError: If the name is empty or contains only whitespace
        """
        v = v.strip()
        if not v:
            raise ValueError("Product name cannot be empty or contain only whitespace")
        return v

    @field_validator('description')
    def validate_description(cls, v: Optional[str]) -> Optional[str]:
        """Validates the product description.

        Args:
            v: The description to validate

        Returns:
            Optional[str]: The validated description

        Raises:
            ValueError: If the description is empty or contains only whitespace
        """
        if v is not None:
            v = v.strip()
            if not v:
                raise ValueError("Product description cannot be empty or contain only whitespace")
        return v

    @override
    def to_xml(self, element_name: str, profile: InvoiceProfile) -> ET.Element:
        """Converts the trade product to XML representation.

        Creates an XML element representing the product according to
        the Cross Industry Invoice (CII) XML schema.

        Args:
            element_name: The name to use for the root XML element
            profile: The invoice profile containing serialization settings

        Returns:
            ET.Element: An XML element representing the product

        Example:
            ```xml
            <ram:SpecifiedTradeProduct>
                <ram:GlobalID>12345678</ram:GlobalID>
                <ram:SellerAssignedID>PROD001</ram:SellerAssignedID>
                <ram:Name>Product Name</ram:Name>
                <ram:Description>Product Description</ram:Description>
                <!-- Additional elements based on profile -->
            </ram:SpecifiedTradeProduct>
            ```
        """
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

    def __str__(self) -> str:
        """Returns a human-readable string representation.

        Returns:
            str: Description of the trade product
        """
        parts = [f"Name: {self.name}"]
        if self.global_id:
            parts.append(f"Global ID: {self.global_id}")
        if self.seller_assigned_id:
            parts.append(f"Seller ID: {self.seller_assigned_id}")
        if self.buyer_assigned_id:
            parts.append(f"Buyer ID: {self.buyer_assigned_id}")
        if self.description:
            parts.append(f"Description: {self.description}")
        if self.origin_trade_country:
            parts.append(f"Origin: {self.origin_trade_country}")
        return " | ".join(parts)