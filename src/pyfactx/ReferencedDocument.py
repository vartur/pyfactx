from datetime import datetime
from typing import Optional
from lxml import etree as ET

from pydantic import Field
from typing_extensions import override

from .BinaryObject import BinaryObject
from .DocumentTypeCode import DocumentTypeCode
from .InvoiceProfile import InvoiceProfile
from .XMLBaseModel import XMLBaseModel
from .namespaces import NAMESPACES, RAM, UDT


class ReferencedDocument(XMLBaseModel):
    issuer_assigned_id: Optional[str] = Field(default=None)
    uri_id: Optional[str] = Field(default=None)
    line_id: Optional[str] = Field(default=None)
    type_code: Optional[DocumentTypeCode] = Field(default=None)
    name: Optional[str] = Field(default=None)
    attachment_binary_object: Optional[BinaryObject] = Field(default=None)
    reference_type_code: Optional[str] = Field(default=None)
    issue_date: Optional[datetime] = Field(default=None)

    @override
    def to_xml(self, element_name: str, profile: InvoiceProfile) -> ET.Element:
        root = ET.Element(f"{{{NAMESPACES[RAM]}}}{element_name}")

        # IssuerAssignedID
        if self.issuer_assigned_id:
            ET.SubElement(root, f"{{{NAMESPACES[RAM]}}}IssuerAssignedID").text = self.issuer_assigned_id

        if profile >= InvoiceProfile.EN16931:
            # URIID
            if self.uri_id:
                ET.SubElement(root, f"{{{NAMESPACES[RAM]}}}URIID").text = self.uri_id

            # LineID
            if self.line_id:
                ET.SubElement(root, f"{{{NAMESPACES[RAM]}}}LineID").text = self.line_id

            # TypeCode
            if self.type_code:
                ET.SubElement(root, f"{{{NAMESPACES[RAM]}}}TypeCode").text = str(self.type_code.value)

            # Name
            if self.name:
                ET.SubElement(root, f"{{{NAMESPACES[RAM]}}}Name").text = self.name

            # AttachmentBinaryObject
            if self.attachment_binary_object:
                root.append(self.attachment_binary_object.to_xml("AttachmentBinaryObject", profile))

            # ReferenceTypeCode
            if self.reference_type_code:
                ET.SubElement(root, f"{{{NAMESPACES[RAM]}}}ReferenceTypeCode").text = self.reference_type_code

            # FormattedIssueDateTime
            if self.issue_date:
                issue_dt_element = ET.SubElement(root, f"{{{NAMESPACES[RAM]}}}FormattedIssueDateTime")
                ET.SubElement(issue_dt_element, f"{{{NAMESPACES[UDT]}}}DateTimeString",
                              attrib={"format": "102"}).text = self.issue_date.strftime("%Y%m%d")

        return root
