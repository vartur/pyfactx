from typing import Optional
from lxml import etree as ET

from pydantic import Field, field_validator, ConfigDict
from typing_extensions import override

from .InvoiceProfile import InvoiceProfile
from .XMLBaseModel import XMLBaseModel
from .namespaces import NAMESPACES, RAM


class Note(XMLBaseModel):
    """Represents a textual note in the invoice document.

    This class models notes and comments that can be attached to various
    elements in a Factur-X invoice, with optional subject classification
    according to UN/EDIFACT code list 4451.

    Attributes:
        content: The actual text content of the note.
        subject_code: Optional UN/EDIFACT 4451 code classifying the note type.
            See: https://service.unece.org/trade/untdid/d00a/tred/tred4451.htm

    Examples:
        >>> note = Note(content="Delivery delayed due to weather conditions")
        >>> note_with_code = Note(
        ...     content="Payment terms: 30 days net",
        ...     subject_code="PMT"
        ... )
    """

    model_config = ConfigDict(
        validate_assignment=True,
        str_strip_whitespace=True,
        str_max_length=1000  # Reasonable limit for note content
    )

    content: str = Field(
        ...,
        description="Text content of the note",
        min_length=1,
        max_length=1000
    )

    subject_code: Optional[str] = Field(
        default=None,
        description="UN/EDIFACT 4451 code classifying the note",
        max_length=3,
        pattern=r'^[A-Z0-9]{1,3}$'
    )

    @field_validator('content')
    def validate_content(cls, value: str) -> str:
        """Validates the note content.

        Args:
            value: Note content to validate

        Returns:
            str: Validated note content

        Raises:
            ValueError: If content validation fails
        """
        # Remove excessive whitespace
        value = " ".join(value.split())
        
        # Check for minimum meaningful content
        if len(value.strip()) < 1:
            raise ValueError("Note content cannot be empty")
            
        # Check for reasonable line length
        if any(len(line) > 200 for line in value.splitlines()):
            raise ValueError("Note content contains lines that are too long")
            
        return value

    @field_validator('subject_code')
    def validate_subject_code(cls, value: Optional[str]) -> Optional[str]:
        """Validates the subject code according to UN/EDIFACT 4451.

        Args:
            value: Subject code to validate

        Returns:
            Optional[str]: Validated subject code or None

        Raises:
            ValueError: If subject code validation fails
        """
        if value is not None:
            # Convert to uppercase for consistency
            value = value.upper()
            
            # Validate format
            if not value.isalnum():
                raise ValueError(
                    "Subject code must contain only letters and numbers"
                )
                
            if len(value) > 3:
                raise ValueError("Subject code cannot exceed 3 characters")
                
        return value

    @override
    def to_xml(self, element_name: str, _profile: InvoiceProfile) -> ET.Element:
        """Converts the note to XML format.

        Creates an XML element representing the note according to
        the Factur-X specification.

        Args:
            element_name: Name of the root XML element
            _profile: Factur-X profile (unused but required by interface)

        Returns:
            ET.Element: XML element containing the note data
        """
        root = ET.Element(f"{{{NAMESPACES[RAM]}}}{element_name}")

        # Content (required)
        content_element = ET.SubElement(
            root,
            f"{{{NAMESPACES[RAM]}}}Content"
        )
        content_element.text = self.content

        # SubjectCode (optional)
        if self.subject_code:
            subject_element = ET.SubElement(
                root,
                f"{{{NAMESPACES[RAM]}}}SubjectCode"
            )
            subject_element.text = self.subject_code

        return root

    def __str__(self) -> str:
        """Returns a string representation of the note.

        Returns:
            str: Note content with optional subject code
        """
        if self.subject_code:
            return f"[{self.subject_code}] {self.content}"
        return self.content

    def get_formatted_content(self, max_line_length: int = 80) -> str:
        """Returns the note content formatted for display.

        Args:
            max_line_length: Maximum length for wrapped lines

        Returns:
            str: Formatted note content with wrapped lines
        """
        words = self.content.split()
        lines = []
        current_line = []
        current_length = 0

        for word in words:
            word_length = len(word)
            if current_length + word_length + 1 <= max_line_length:
                current_line.append(word)
                current_length += word_length + 1
            else:
                lines.append(" ".join(current_line))
                current_line = [word]
                current_length = word_length + 1

        if current_line:
            lines.append(" ".join(current_line))

        return "\n".join(lines)