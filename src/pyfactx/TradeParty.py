from typing import Optional

from pydantic import BaseModel, Field

from .InvoiceProfile import InvoiceProfile
from .TradeAddress import TradeAddress
from .LegalOrganization import LegalOrganization


class TradeParty(BaseModel):
    ids: Optional[list[str]] = Field(default=None)
    global_ids: Optional[list[tuple[str, str]]] = Field(
        default=None)  # <ram:GlobalID schemeID="0088">587451236587</ram:GlobalID>
    name: str = Field(...)
    specified_legal_organisation: Optional[LegalOrganization] = Field(default=None)  # Mandatory for seller
    trade_address: Optional[TradeAddress] = Field(default=None)  # Mandatory for seller
    uri_universal_communication: Optional[str] = Field(default=None)  # e-mail
    specified_tax_registration: Optional[str] = Field(default=None)

    def to_xml(self, profile: InvoiceProfile.MINIMUM):
        xml_string = ""

        if profile != InvoiceProfile.MINIMUM:
            if self.ids is not None:
                for identifier in self.ids:
                    xml_string += f"<ram:ID>{identifier}</ram:ID>"

            if self.global_ids is not None:
                for scheme_id, global_id in self.global_ids:
                    xml_string += f"<ram:GlobalID schemeID=\"{scheme_id}\">{global_id}</ram:GlobalID>"

        xml_string += f"<ram:Name>{self.name}</ram:Name>"

        if self.specified_legal_organisation is not None:
            xml_string += f'''<ram:SpecifiedLegalOrganization>
                                    {self.specified_legal_organisation.to_xml(profile)}
                                </ram:SpecifiedLegalOrganization>'''

        if self.trade_address is not None:
            xml_string += self.trade_address.to_xml(profile)

        if profile != InvoiceProfile.MINIMUM:
            if self.uri_universal_communication is not None:
                xml_string += f'''<ram:URIUniversalCommunication>
                                        <ram:URIID schemeID="EM">{self.uri_universal_communication}</ram:URIID>
                                    </ram:URIUniversalCommunication>'''

        if self.specified_tax_registration is not None:
            xml_string += f'''<ram:SpecifiedTaxRegistration>
                                    <ram:ID schemeID="VA">{self.specified_tax_registration}</ram:ID>
                                </ram:SpecifiedTaxRegistration>'''

        return xml_string
