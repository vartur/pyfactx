from typing import Optional
from xml.etree.ElementTree import Element, SubElement

from pydantic import Field

from .InvoiceProfile import InvoiceProfile
from .UniversalCommunication import UniversalCommunication
from .XMLBaseModel import XMLBaseModel
from .namespaces import RAM


class TradeContact(XMLBaseModel):
    person_name: Optional[str] = Field(default=None)
    department_name: Optional[str] = Field(default=None)
    telephone_universal_communication: Optional[UniversalCommunication] = Field(default=None)
    email_uri_universal_communication: Optional[UniversalCommunication] = Field(default=None)

    def to_xml(self, element_name: str, profile: InvoiceProfile) -> Element:
        root = Element(f"{RAM}:{element_name}")

        # PersonName
        if self.person_name:
            SubElement(root, f"{RAM}:PersonName").text = self.person_name

        # DepartmentName
        if self.department_name:
            SubElement(root, f"{RAM}:DepartmentName").text = self.department_name

        # TelephoneUniversalCommunication
        if self.telephone_universal_communication:
            root.append(self.telephone_universal_communication.to_xml("TelephoneUniversalCommunication", profile))

        # EmailURIUniversalCommunication
        if self.email_uri_universal_communication:
            root.append(self.email_uri_universal_communication.to_xml("EmailURIUniversalCommunication", profile))

        return root
