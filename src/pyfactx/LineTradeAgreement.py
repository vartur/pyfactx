from typing import Optional, override
from lxml import etree as ET

from pydantic import Field, field_validator, ConfigDict

from .InvoiceProfile import InvoiceProfile
from .ReferencedDocument import ReferencedDocument
from .TradePrice import TradePrice
from .XMLBaseModel import XMLBaseModel
from .namespaces import NAMESPACES, RAM


class LineTradeAgreement(XMLBaseModel):
    """Represents trade agreement details for an invoice line item.

    This class models the trade agreement information according to Factur-X standards,
    including pricing details and order references for individual line items.

    Attributes:
        buyer_order_referenced_document: Reference to the buyer's purchase order.
            Optional, only available in EN16931 and higher profiles.
        gross_price_product_trade_price: Original price before discounts or charges.
            Optional, but recommended for transparency.
        net_price_product_trade_price: Final price after all discounts and charges.
            Required for all invoice lines.

    Examples:
        >>> trade_price = TradePrice(amount=100.00)
        >>> agreement = LineTradeAgreement(
        ...     net_price_product_trade_price=trade_price,
        ...     gross_price_product_trade_price=TradePrice(amount=120.00)
        ... )
    """

    model_config = ConfigDict(
        validate_assignment=True,
        arbitrary_types_allowed=True
    )

    buyer_order_referenced_document: Optional[ReferencedDocument] = Field(
        default=None,
        description="Reference to buyer's purchase order document"
    )

    gross_price_product_trade_price: Optional[TradePrice] = Field(
        default=None,
        description="Original price before adjustments"
    )

    net_price_product_trade_price: TradePrice = Field(
        ...,
        description="Final price after all adjustments"
    )

    @field_validator('net_price_product_trade_price')
    def validate_net_price(cls, value: TradePrice) -> TradePrice:
        """Validates that net price is provided and valid.

        Args:
            value: Net price to validate

        Returns:
            The validated net price

        Raises:
            ValueError: If net price is invalid or negative
        """
        if value is None:
            raise ValueError("Net price is required")
        return value

    @field_validator('gross_price_product_trade_price')
    def validate_gross_price(cls, value: Optional[TradePrice], 
                           values: dict) -> Optional[TradePrice]:
        """Validates gross price in relation to net price.

        Args:
            value: Gross price to validate
            values: Dictionary containing other field values

        Returns:
            The validated gross price

        Raises:
            ValueError: If gross price is less than net price
        """
        if value is not None and 'net_price_product_trade_price' in values:
            net_price = values['net_price_product_trade_price']
            if value.amount < net_price.amount:
                raise ValueError(
                    "Gross price cannot be less than net price"
                )
        return value

    @override
    def to_xml(self, element_name: str, profile: InvoiceProfile) -> ET.Element:
        """Converts the trade agreement to XML format.

        Creates an XML element representing the line trade agreement according to
        the Factur-X specification and the given profile level.

        Args:
            element_name: Name of the root XML element
            profile: Factur-X profile determining required elements

        Returns:
            ET.Element: XML element containing the trade agreement data
        """
        root = ET.Element(f"{{{NAMESPACES[RAM]}}}{element_name}")

        # BuyerOrderReferencedDocument - EN16931 and higher only
        if profile >= InvoiceProfile.EN16931 and self.buyer_order_referenced_document:
            root.append(
                self.buyer_order_referenced_document.to_xml(
                    "BuyerOrderReferencedDocument",
                    profile
                )
            )

        # GrossPriceProductTradePrice - Optional
        if self.gross_price_product_trade_price:
            root.append(
                self.gross_price_product_trade_price.to_xml(
                    "GrossPriceProductTradePrice",
                    profile
                )
            )

        # NetPriceProductTradePrice - Required
        root.append(
            self.net_price_product_trade_price.to_xml(
                "NetPriceProductTradePrice",
                profile
            )
        )

        return root

    def __str__(self) -> str:
        """Returns a string representation of the trade agreement.

        Returns:
            str: Trade agreement details in readable format
        """
        parts = [f"Net Price: {self.net_price_product_trade_price}"]
        if self.gross_price_product_trade_price:
            parts.append(f"Gross Price: {self.gross_price_product_trade_price}")
        if self.buyer_order_referenced_document:
            parts.append(f"Order Ref: {self.buyer_order_referenced_document}")
        return " | ".join(parts)