from enum import Enum
from typing import Optional


class DocumentTypeCode(Enum):
    """Document Type Codes as defined in UN/EDIFACT 1001.
    
    This enumeration represents standardized document type codes according to the
    UN/EDIFACT 1001 code list used in electronic business transactions and Factur-X.
    Each code identifies a specific type of business document.

    Attributes:
        VALIDATED_PRICE_TENDER (50): Price/sales catalogue response
            Used for validated price tenders in response to price/sales catalogue.
            
        INVOICING_DATA_SHEET (130): Invoicing data sheet
            Document used for providing invoicing information.
            
        RELATED_DOCUMENT (916): Related document
            Document that has a relationship with the referenced document.

    Example:
        ```python
        # Using the enum
        doc_type = DocumentTypeCode.INVOICING_DATA_SHEET
        print(doc_type.value)  # Outputs: 130
        print(doc_type.name)   # Outputs: "INVOICING_DATA_SHEET"
        ```

    References:
        - UN/EDIFACT 1001: https://unece.org/trade/uncefact/unedifact
        - Factur-X Documentation: https://www.ferd-net.de/standards/factur-x/
    """

    VALIDATED_PRICE_TENDER = 50
    INVOICING_DATA_SHEET = 130
    RELATED_DOCUMENT = 916

    @classmethod
    def get_description(cls, code: 'DocumentTypeCode') -> str:
        """Returns a human-readable description of the document type code.

        Args:
            code (DocumentTypeCode): The document type code enum value.

        Returns:
            str: Description of the document type.

        Example:
            ```python
            description = DocumentTypeCode.get_description(
                DocumentTypeCode.INVOICING_DATA_SHEET
            )
            print(description)  # Outputs: "Invoicing data sheet document..."
            ```
        """
        descriptions = {
            cls.VALIDATED_PRICE_TENDER: (
                "Price/sales catalogue response used for validated price tenders"
            ),
            cls.INVOICING_DATA_SHEET: (
                "Invoicing data sheet document used for providing "
                "invoicing information"
            ),
            cls.RELATED_DOCUMENT: (
                "Document that has a relationship with the referenced document"
            )
        }
        return descriptions.get(code, "Unknown document type")

    @classmethod
    def from_code(cls, code: int) -> Optional['DocumentTypeCode']:
        """Creates a DocumentTypeCode enum from a numeric code.

        Args:
            code (int): The numeric code value.

        Returns:
            Optional[DocumentTypeCode]: The corresponding enum value,
                or None if not found.

        Example:
            ```python
            doc_type = DocumentTypeCode.from_code(130)
            if doc_type:
                print(doc_type.name)  # Outputs: "INVOICING_DATA_SHEET"
            ```
        """
        try:
            return cls(code)
        except ValueError:
            return None

    def __str__(self) -> str:
        """Returns a human-readable string representation of the document type.

        Returns:
            str: String representation including code and description.

        Example:
            ```python
            doc_type = DocumentTypeCode.INVOICING_DATA_SHEET
            print(str(doc_type))
            # Outputs: "INVOICING_DATA_SHEET (130): Invoicing data sheet..."
            ```
        """
        return f"{self.name} ({self.value}): {self.get_description(self)}"

    @classmethod
    def is_valid_code(cls, code: int) -> bool:
        """Checks if a numeric code is a valid document type code.

        Args:
            code (int): The numeric code to validate.

        Returns:
            bool: True if the code is valid, False otherwise.

        Example:
            ```python
            is_valid = DocumentTypeCode.is_valid_code(130)
            print(is_valid)  # Outputs: True
            ```
        """
        return any(code == member.value for member in cls)

    @classmethod
    def get_all_codes(cls) -> list[tuple[int, str]]:
        """Returns all available document type codes with their descriptions.

        Returns:
            list[tuple[int, str]]: List of tuples containing code values
                and their descriptions.

        Example:
            ```python
            codes = DocumentTypeCode.get_all_codes()
            for code, desc in codes:
                print(f"{code}: {desc}")
            ```
        """
        return [(member.value, cls.get_description(member)) 
                for member in cls]