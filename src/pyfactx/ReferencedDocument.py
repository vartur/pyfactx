from xml.etree.ElementTree import Element, SubElement

from pydantic import BaseModel, Field

from .InvoiceProfile import InvoiceProfile
from .namespaces import RAM


class ReferencedDocument(BaseModel):
    issuer_assigned_id: str = Field(...)

    def to_xml(self, element_name: str, profile: InvoiceProfile = InvoiceProfile.MINIMUM) -> Element:
        root = Element(f"{RAM}:{element_name}")

        # IssuerAssignedID
        SubElement(root, f"{RAM}:IssuerAssignedID").text = self.issuer_assigned_id

        return root
