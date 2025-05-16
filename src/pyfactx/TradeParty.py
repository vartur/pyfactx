from typing import Optional, override
from lxml import etree as ET

from pydantic import Field

from .InvoiceProfile import InvoiceProfile
from .LegalOrganization import LegalOrganization
from .TradeAddress import TradeAddress
from .TradeContact import TradeContact
from .UniversalCommunication import UniversalCommunication
from .XMLBaseModel import XMLBaseModel
from .namespaces import NAMESPACES, RAM


class TradeParty(XMLBaseModel):
    ids: Optional[list[str]] = Field(default=None)
    global_ids: Optional[list[tuple[str, str]]] = Field(
        default=None)  # <ram:GlobalID schemeID="0088">587451236587</ram:GlobalID>
    name: str = Field(...)
    description: Optional[str] = Field(default=None)  # From EN16931
    specified_legal_organisation: Optional[LegalOrganization] = Field(default=None)  # Mandatory for seller
    defined_trade_contact: Optional[TradeContact] = Field(default=None)  # From EN16931
    trade_address: Optional[TradeAddress] = Field(default=None)  # Mandatory for seller
    uri_universal_communication: Optional[UniversalCommunication] = Field(default=None)  # e-mail
    specified_tax_registration: Optional[str] = Field(default=None)

    @override
    def to_xml(self, element_name: str, profile: InvoiceProfile) -> ET.Element:
        root = ET.Element(f"{{{NAMESPACES[RAM]}}}{element_name}")

        if profile >= InvoiceProfile.BASICWL:
            # IDs
            if self.ids:
                for identifier in self.ids:
                    ET.SubElement(root, f"{{{NAMESPACES[RAM]}}}ID").text = identifier

            # GlobalIDs
            if self.global_ids:
                for scheme_id, global_id in self.global_ids:
                    ET.SubElement(root, f"{{{NAMESPACES[RAM]}}}GlobalID", attrib={"schemeID": scheme_id}).text = global_id

        # Name
        ET.SubElement(root, f"{{{NAMESPACES[RAM]}}}Name").text = self.name

        if profile >= InvoiceProfile.EN16931:
            # Description
            if self.description:
                ET.SubElement(root, f"{{{NAMESPACES[RAM]}}}Description").text = self.description

        # SpecifiedLegalOrganization
        if self.specified_legal_organisation:
            root.append(self.specified_legal_organisation.to_xml("SpecifiedLegalOrganization", profile))

        if profile >= InvoiceProfile.EN16931:
            # DefinedTradeContact
            if self.defined_trade_contact:
                root.append(self.defined_trade_contact.to_xml("DefinedTradeContact", profile))

        # PostalTradeAddress
        if profile > InvoiceProfile.MINIMUM or element_name == "SellerTradeParty":
            if self.trade_address:
                root.append(self.trade_address.to_xml("PostalTradeAddress", profile))

        if profile >= InvoiceProfile.BASICWL:
            # URIUniversalCommunication
            if self.uri_universal_communication:
                root.append(self.uri_universal_communication.to_xml("URIUniversalCommunication", profile))

        # SpecifiedTaxRegistration
        if profile > InvoiceProfile.MINIMUM or element_name == "SellerTradeParty":
            if self.specified_tax_registration:
                spec_tax_elem = ET.SubElement(root, f"{{{NAMESPACES[RAM]}}}SpecifiedTaxRegistration")
                ET.SubElement(spec_tax_elem, f"{{{NAMESPACES[RAM]}}}ID", attrib={"schemeID": "VA"}).text = self.specified_tax_registration

        return root
