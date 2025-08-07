from typing import Optional
from lxml import etree as ET
from pydantic import Field, field_validator
from typing_extensions import override

from .InvoiceProfile import InvoiceProfile
from .Note import Note
from .XMLBaseModel import XMLBaseModel
from .namespaces import NAMESPACES, RAM


class DocumentLineDocument(XMLBaseModel):
    """Represents a line item document in Factur-X invoice.

    This class handles the documentation aspects of an invoice line item,
    including line identification and optional notes. It is part of the 
    structured data representation of an invoice line, according to EN16931.

    Attributes:
        line_id (int): Unique identifier for the invoice line. Must be positive.
        included_note (Optional[Note]): Additional notes or comments for the line item.
            This field is optional and can contain textual information about the
            line item.

    Example:
        ```python
        line_doc = DocumentLineDocument(
            line_id=1,
            included_note=Note(content="Special handling required"))
        ```
    """

    line_id: int = Field(
        ...,
        description="Unique identifier for the invoice line",
        gt=0,
        lt=1000000  # Reasonable upper limit for line items
    )

    included_note: Optional[Note] = Field(
        default=None,
        description="Optional note or comment for the line item"
    )

    @field_validator('line_id')
    def validate_line_id(cls, v: int) -> int:
        """Validates the line_id value.

        Args:
            v (int): Line ID to validate.

        Returns:
            int: Validated line ID.

        Raises:
            ValueError: If the line ID is invalid.
        """
        if v is None:
            raise ValueError("Line ID is required")

        if not isinstance(v, int):
            raise ValueError("Line ID must be an integer")

        if v <= 0:
            raise ValueError("Line ID must be a positive number")

        if v >= 1000000:
            raise ValueError("Line ID is too large (maximum: 999999)")

        return v

    @field_validator('included_note')
    def validate_included_note(cls, v: Optional[Note]) -> Optional[Note]:
        """Validates the included note if present.

        Args:
            v (Optional[Note]): Note to validate.

        Returns:
            Optional[Note]: Validated note or None.

        Raises:
            ValueError: If the note is invalid.
        """
        if v is not None and not isinstance(v, Note):
            raise ValueError("Included note must be an instance of Note class")
        return v

    @override
    def to_xml(self, element_name: str, profile: InvoiceProfile) -> ET.Element:
        """Converts the document line information to XML format.

        Creates an XML element representing the document line according to
        the Factur-X standard.

        Args:
            element_name (str): Name of the XML element to create.
            profile (InvoiceProfile): The Factur-X profile being used for
                profile-specific formatting.

        Returns:
            ET.Element: An XML element containing the document line information.

        Raises:
            ValueError: If XML creation fails.
        """
        try:
            root = ET.Element(f"{{{NAMESPACES[RAM]}}}{element_name}")

            # LineID - convert to string and ensure it's properly formatted
            line_id_element = ET.SubElement(root, f"{{{NAMESPACES[RAM]}}}LineID")
            line_id_element.text = str(self.line_id)

            # IncludedNote - only append if the note exists
            if self.included_note is not None:
                try:
                    note_element = self.included_note.to_xml("IncludedNote", profile)
                    root.append(note_element)
                except Exception as e:
                    raise ValueError(f"Failed to create included note XML: {str(e)}")

            return root

        except (ET.XMLSyntaxError, UnicodeEncodeError) as e:
            raise ValueError(f"Failed to create XML element: {str(e)}")

    def __str__(self) -> str:
        """Returns a string representation of the document line.

        Returns:
            str: Human-readable representation of the document line.
        """
        note_str = f", Note: {self.included_note}" if self.included_note else ""
        return f"DocumentLine(ID: {self.line_id}{note_str})"

    def __repr__(self) -> str:
        """Returns a detailed string representation of the document line.

        Returns:
            str: Detailed representation of the document line for debugging.
        """
        return (f"DocumentLineDocument(line_id={self.line_id}, "
                f"included_note={repr(self.included_note)})")
