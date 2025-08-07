from typing import Optional, ClassVar
from lxml import etree as ET
from pydantic import Field, ConfigDict, model_validator
from typing_extensions import override

from .InvoiceProfile import InvoiceProfile
from .ReferencedDocument import ReferencedDocument
from .SupplyChainEvent import SupplyChainEvent
from .TradeParty import TradeParty
from .XMLBaseModel import XMLBaseModel
from .namespaces import NAMESPACES, RAM


class HeaderTradeDelivery(XMLBaseModel):
    """Represents the trade delivery header section of a Factur-X document.

    This class contains information about delivery details, including shipping
    addresses, delivery events, and related delivery documents.

    Attributes:
        ship_to_trade_party: Optional delivery destination details
        actual_delivery_supply_chain_event: Optional actual delivery event details
        despatch_advice_referenced_document: Optional dispatch advice reference
        receiving_advice_referenced_document: Optional receiving advice reference
    """

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        validate_assignment=True
    )

    # XML element names as constants
    XML_ELEMENTS: ClassVar[dict[str, str]] = {
        'ship_to': 'ShipToTradeParty',
        'delivery_event': 'ActualDeliverySupplyChainEvent',
        'despatch_advice': 'DespatchAdviceReferencedDocument',
        'receiving_advice': 'ReceivingAdviceReferencedDocument'
    }

    ship_to_trade_party: Optional[TradeParty] = Field(
        default=None,
        description="Trading partner where goods are delivered (BASICWL and above)"
    )

    actual_delivery_supply_chain_event: Optional[SupplyChainEvent] = Field(
        default=None,
        description="Actual delivery event details (BASICWL and above)"
    )

    despatch_advice_referenced_document: Optional[ReferencedDocument] = Field(
        default=None,
        description="Reference to dispatch advice document (BASICWL and above)"
    )

    receiving_advice_referenced_document: Optional[ReferencedDocument] = Field(
        default=None,
        description="Reference to receiving advice document (EN16931 and above)"
    )

    @model_validator(mode='after')
    def validate_profile_specific_fields(self) -> 'HeaderTradeDelivery':
        """Validates that fields are appropriate for their profile level.

        Returns:
            HeaderTradeDelivery: The validated instance

        Raises:
            ValueError: If fields are used with inappropriate profile levels
        """
        profile = getattr(self, '_current_profile', None)
        if not profile:
            return self

        if profile < InvoiceProfile.BASICWL:
            if any([
                self.ship_to_trade_party,
                self.actual_delivery_supply_chain_event,
                self.despatch_advice_referenced_document
            ]):
                raise ValueError(
                    "Ship-to, delivery event, and dispatch advice are only allowed "
                    "in BASICWL profile and above"
                )

        if profile < InvoiceProfile.EN16931:
            if self.receiving_advice_referenced_document:
                raise ValueError(
                    "Receiving advice document is only allowed in EN16931 profile "
                    "and above"
                )

        return self

    def _append_element_if_valid(
        self,
        root: ET.Element,
        field_value: Optional[XMLBaseModel],
        element_name: str,
        profile: InvoiceProfile,
        min_profile: InvoiceProfile
    ) -> None:
        """Helper method to append XML elements based on profile requirements.

        Args:
            root: The root element to append to
            field_value: The value to append
            element_name: The name of the XML element
            profile: Current profile
            min_profile: Minimum required profile
        """
        if field_value is not None and profile >= min_profile:
            root.append(field_value.to_xml(element_name, profile))

    @override
    def to_xml(self, element_name: str, profile: InvoiceProfile) -> ET.Element:
        """Converts the trade delivery to XML format.

        Args:
            element_name: Name of the root XML element
            profile: The Factur-X profile being used

        Returns:
            ET.Element: The XML element containing the trade delivery data
        """
        root = ET.Element(f"{{{NAMESPACES[RAM]}}}{element_name}")

        # Set profile for validation
        self._current_profile = profile

        # BASICWL and above elements
        self._append_element_if_valid(
            root,
            self.ship_to_trade_party,
            self.XML_ELEMENTS['ship_to'],
            profile,
            InvoiceProfile.BASICWL
        )

        self._append_element_if_valid(
            root,
            self.actual_delivery_supply_chain_event,
            self.XML_ELEMENTS['delivery_event'],
            profile,
            InvoiceProfile.BASICWL
        )

        self._append_element_if_valid(
            root,
            self.despatch_advice_referenced_document,
            self.XML_ELEMENTS['despatch_advice'],
            profile,
            InvoiceProfile.BASICWL
        )

        # EN16931 and above elements
        self._append_element_if_valid(
            root,
            self.receiving_advice_referenced_document,
            self.XML_ELEMENTS['receiving_advice'],
            profile,
            InvoiceProfile.EN16931
        )

        return root

    @classmethod
    def create_basic_delivery(
        cls,
        ship_to: Optional[TradeParty] = None,
        delivery_event: Optional[SupplyChainEvent] = None
    ) -> 'HeaderTradeDelivery':
        """Creates a basic delivery header with minimal information.

        Args:
            ship_to: Optional shipping destination
            delivery_event: Optional delivery event details

        Returns:
            HeaderTradeDelivery: A new instance with basic delivery information
        """
        return cls(
            ship_to_trade_party=ship_to,
            actual_delivery_supply_chain_event=delivery_event
        )