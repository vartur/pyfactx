from xml.etree.ElementTree import Element, SubElement

from pydantic import Field
from typing_extensions import override

from .InvoiceProfile import InvoiceProfile
from .XMLBaseModel import XMLBaseModel
from .namespaces import RAM


class ReferencedDocument(XMLBaseModel):
    issuer_assigned_id: str = Field(...)

    @override
    def to_xml(self, element_name: str, _profile: InvoiceProfile) -> Element:
        root = Element(f"{RAM}:{element_name}")

        # IssuerAssignedID
        SubElement(root, f"{RAM}:IssuerAssignedID").text = self.issuer_assigned_id

        return root
