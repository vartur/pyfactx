from typing import Optional, ClassVar
from lxml import etree as ET
from pydantic import Field, field_validator
from typing_extensions import override
import re

from .InvoiceProfile import InvoiceProfile
from .XMLBaseModel import XMLBaseModel
from .namespaces import NAMESPACES, RAM, RSM


class ExchangedDocumentContext(XMLBaseModel):
    """Represents the context information for an exchanged document in Factur-X format.

    This class defines the business process and guideline parameters that provide
    context for electronic invoice documents according to EN16931 standard.

    Attributes:
        business_process_specified_document_context_parameter (Optional[str]): 
            Optional identifier for the business process context.
        guideline_specified_document_context_parameter (InvoiceProfile):
            The invoice profile guideline being used.

    Example:
        ```python
        context = ExchangedDocumentContext(
            business_process_specified_document_context_parameter="ORDER-1",
            guideline_specified_document_context_parameter=InvoiceProfile.EN16931
        )
        ```
    """

    # Class constants for validation
    MAX_BUSINESS_PROCESS_ID_LENGTH: ClassVar[int] = 50
    BUSINESS_PROCESS_ID_PATTERN: ClassVar[str] = r'^[A-Za-z0-9\-/_\.\(\)]+$'

    business_process_specified_document_context_parameter: Optional[str] = Field(
        default=None,
        description="Identifier for the business process context",
        max_length=MAX_BUSINESS_PROCESS_ID_LENGTH
    )

    guideline_specified_document_context_parameter: InvoiceProfile = Field(
        ...,
        description="Invoice profile guideline being used"
    )

    @field_validator('business_process_specified_document_context_parameter')
    def validate_business_process_id(cls, v: Optional[str]) -> Optional[str]:
        """Validates the business process identifier format.

        Args:
            v (Optional[str]): Business process identifier to validate.

        Returns:
            Optional[str]: Validated business process identifier.

        Raises:
            ValueError: If the identifier format is invalid.
        """
        if v is not None:
            # Remove leading/trailing whitespace
            v = v.strip()

            if not v:
                raise ValueError("Business process ID cannot be empty if provided")

            if not re.match(cls.BUSINESS_PROCESS_ID_PATTERN, v):
                raise ValueError(
                    "Business process ID can only contain letters, numbers, "
                    "and the following characters: -/_.()"
                )

            if len(v) > cls.MAX_BUSINESS_PROCESS_ID_LENGTH:
                raise ValueError(
                    f"Business process ID length cannot exceed "
                    f"{cls.MAX_BUSINESS_PROCESS_ID_LENGTH} characters"
                )

        return v

    @field_validator('guideline_specified_document_context_parameter')
    def validate_guideline(cls, v: InvoiceProfile) -> InvoiceProfile:
        """Validates the guideline parameter.

        Args:
            v (InvoiceProfile): Profile guideline to validate.

        Returns:
            InvoiceProfile: Validated profile guideline.

        Raises:
            ValueError: If the guideline is invalid.
        """
        if not isinstance(v, InvoiceProfile):
            valid_values = [str(p.value) for p in InvoiceProfile]
            raise ValueError(
                f"Invalid guideline specified: {v}. "
                f"Must be one of: {', '.join(valid_values)}"
            )
        return v

    def get_guideline_version(self) -> str:
        """Gets the version of the guideline being used.

        Returns:
            str: Version identifier based on the profile.
        """
        # Map profiles to their corresponding versions
        version_map = {
            InvoiceProfile.MINIMUM: "1.0",
            InvoiceProfile.BASICWL: "1.0",
            InvoiceProfile.EN16931: "1.0",
            InvoiceProfile.EXTENDED: "1.0",
        }
        return version_map.get(self.guideline_specified_document_context_parameter, "1.0")

    @override
    def to_xml(self, element_name: str, profile: InvoiceProfile) -> ET.Element:
        """Converts the document context to XML format.

        Args:
            element_name (str): Name of the XML element to create.
            profile (InvoiceProfile): The Factur-X profile being used.

        Returns:
            ET.Element: An XML element containing the document context information.

        Raises:
            ValueError: If XML creation fails.
        """
        try:
            root = ET.Element(f"{{{NAMESPACES[RSM]}}}{element_name}")

            # BusinessProcessSpecifiedDocumentContextParameter
            if self.business_process_specified_document_context_parameter:
                business_elem = ET.SubElement(
                    root,
                    f"{{{NAMESPACES[RAM]}}}"
                    "BusinessProcessSpecifiedDocumentContextParameter"
                )
                id_elem = ET.SubElement(business_elem, f"{{{NAMESPACES[RAM]}}}ID")
                id_elem.text = self.business_process_specified_document_context_parameter

            # GuidelineSpecifiedDocumentContextParameter
            guideline_elem = ET.SubElement(
                root,
                f"{{{NAMESPACES[RAM]}}}GuidelineSpecifiedDocumentContextParameter"
            )
            id_elem = ET.SubElement(guideline_elem, f"{{{NAMESPACES[RAM]}}}ID")
            id_elem.text = profile.value

            return root

        except (ET.XMLSyntaxError, UnicodeEncodeError) as e:
            raise ValueError(f"Failed to create XML element: {str(e)}")

    def __str__(self) -> str:
        """Returns a human-readable string representation of the context."""
        parts = [f"Profile: {self.guideline_specified_document_context_parameter.name}"]
        if self.business_process_specified_document_context_parameter:
            parts.append(
                f"Business Process: "
                f"{self.business_process_specified_document_context_parameter}"
            )
        return "ExchangedDocumentContext(" + ", ".join(parts) + ")"

    @classmethod
    def create_default(cls, profile: InvoiceProfile) -> 'ExchangedDocumentContext':
        """Creates a default document context with specified profile.

        Args:
            profile (InvoiceProfile): The invoice profile to use.

        Returns:
            ExchangedDocumentContext: New document context instance.
        """
        return cls(guideline_specified_document_context_parameter=profile)

    @classmethod
    def create_with_business_process(
            cls,
            profile: InvoiceProfile,
            business_process_id: str
    ) -> 'ExchangedDocumentContext':
        """Creates a document context with business process identifier.

        Args:
            profile (InvoiceProfile): The invoice profile to use.
            business_process_id (str): Business process identifier.

        Returns:
            ExchangedDocumentContext: New document context instance.
        """
        return cls(
            guideline_specified_document_context_parameter=profile,
            business_process_specified_document_context_parameter=business_process_id
        )
