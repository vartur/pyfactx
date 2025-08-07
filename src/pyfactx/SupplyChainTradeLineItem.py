from decimal import Decimal
from lxml import etree as ET
from typing import Optional

from pydantic import Field, ConfigDict
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
    """Represents a supply chain trade line item in the invoice.

    This class models individual line items in a trade transaction according to
    the Factur-X standard, combining document, product, agreement, delivery,
    and settlement information.

    Attributes:
        associated_document_line_document: Document information for the line item
        specified_trade_product: Product information
        specified_line_trade_agreement: Trade agreement details
        specified_line_trade_delivery: Delivery information
        specified_line_trade_settlement: Settlement details

    Examples:
        >>> line_item = SupplyChainTradeLineItem(
        ...     associated_document_line_document=DocumentLineDocument(...),
        ...     specified_trade_product=TradeProduct(...),
        ...     specified_line_trade_agreement=LineTradeAgreement(...),
        ...     specified_line_trade_delivery=LineTradeDelivery(...),
        ...     specified_line_trade_settlement=LineTradeSettlement(...)
        ... )
    """

    model_config = ConfigDict(
        validate_assignment=True,
        str_strip_whitespace=True
    )

    associated_document_line_document: DocumentLineDocument = Field(
        ...,
        description="Document information for the line item"
    )

    specified_trade_product: TradeProduct = Field(
        ...,
        description="Product information"
    )

    specified_line_trade_agreement: LineTradeAgreement = Field(
        ...,
        description="Trade agreement details"
    )

    specified_line_trade_delivery: LineTradeDelivery = Field(
        ...,
        description="Delivery information"
    )

    specified_line_trade_settlement: LineTradeSettlement = Field(
        ...,
        description="Settlement details"
    )

    @override
    def to_xml(self, element_name: str, profile: InvoiceProfile) -> ET.Element:
        """Converts the line item to XML format.

        Creates an XML element representing the line item according to
        the Factur-X specification and the specified profile.

        Args:
            element_name: Name of the root XML element
            profile: Factur-X profile determining available fields

        Returns:
            ET.Element: XML element containing the line item data
        """
        root = ET.Element(f"{{{NAMESPACES[RAM]}}}{element_name}")

        # AssociatedDocumentLineDocument
        root.append(
            self.associated_document_line_document.to_xml(
                "AssociatedDocumentLineDocument",
                profile
            )
        )

        # SpecifiedTradeProduct
        root.append(
            self.specified_trade_product.to_xml(
                "SpecifiedTradeProduct",
                profile
            )
        )

        # SpecifiedLineTradeAgreement
        root.append(
            self.specified_line_trade_agreement.to_xml(
                "SpecifiedLineTradeAgreement",
                profile
            )
        )

        # SpecifiedLineTradeDelivery
        root.append(
            self.specified_line_trade_delivery.to_xml(
                "SpecifiedLineTradeDelivery",
                profile
            )
        )

        # SpecifiedLineTradeSettlement
        root.append(
            self.specified_line_trade_settlement.to_xml(
                "SpecifiedLineTradeSettlement",
                profile
            )
        )

        return root

    def __str__(self) -> str:
        """Returns a string representation of the line item.

        Returns:
            str: Line item in readable format
        """
        return (
            f"Line {self.associated_document_line_document.line_id}: "
            f"{self.specified_trade_product.name or 'Unnamed product'}"
        )

    def get_product_details(self) -> dict:
        """Gets a dictionary of product details.

        Returns:
            dict: Dictionary containing product information
        """
        return {
            "id": self.specified_trade_product.id,
            "name": self.specified_trade_product.name,
            "description": self.specified_trade_product.description,
        }