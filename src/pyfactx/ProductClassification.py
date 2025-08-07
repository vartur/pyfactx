from typing import Optional, Dict, ClassVar
from lxml import etree as ET
from typing_extensions import override

from pydantic import Field, field_validator, ConfigDict

from .InvoiceProfile import InvoiceProfile
from .XMLBaseModel import XMLBaseModel
from .namespaces import NAMESPACES, RAM


class ProductClassification(XMLBaseModel):
    """Represents a product classification in the invoice.

    This class models product classification information according to standard
    classification schemes (e.g., UNSPSC, CPV, eCl@ss).

    Attributes:
        list_id: Identifier of the classification scheme (e.g., "UNSPSC", "CPV")
        class_code: Classification code from the specified scheme

    Examples:
        >>> unspsc = ProductClassification(
        ...     list_id="UNSPSC",
        ...     class_code="43211508"  # Desktop computers
        ... )
        >>> cpv = ProductClassification(
        ...     list_id="CPV",
        ...     class_code="30213000-5"  # Laptop computers
        ... )
    """

    KNOWN_CLASSIFICATION_SCHEMES: ClassVar[Dict[str, str]] = {
        "UNSPSC": "United Nations Standard Products and Services Code",
        "CPV": "Common Procurement Vocabulary",
        "ECLASS": "eCl@ss Classification",
        "GPC": "Global Product Classification",
        "TARIC": "EU Customs Code",
        "NCM": "Mercosur Common Nomenclature",
        "HS": "Harmonized System",
        "GTIN": "Global Trade Item Number"
    }

    model_config = ConfigDict(
        validate_assignment=True,
        str_strip_whitespace=True
    )

    list_id: Optional[str] = Field(
        default=None,
        description="Identifier of the classification scheme",
        max_length=50,
        examples=list(KNOWN_CLASSIFICATION_SCHEMES.keys())
    )

    class_code: str = Field(
        ...,
        description="Classification code from the specified scheme",
        min_length=1,
        max_length=50,
        examples=["43211508", "30213000-5", "27-23-92-90"]
    )

    @field_validator('list_id')
    def validate_list_id(cls, value: Optional[str]) -> Optional[str]:
        """Validates the classification scheme identifier.

        Args:
            value: Classification scheme ID to validate

        Returns:
            Optional[str]: Validated classification scheme ID or None

        Raises:
            ValueError: If list_id validation fails
        """
        if value is not None:
            # Remove whitespace and convert to uppercase
            value = value.strip().upper()
            
            # Validate known schemes
            if value not in cls.KNOWN_CLASSIFICATION_SCHEMES:
                # Allow custom schemes but warn about unknown ones
                if not all(c.isalnum() or c in '-_' for c in value):
                    raise ValueError(
                        "Classification scheme ID can only contain letters, "
                        "numbers, hyphens and underscores"
                    )
                    
            if len(value) > 50:
                raise ValueError("Classification scheme ID is too long")
                
        return value

    @field_validator('class_code')
    def validate_class_code(cls, value: str) -> str:
        """Validates the classification code.

        Args:
            value: Classification code to validate

        Returns:
            str: Validated classification code

        Raises:
            ValueError: If class_code validation fails
        """
        # Remove whitespace
        value = value.strip()
        
        # Basic format validation
        if not all(c.isalnum() or c in '-._' for c in value):
            raise ValueError(
                "Classification code can only contain letters, numbers, "
                "hyphens, dots and underscores"
            )
            
        # Length validation
        if len(value) > 50:
            raise ValueError("Classification code is too long")
            
        if len(value) < 1:
            raise ValueError("Classification code cannot be empty")
            
        return value

    @override
    def to_xml(self, element_name: str, _profile: InvoiceProfile) -> ET.Element:
        """Converts the product classification to XML format.

        Creates an XML element representing the product classification according to
        the Factur-X specification.

        Args:
            element_name: Name of the root XML element
            _profile: Factur-X profile (unused but required by interface)

        Returns:
            ET.Element: XML element containing the classification data
        """
        root = ET.Element(f"{{{NAMESPACES[RAM]}}}{element_name}")

        # ClassCode with optional listID attribute
        attrib: Dict[str, str] = {}
        if self.list_id:
            attrib["listID"] = self.list_id
            
        class_code_element = ET.SubElement(
            root,
            f"{{{NAMESPACES[RAM]}}}ClassCode",
            attrib=attrib
        )
        class_code_element.text = self.class_code

        return root

    def __str__(self) -> str:
        """Returns a string representation of the classification.

        Returns:
            str: Classification in readable format
        """
        if self.list_id:
            return f"{self.list_id}: {self.class_code}"
        return self.class_code

    def get_scheme_description(self) -> Optional[str]:
        """Returns the description of the classification scheme.

        Returns:
            Optional[str]: Description of the classification scheme if known
        """
        if self.list_id:
            return self.KNOWN_CLASSIFICATION_SCHEMES.get(self.list_id.upper())
        return None

    def is_known_scheme(self) -> bool:
        """Checks if the classification scheme is a known standard.

        Returns:
            bool: True if the scheme is a known standard
        """
        return bool(
            self.list_id and 
            self.list_id.upper() in self.KNOWN_CLASSIFICATION_SCHEMES
        )