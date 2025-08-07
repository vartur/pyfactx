from typing import Optional, List, Tuple
from lxml import etree as ET

from pydantic import Field, field_validator
from typing_extensions import override

from .InvoiceProfile import InvoiceProfile
from .LegalOrganization import LegalOrganization
from .TradeAddress import TradeAddress
from .TradeContact import TradeContact
from .UniversalCommunication import UniversalCommunication
from .XMLBaseModel import XMLBaseModel
from .namespaces import NAMESPACES, RAM


class TradeParty(XMLBaseModel):
    """Represents a trade party according to UN/CEFACT standards.
    
    This class models organizations or individuals involved in trade transactions,
    particularly in electronic invoices. It includes identification, contact details,
    and legal information.

    Attributes:
        ids: List of party identifiers
        global_ids: List of globally unique identifiers with scheme IDs
        name: Official name of the trade party
        description: Additional description of the trade party
        specified_legal_organisation: Legal organization details
        defined_trade_contact: Contact person details
        trade_address: Postal address details
        uri_universal_communication: Electronic communication details
        specified_tax_registration: VAT registration number
    """

    ids: Optional[List[str]] = Field(
        default=None,
        description="List of party identifiers",
        max_length=100  # Reasonable limit for number of IDs
    )

    global_ids: Optional[List[Tuple[str, str]]] = Field(
        default=None,
        description="List of global IDs with scheme identifiers",
        max_length=100  # Reasonable limit for number of global IDs
    )

    name: str = Field(
        ...,
        description="Official name of the trade party",
        min_length=1,
        max_length=140
    )

    description: Optional[str] = Field(
        default=None,
        description="Additional description of the trade party",
        max_length=512
    )

    specified_legal_organisation: Optional[LegalOrganization] = Field(
        default=None,
        description="Legal organization details (mandatory for seller)"
    )

    defined_trade_contact: Optional[TradeContact] = Field(
        default=None,
        description="Contact person details"
    )

    trade_address: Optional[TradeAddress] = Field(
        default=None,
        description="Postal address details (mandatory for seller)"
    )

    uri_universal_communication: Optional[UniversalCommunication] = Field(
        default=None,
        description="Electronic communication details (e.g., email)"
    )

    specified_tax_registration: Optional[str] = Field(
        default=None,
        description="VAT registration number",
        pattern=r'^[A-Z]{2}[0-9A-Z]+$'  # Basic VAT number format validation
    )

    @field_validator('ids')
    def validate_ids(cls, v: Optional[List[str]]) -> Optional[List[str]]:
        """Validates the list of party identifiers."""
        if v is not None:
            if not all(id_.strip() for id_ in v):
                raise ValueError("IDs cannot be empty or whitespace")
            return [id_.strip() for id_ in v]
        return v

    @field_validator('global_ids')
    def validate_global_ids(cls, v: Optional[List[Tuple[str, str]]]) -> Optional[List[Tuple[str, str]]]:
        """Validates the list of global identifiers."""
        if v is not None:
            for scheme_id, global_id in v:
                if not scheme_id.strip():
                    raise ValueError("Scheme ID cannot be empty")
                if not global_id.strip():
                    raise ValueError("Global ID cannot be empty")
            return [(s.strip(), g.strip()) for s, g in v]
        return v

    def is_seller(self) -> bool:
        """Checks if this party has all mandatory seller fields.

        Returns:
            bool: True if party has all required seller fields
        """
        return bool(
            self.specified_legal_organisation and 
            self.trade_address and
            self.specified_tax_registration
        )

    @override
    def to_xml(self, element_name: str, profile: InvoiceProfile) -> ET.Element:
        """Converts the trade party to its XML representation.

        Creates an XML element representing this trade party according to
        the Cross Industry Invoice (CII) XML schema and the specified profile.

        Args:
            element_name: The name to use for the root XML element
            profile: The invoice profile containing serialization settings

        Returns:
            ET.Element: An XML element representing this trade party

        Example:
            ```xml
            <ram:SellerTradeParty>
                <ram:ID>123456789</ram:ID>
                <ram:GlobalID schemeID="0088">587451236587</ram:GlobalID>
                <ram:Name>Seller Company Ltd</ram:Name>
                <ram:Description>Main office</ram:Description>
                <!-- Other elements -->
            </ram:SellerTradeParty>
            ```
        """
        root = ET.Element(f"{{{NAMESPACES[RAM]}}}{element_name}")

        if profile >= InvoiceProfile.BASICWL:
            # IDs
            if self.ids:
                for identifier in self.ids:
                    ET.SubElement(root, f"{{{NAMESPACES[RAM]}}}ID").text = identifier

            # GlobalIDs
            if self.global_ids:
                for scheme_id, global_id in self.global_ids:
                    ET.SubElement(
                        root, 
                        f"{{{NAMESPACES[RAM]}}}GlobalID",
                        attrib={"schemeID": scheme_id}
                    ).text = global_id

        # Name
        ET.SubElement(root, f"{{{NAMESPACES[RAM]}}}Name").text = self.name

        if profile >= InvoiceProfile.EN16931:
            # Description
            if self.description:
                ET.SubElement(root, f"{{{NAMESPACES[RAM]}}}Description").text = self.description

        # SpecifiedLegalOrganization
        if self.specified_legal_organisation:
            root.append(self.specified_legal_organisation.to_xml(
                "SpecifiedLegalOrganization",
                profile
            ))

        if profile >= InvoiceProfile.EN16931:
            # DefinedTradeContact
            if self.defined_trade_contact:
                root.append(self.defined_trade_contact.to_xml(
                    "DefinedTradeContact",
                    profile
                ))

        # PostalTradeAddress
        if profile > InvoiceProfile.MINIMUM or element_name == "SellerTradeParty":
            if self.trade_address:
                root.append(self.trade_address.to_xml(
                    "PostalTradeAddress",
                    profile
                ))

        if profile >= InvoiceProfile.BASICWL:
            # URIUniversalCommunication
            if self.uri_universal_communication:
                root.append(self.uri_universal_communication.to_xml(
                    "URIUniversalCommunication",
                    profile
                ))

        # SpecifiedTaxRegistration
        if profile > InvoiceProfile.MINIMUM or element_name == "SellerTradeParty":
            if self.specified_tax_registration:
                spec_tax_elem = ET.SubElement(
                    root,
                    f"{{{NAMESPACES[RAM]}}}SpecifiedTaxRegistration"
                )
                ET.SubElement(
                    spec_tax_elem,
                    f"{{{NAMESPACES[RAM]}}}ID",
                    attrib={"schemeID": "VA"}
                ).text = self.specified_tax_registration

        return root

    def __str__(self) -> str:
        """Returns a human-readable string representation.

        Returns:
            str: Description of the trade party
        """
        parts = [f"Name: {self.name}"]
        if self.description:
            parts.append(f"Description: {self.description}")
        if self.specified_tax_registration:
            parts.append(f"VAT: {self.specified_tax_registration}")
        return ", ".join(parts)