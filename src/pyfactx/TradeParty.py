from typing import Optional, override
from xml.etree.ElementTree import Element, SubElement

from pydantic import Field

from .InvoiceProfile import InvoiceProfile
from .LegalOrganization import LegalOrganization
from .TradeAddress import TradeAddress
from .XMLBaseModel import XMLBaseModel
from .namespaces import RAM


class TradeParty(XMLBaseModel):
    ids: Optional[list[str]] = Field(default=None)
    global_ids: Optional[list[tuple[str, str]]] = Field(
        default=None)  # <ram:GlobalID schemeID="0088">587451236587</ram:GlobalID>
    name: str = Field(...)
    specified_legal_organisation: Optional[LegalOrganization] = Field(default=None)  # Mandatory for seller
    trade_address: Optional[TradeAddress] = Field(default=None)  # Mandatory for seller
    uri_universal_communication: Optional[str] = Field(default=None)  # e-mail
    specified_tax_registration: Optional[str] = Field(default=None)

    @override
    def to_xml(self, element_name: str, profile: InvoiceProfile) -> Element:
        root = Element(f"{RAM}:{element_name}")

        if profile != InvoiceProfile.MINIMUM:
            # IDs
            if self.ids:
                for identifier in self.ids:
                    SubElement(root, f"{RAM}:ID").text = identifier

            # GlobalIDs
            if self.global_ids:
                for scheme_id, global_id in self.global_ids:
                    SubElement(root, f"{RAM}:GlobalID", attrib={"schemeID": scheme_id}).text = global_id

        # Name
        SubElement(root, f"{RAM}:Name").text = self.name

        # SpecifiedLegalOrganization
        if self.specified_legal_organisation:
            root.append(self.specified_legal_organisation.to_xml("SpecifiedLegalOrganization", profile))

        # PostalTradeAddress
        if self.trade_address:
            root.append(self.trade_address.to_xml("PostalTradeAddress", profile))

        if profile != InvoiceProfile.MINIMUM:
            # URIUniversalCommunication
            if self.uri_universal_communication:
                uri_univ_element = SubElement(root, f"{RAM}:URIUniversalCommunication")
                SubElement(uri_univ_element, f"{RAM}:URIID",
                           attrib={"schemeID": "EM"}).text = self.uri_universal_communication

        # SpecifiedTaxRegistration
        if self.specified_tax_registration:
            spec_tax_elem = SubElement(root, f"{RAM}:SpecifiedTaxRegistration")
            SubElement(spec_tax_elem, f"{RAM}:ID", attrib={"schemeID": "VA"}).text = self.specified_tax_registration

        return root
