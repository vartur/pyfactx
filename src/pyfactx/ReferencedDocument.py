from datetime import datetime
from typing import Optional
from lxml import etree as ET

from pydantic import Field, field_validator, ConfigDict
from typing_extensions import override
from urllib.parse import urlparse

from .BinaryObject import BinaryObject
from .DocumentTypeCode import DocumentTypeCode
from .InvoiceProfile import InvoiceProfile
from .XMLBaseModel import XMLBaseModel
from .namespaces import NAMESPACES, RAM, UDT


class ReferencedDocument(XMLBaseModel):
    """Represents a referenced document in the invoice.

    This class models references to external documents according to the Factur-X standard,
    such as supporting documents, attachments, or related business documents.

    Attributes:
        issuer_assigned_id: ID assigned by the document issuer
        uri_id: URI identifier for the document
        line_id: Line identifier within the document
        type_code: Type of the referenced document
        name: Name or title of the document
        attachment_binary_object: Binary attachment data
        reference_type_code: Code specifying the type of reference
        issue_date: Date when the referenced document was issued
    """

    model_config = ConfigDict(
        validate_assignment=True,
        str_strip_whitespace=True,
        str_max_length=1000
    )

    issuer_assigned_id: Optional[str] = Field(
        default=None,
        description="ID assigned by the document issuer",
        max_length=50,
        examples=["DOC-2025-001", "INV-123456"]
    )

    uri_id: Optional[str] = Field(
        default=None,
        description="URI identifier for the document",
        max_length=256,
        examples=["https://example.com/docs/invoice.pdf", "file:///local/doc.pdf"]
    )

    line_id: Optional[str] = Field(
        default=None,
        description="Line identifier within the document",
        max_length=50,
        examples=["LINE-001", "1"]
    )

    type_code: Optional[DocumentTypeCode] = Field(
        default=None,
        description="Type of the referenced document"
    )

    name: Optional[str] = Field(
        default=None,
        description="Name or title of the document",
        max_length=256,
        examples=["Purchase Order", "Delivery Note"]
    )

    attachment_binary_object: Optional[BinaryObject] = Field(
        default=None,
        description="Binary attachment data"
    )

    reference_type_code: Optional[str] = Field(
        default=None,
        description="Code specifying the type of reference",
        max_length=50,
        examples=["PO", "DN"]
    )

    issue_date: Optional[datetime] = Field(
        default=None,
        description="Date when the referenced document was issued"
    )

    @field_validator('issuer_assigned_id')
    def validate_issuer_assigned_id(cls, value: Optional[str]) -> Optional[str]:
        """Validates the issuer assigned ID.

        Args:
            value: ID to validate

        Returns:
            Optional[str]: Validated ID or None

        Raises:
            ValueError: If validation fails
        """
        if value is not None:
            value = value.strip()
            if not value:
                raise ValueError("Issuer assigned ID cannot be empty if provided")
        return value

    @field_validator('uri_id')
    def validate_uri_id(cls, value: Optional[str]) -> Optional[str]:
        """Validates the URI identifier.

        Args:
            value: URI to validate

        Returns:
            Optional[str]: Validated URI or None

        Raises:
            ValueError: If validation fails
        """
        if value is not None:
            value = value.strip()
            try:
                result = urlparse(value)
                if not all([result.scheme, result.netloc or result.path]):
                    raise ValueError("Invalid URI format")
            except Exception as e:
                raise ValueError(f"Invalid URI: {str(e)}")
        return value

    @field_validator('line_id')
    def validate_line_id(cls, value: Optional[str]) -> Optional[str]:
        """Validates the line identifier.

        Args:
            value: Line ID to validate

        Returns:
            Optional[str]: Validated line ID or None

        Raises:
            ValueError: If validation fails
        """
        if value is not None:
            value = value.strip()
            if not value:
                raise ValueError("Line ID cannot be empty if provided")
            if not all(c.isalnum() or c in '-_.' for c in value):
                raise ValueError("Line ID contains invalid characters")
        return value

    @field_validator('name')
    def validate_name(cls, value: Optional[str]) -> Optional[str]:
        """Validates the document name.

        Args:
            value: Name to validate

        Returns:
            Optional[str]: Validated name or None

        Raises:
            ValueError: If validation fails
        """
        if value is not None:
            value = " ".join(value.split())
            if not value:
                raise ValueError("Document name cannot be empty if provided")
        return value

    @field_validator('reference_type_code')
    def validate_reference_type_code(cls, value: Optional[str]) -> Optional[str]:
        """Validates the reference type code.

        Args:
            value: Reference type code to validate

        Returns:
            Optional[str]: Validated reference type code or None

        Raises:
            ValueError: If validation fails
        """
        if value is not None:
            value = value.strip().upper()
            if not value:
                raise ValueError("Reference type code cannot be empty if provided")
            if not all(c.isalnum() or c == '-' for c in value):
                raise ValueError("Reference type code contains invalid characters")
        return value

    @override
    def to_xml(self, element_name: str, profile: InvoiceProfile) -> ET.Element:
        """Converts the referenced document to XML format.

        Creates an XML element representing the referenced document according to
        the Factur-X specification and the specified profile.

        Args:
            element_name: Name of the root XML element
            profile: Factur-X profile determining available fields

        Returns:
            ET.Element: XML element containing the document data
        """
        root = ET.Element(f"{{{NAMESPACES[RAM]}}}{element_name}")

        # IssuerAssignedID (Basic profile)
        if self.issuer_assigned_id:
            ET.SubElement(
                root,
                f"{{{NAMESPACES[RAM]}}}IssuerAssignedID"
            ).text = self.issuer_assigned_id

        # Extended fields for EN16931 and higher profiles
        if profile >= InvoiceProfile.EN16931:
            # URIID
            if self.uri_id:
                ET.SubElement(
                    root,
                    f"{{{NAMESPACES[RAM]}}}URIID"
                ).text = self.uri_id

            # LineID
            if self.line_id:
                ET.SubElement(
                    root,
                    f"{{{NAMESPACES[RAM]}}}LineID"
                ).text = self.line_id

            # TypeCode
            if self.type_code:
                ET.SubElement(
                    root,
                    f"{{{NAMESPACES[RAM]}}}TypeCode"
                ).text = str(self.type_code.value)

            # Name
            if self.name:
                ET.SubElement(
                    root,
                    f"{{{NAMESPACES[RAM]}}}Name"
                ).text = self.name

            # AttachmentBinaryObject
            if self.attachment_binary_object:
                root.append(
                    self.attachment_binary_object.to_xml(
                        "AttachmentBinaryObject",
                        profile
                    )
                )

            # ReferenceTypeCode
            if self.reference_type_code:
                ET.SubElement(
                    root,
                    f"{{{NAMESPACES[RAM]}}}ReferenceTypeCode"
                ).text = self.reference_type_code

            # FormattedIssueDateTime
            if self.issue_date:
                issue_dt_element = ET.SubElement(
                    root,
                    f"{{{NAMESPACES[RAM]}}}FormattedIssueDateTime"
                )
                ET.SubElement(
                    issue_dt_element,
                    f"{{{NAMESPACES[UDT]}}}DateTimeString",
                    attrib={"format": "102"}
                ).text = self.issue_date.strftime("%Y%m%d")

        return root

    def __str__(self) -> str:
        """Returns a string representation of the referenced document.

        Returns:
            str: Document reference in readable format
        """
        parts = []
        if self.type_code:
            parts.append(f"Type: {self.type_code}")
        if self.name:
            parts.append(f"Name: {self.name}")
        if self.issuer_assigned_id:
            parts.append(f"ID: {self.issuer_assigned_id}")
        if not parts:
            return "Empty document reference"
        return " | ".join(parts)

    def has_attachment(self) -> bool:
        """Checks if the document has an attachment.

        Returns:
            bool: True if the document has an attachment
        """
        return self.attachment_binary_object is not None

    def get_reference_details(self) -> dict:
        """Gets a dictionary of reference details.

        Returns:
            dict: Dictionary containing non-None reference details
        """
        return {
            key: value for key, value in {
                "id": self.issuer_assigned_id,
                "uri": self.uri_id,
                "line": self.line_id,
                "type": self.type_code,
                "name": self.name,
                "reference_type": self.reference_type_code,
                "issue_date": self.issue_date
            }.items() if value is not None
        }