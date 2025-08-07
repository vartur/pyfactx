from datetime import datetime
from typing import Optional, override, List, ClassVar
from lxml import etree as ET
from pydantic import Field, field_validator, model_validator
import re

from .InvoiceProfile import InvoiceProfile
from .InvoiceTypeCode import InvoiceTypeCode
from .Note import Note
from .XMLBaseModel import XMLBaseModel
from .namespaces import NAMESPACES, RAM, RSM, UDT


class ExchangedDocument(XMLBaseModel):
    """Represents an exchanged document in Factur-X format.

    This class represents the header information of an electronic invoice document
    according to the EN16931 standard and Factur-X specifications.

    Attributes:
        id (str): Unique identifier of the document.
        type_code (InvoiceTypeCode): Type of the invoice document.
        issue_date_time (datetime): Date and time when the document was issued.
        included_notes (Optional[list[Note]]): Optional notes included in the document.

    Example:
        ```python
        doc = ExchangedDocument(
            id="INV-2025-001",
            type_code=InvoiceTypeCode.COMMERCIAL_INVOICE,
            issue_date_time=datetime.now(),
            included_notes=[Note(content="Test invoice")]
        )
        ```
    """

    # Class constants for validation
    MAX_ID_LENGTH: ClassVar[int] = 50
    MAX_NOTES: ClassVar[int] = 10
    ALLOWED_ID_PATTERN: ClassVar[str] = r'^[A-Za-z0-9\-/_\.\(\)]+$'
    MIN_DATE: ClassVar[datetime] = datetime(2000, 1, 1)
    MAX_DATE: ClassVar[datetime] = datetime(2100, 12, 31)

    id: str = Field(
        ...,
        description="Unique identifier of the document",
        max_length=MAX_ID_LENGTH
    )

    type_code: InvoiceTypeCode = Field(
        default=InvoiceTypeCode.COMMERCIAL_INVOICE,
        description="Type of the invoice document"
    )

    issue_date_time: datetime = Field(
        ...,
        description="Date and time when the document was issued"
    )

    included_notes: Optional[List[Note]] = Field(
        default=None,
        description="Optional notes included in the document"
    )

    @field_validator('id')
    def validate_id(cls, v: str) -> str:
        """Validates the document identifier format.

        Args:
            v (str): Document identifier to validate.

        Returns:
            str: Validated document identifier.

        Raises:
            ValueError: If the identifier format is invalid.
        """
        # Remove leading/trailing whitespace
        v = v.strip()

        if not v:
            raise ValueError("Document ID cannot be empty")

        if not re.match(cls.ALLOWED_ID_PATTERN, v):
            raise ValueError(
                "Document ID can only contain letters, numbers, and "
                "the following characters: -/_.()"
            )

        if len(v) > cls.MAX_ID_LENGTH:
            raise ValueError(
                f"Document ID length cannot exceed {cls.MAX_ID_LENGTH} characters"
            )

        return v

    @field_validator('issue_date_time')
    def validate_issue_date_time(cls, v: datetime) -> datetime:
        """Validates the issue date and time.

        Args:
            v (datetime): Issue date and time to validate.

        Returns:
            datetime: Validated issue date and time.

        Raises:
            ValueError: If the date is outside the allowed range.
        """
        if v < cls.MIN_DATE or v > cls.MAX_DATE:
            raise ValueError(
                f"Issue date must be between {cls.MIN_DATE.date()} "
                f"and {cls.MAX_DATE.date()}"
            )

        # Ensure timezone-naive datetime for consistency
        if v.tzinfo is not None:
            v = v.replace(tzinfo=None)

        return v

    @model_validator(mode='after')
    def validate_notes(self) -> 'ExchangedDocument':
        """Validates the included notes.

        Raises:
            ValueError: If notes validation fails.
        """
        if self.included_notes:
            if len(self.included_notes) > self.MAX_NOTES:
                raise ValueError(
                    f"Number of notes cannot exceed {self.MAX_NOTES}"
                )

            # Ensure notes are unique
            note_contents = [note.content for note in self.included_notes]
            if len(note_contents) != len(set(note_contents)):
                raise ValueError("Duplicate notes are not allowed")

        return self

    def add_note(self, content: str, subject_code: Optional[str] = None) -> None:
        """Adds a note to the document.

        Args:
            content (str): Content of the note.
            subject_code (Optional[str]): Optional subject code for the note.

        Raises:
            ValueError: If maximum number of notes is exceeded.
        """
        if self.included_notes is None:
            self.included_notes = []

        if len(self.included_notes) >= self.MAX_NOTES:
            raise ValueError(f"Maximum number of notes ({self.MAX_NOTES}) exceeded")

        new_note = Note(content=content, subject_code=subject_code)
        self.included_notes.append(new_note)

    @override
    def to_xml(self, element_name: str, profile: InvoiceProfile) -> ET.Element:
        """Converts the document to XML format.

        Args:
            element_name (str): Name of the XML element to create.
            profile (InvoiceProfile): The Factur-X profile being used.

        Returns:
            ET.Element: An XML element containing the document information.

        Raises:
            ValueError: If XML creation fails.
        """
        try:
            root = ET.Element(f"{{{NAMESPACES[RSM]}}}{element_name}")

            # ID
            id_element = ET.SubElement(root, f"{{{NAMESPACES[RAM]}}}ID")
            id_element.text = self.id

            # TypeCode
            type_element = ET.SubElement(root, f"{{{NAMESPACES[RAM]}}}TypeCode")
            type_element.text = str(self.type_code.value)

            # IssueDateTime
            issue_dt_element = ET.SubElement(
                root, f"{{{NAMESPACES[RAM]}}}IssueDateTime"
            )
            date_element = ET.SubElement(
                issue_dt_element,
                f"{{{NAMESPACES[UDT]}}}DateTimeString",
                attrib={"format": "102"}
            )
            date_element.text = self.issue_date_time.strftime("%Y%m%d")

            # IncludedNotes - only for BASICWL profile and higher
            if profile >= InvoiceProfile.BASICWL and self.included_notes:
                for note in self.included_notes:
                    root.append(note.to_xml("IncludedNote", profile))

            return root

        except (ET.XMLSyntaxError, UnicodeEncodeError) as e:
            raise ValueError(f"Failed to create XML element: {str(e)}")

    def __str__(self) -> str:
        """Returns a human-readable string representation of the document."""
        notes_str = (
            f", Notes: {len(self.included_notes)}" if self.included_notes else ""
        )
        return (
            f"ExchangedDocument(ID: {self.id}, "
            f"Type: {self.type_code.name}, "
            f"Date: {self.issue_date_time.date()}{notes_str})"
        )

    @classmethod
    def create_invoice(
        cls,
        invoice_id: str,
        issue_date: datetime,
        type_code: InvoiceTypeCode = InvoiceTypeCode.COMMERCIAL_INVOICE
    ) -> 'ExchangedDocument':
        """Creates a new invoice document.

        Args:
            invoice_id (str): Unique identifier for the invoice.
            issue_date (datetime): Date when the invoice was issued.
            type_code (InvoiceTypeCode): Type of invoice document.

        Returns:
            ExchangedDocument: New invoice document instance.
        """
        return cls(
            id=invoice_id,
            type_code=type_code,
            issue_date_time=issue_date
        )