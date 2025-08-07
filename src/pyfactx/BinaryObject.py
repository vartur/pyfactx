import base64
import mimetypes
from pathlib import Path
from typing import ClassVar

from lxml import etree as ET
from pydantic import Field, field_validator, computed_field

from .InvoiceProfile import InvoiceProfile
from .XMLBaseModel import XMLBaseModel
from .namespaces import NAMESPACES, RAM


class BinaryObject(XMLBaseModel):
    """A class representing binary content in Factur-X documents.

    This class handles binary attachments in Factur-X XML, supporting the hybrid format
    that combines PDF and XML in accordance with EN 16931 and Factur-X standards.

    Attributes:
        content_b64 (str): The Base64-encoded content of the binary object.
        mime_code (str): The MIME type of the content (e.g., 'application/pdf').
        filename (str): The name of the file including extension.

    Example:
        ```python
        with open('invoice.pdf', 'rb') as f:
            content = base64.b64encode(f.read()).decode('utf-8')
            
        binary_obj = BinaryObject(
            content_b64=content,
            mime_code="application/pdf",
            filename="invoice.pdf"
        )
        ```
    """

    # Class constants for validation
    MAX_FILENAME_LENGTH: ClassVar[int] = 255
    MAX_CONTENT_SIZE: ClassVar[int] = 50 * 1024 * 1024  # 50MB limit
    ALLOWED_MIME_TYPES: ClassVar[set[str]] = {
        'application/pdf',
        'image/png',
        'image/jpeg',
        'image/gif',
        'text/csv',
        'application/xml',
        'text/xml'
    }

    content_b64: str = Field(
        ...,
        description="Base64-encoded binary content",
        min_length=1
    )
    
    mime_code: str = Field(
        ...,
        description="MIME type of the content",
        pattern=r'^[a-z]+/[a-z0-9.+-]+$'
    )
    
    filename: str = Field(
        ...,
        description="Name of the file including extension",
        pattern=r'^[a-zA-Z0-9][a-zA-Z0-9._-]*$'
    )

    @computed_field
    def size(self) -> int:
        """Calculate the size of the decoded binary content in bytes."""
        try:
            return len(base64.b64decode(self.content_b64))
        except Exception:
            return 0

    @field_validator('content_b64')
    def validate_base64(cls, v: str) -> str:
        """Validate that the content is proper base64-encoded data.
        
        Args:
            v (str): Base64-encoded content to validate.
            
        Returns:
            str: Validated base64 content.
            
        Raises:
            ValueError: If content is invalid or exceeds size limit.
        """
        try:
            if not v:
                raise ValueError("Empty base64 content")
            
            # Decode to validate and check size
            content = base64.b64decode(v, validate=True)
            
            if len(content) > cls.MAX_CONTENT_SIZE:
                raise ValueError(
                    f"Content size exceeds maximum allowed size of "
                    f"{cls.MAX_CONTENT_SIZE // (1024*1024)}MB"
                )
            
            return v
        except Exception as e:
            raise ValueError(f"Invalid base64 content: {str(e)}")

    @field_validator('mime_code')
    def validate_mime_code(cls, v: str) -> str:
        """Validate MIME type format and allowed values.
        
        Args:
            v (str): MIME type to validate.
            
        Returns:
            str: Validated MIME type.
            
        Raises:
            ValueError: If MIME type is invalid or not allowed.
        """
        mime_type = v.lower()
        if mime_type not in cls.ALLOWED_MIME_TYPES:
            raise ValueError(
                f"MIME type '{mime_type}' not allowed. "
                f"Allowed types: {', '.join(sorted(cls.ALLOWED_MIME_TYPES))}"
            )
        return mime_type

    @field_validator('filename')
    def validate_filename(cls, v: str) -> str:
        """Validate filename for security and format.
        
        Args:
            v (str): Filename to validate.
            
        Returns:
            str: Validated filename.
            
        Raises:
            ValueError: If filename is invalid or unsafe.
        """
        if len(v) > cls.MAX_FILENAME_LENGTH:
            raise ValueError(
                f"Filename too long (max {cls.MAX_FILENAME_LENGTH} characters)"
            )

        # Prevent directory traversal
        if '..' in v or '/' in v or '\\' in v:
            raise ValueError("Invalid filename: must not contain path separators")

        # Check if the filename is safe
        filename = Path(v).name
        if filename != v:
            raise ValueError("Invalid filename format")

        # Validate file extension matches mime_code
        ext = Path(v).suffix.lower()
        if not ext:
            raise ValueError("Filename must have an extension")

        return v

    def verify_mime_extension_match(self) -> bool:
        """Verify that the file extension matches the MIME type.
        
        Returns:
            bool: True if extension matches MIME type, False otherwise.
        """
        ext = Path(self.filename).suffix.lower()
        expected_types = mimetypes.guess_type(f"file{ext}")[0]
        return expected_types == self.mime_code if expected_types else False

    @classmethod
    def from_file(cls, filepath: str | Path) -> 'BinaryObject':
        """Create a BinaryObject from a file.
        
        Args:
            filepath (str | Path): Path to the file.
            
        Returns:
            BinaryObject: New instance with file content.
            
        Raises:
            ValueError: If file is invalid or cannot be read.
        """
        path = Path(filepath)
        if not path.is_file():
            raise ValueError(f"File not found: {filepath}")

        try:
            with open(path, 'rb') as f:
                content = base64.b64encode(f.read()).decode('utf-8')
            
            mime_type = mimetypes.guess_type(path)[0] or 'application/octet-stream'
            
            return cls(
                content_b64=content,
                mime_code=mime_type,
                filename=path.name
            )
        except Exception as e:
            raise ValueError(f"Failed to read file: {str(e)}")

    def to_file(self, output_dir: str | Path) -> Path:
        """Save the binary content to a file.
        
        Args:
            output_dir (str | Path): Directory to save the file.
            
        Returns:
            Path: Path to the saved file.
            
        Raises:
            ValueError: If file cannot be saved.
        """
        out_dir = Path(output_dir)
        if not out_dir.is_dir():
            raise ValueError(f"Invalid output directory: {output_dir}")

        try:
            filepath = out_dir / self.filename
            content = base64.b64decode(self.content_b64)
            
            with open(filepath, 'wb') as f:
                f.write(content)
            
            return filepath
        except Exception as e:
            raise ValueError(f"Failed to save file: {str(e)}")

    def to_xml(self, element_name: str, profile: InvoiceProfile) -> ET.Element:
        """Converts the binary object to an XML element.

        Args:
            element_name (str): Name of the XML element to create.
            profile (InvoiceProfile): The Factur-X profile being used.

        Returns:
            ET.Element: An XML element containing the binary object data.

        Raises:
            ValueError: If XML creation fails.
        """
        try:
            root = ET.Element(
                f"{{{NAMESPACES[RAM]}}}{element_name}",
                attrib={
                    "mimeCode": self.mime_code,
                    "filename": self.filename
                }
            )
            root.text = self.content_b64
            return root
        except (ET.XMLSyntaxError, UnicodeEncodeError) as e:
            raise ValueError(f"Failed to create XML element: {str(e)}")

    def __str__(self) -> str:
        """Return a string representation of the binary object."""
        return (f"BinaryObject(filename='{self.filename}', "
                f"mime_code='{self.mime_code}', "
                f"size={self.size} bytes)")