from decimal import Decimal
from lxml import etree as ET
from typing import Optional, List

from pydantic import Field, ConfigDict, model_validator
from typing_extensions import override

from .HeaderTradeAgreement import HeaderTradeAgreement
from .HeaderTradeDelivery import HeaderTradeDelivery
from .HeaderTradeSettlement import HeaderTradeSettlement
from .InvoiceProfile import InvoiceProfile
from .SupplyChainTradeLineItem import SupplyChainTradeLineItem
from .XMLBaseModel import XMLBaseModel
from .namespaces import NAMESPACES, RSM


class SupplyChainTradeTransaction(XMLBaseModel):
    """Represents a supply chain trade transaction in the invoice.

    This class models the complete trade transaction according to the Factur-X standard,
    including line items, trade agreement, delivery, and settlement information.

    Attributes:
        included_supply_chain_trade_line_items: List of line items (mandatory for BASIC profile and above)
        applicable_header_trade_agreement: Header level trade agreement details
        applicable_header_trade_delivery: Header level delivery information
        applicable_header_trade_settlement: Header level settlement details

    Examples:
        >>> transaction = SupplyChainTradeTransaction(
        ...     included_supply_chain_trade_line_items=[SupplyChainTradeLineItem(...)],
        ...     applicable_header_trade_agreement=HeaderTradeAgreement(...),
        ...     applicable_header_trade_delivery=HeaderTradeDelivery(...),
        ...     applicable_header_trade_settlement=HeaderTradeSettlement(...)
        ... )
    """

    model_config = ConfigDict(
        validate_assignment=True,
        str_strip_whitespace=True
    )

    included_supply_chain_trade_line_items: Optional[List[SupplyChainTradeLineItem]] = Field(
        default=None,
        description="List of line items (mandatory for BASIC profile and above)",
        title="Supply Chain Trade Line Items"
    )

    applicable_header_trade_agreement: HeaderTradeAgreement = Field(
        ...,
        description="Header level trade agreement details",
        title="Header Trade Agreement"
    )

    applicable_header_trade_delivery: HeaderTradeDelivery = Field(
        ...,
        description="Header level delivery information",
        title="Header Trade Delivery"
    )

    applicable_header_trade_settlement: HeaderTradeSettlement = Field(
        ...,
        description="Header level settlement details",
        title="Header Trade Settlement"
    )

    @model_validator(mode='after')
    def validate_transaction(self) -> 'SupplyChainTradeTransaction':
        """Validates the consistency of the transaction data.

        Returns:
            SupplyChainTradeTransaction: The validated instance

        Raises:
            ValueError: If validation fails
        """
        # Validate line items presence for BASIC profile and above
        if hasattr(self, '_profile') and self._profile >= InvoiceProfile.BASIC:
            if not self.included_supply_chain_trade_line_items:
                raise ValueError(
                    "Line items are mandatory for BASIC profile and above"
                )

        # Validate line items if present
        if self.included_supply_chain_trade_line_items:
            if len(self.included_supply_chain_trade_line_items) > 999999:
                raise ValueError("Maximum number of line items exceeded (999999)")

            # Validate line numbers are unique
            line_ids = set()
            for item in self.included_supply_chain_trade_line_items:
                if item.associated_document_line_document.line_id in line_ids:
                    raise ValueError(
                        f"Duplicate line ID: {item.associated_document_line_document.line_id}"
                    )
                line_ids.add(item.associated_document_line_document.line_id)

        return self

    @override
    def to_xml(self, element_name: str, profile: InvoiceProfile) -> ET.Element:
        """Converts the transaction to XML format.

        Creates an XML element representing the transaction according to
        the Factur-X specification and the specified profile.

        Args:
            element_name: Name of the root XML element
            profile: Factur-X profile determining available fields

        Returns:
            ET.Element: XML element containing the transaction data
        """
        root = ET.Element(f"{{{NAMESPACES[RSM]}}}{element_name}")

        if profile >= InvoiceProfile.BASIC:
            # IncludedSupplyChainTradeLineItems
            if self.included_supply_chain_trade_line_items:
                for line_item in self.included_supply_chain_trade_line_items:
                    root.append(
                        line_item.to_xml(
                            "IncludedSupplyChainTradeLineItem",
                            profile
                        )
                    )

        # ApplicableHeaderTradeAgreement
        root.append(
            self.applicable_header_trade_agreement.to_xml(
                "ApplicableHeaderTradeAgreement",
                profile
            )
        )

        # ApplicableHeaderTradeDelivery
        root.append(
            self.applicable_header_trade_delivery.to_xml(
                "ApplicableHeaderTradeDelivery",
                profile
            )
        )

        # ApplicableHeaderTradeSettlement
        root.append(
            self.applicable_header_trade_settlement.to_xml(
                "ApplicableHeaderTradeSettlement",
                profile
            )
        )

        return root

    def __str__(self) -> str:
        """Returns a string representation of the transaction.

        Returns:
            str: Transaction in readable format
        """
        item_count = len(self.included_supply_chain_trade_line_items or [])
        return f"Trade Transaction with {item_count} line item(s)"

    def get_line_count(self) -> int:
        """Gets the number of line items in the transaction.

        Returns:
            int: Number of line items
        """
        return len(self.included_supply_chain_trade_line_items or [])

    def has_line_items(self) -> bool:
        """Checks if the transaction has any line items.

        Returns:
            bool: True if there are line items
        """
        return bool(self.included_supply_chain_trade_line_items)