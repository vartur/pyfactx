from typing import Optional, override
from lxml import etree as ET

from pydantic import Field, field_validator, ConfigDict
import re

from .InvoiceProfile import InvoiceProfile
from .XMLBaseModel import XMLBaseModel
from .namespaces import NAMESPACES, RAM


class TradeSettlementFinancialCard(XMLBaseModel):
    """Represents financial card information for trade settlement.
    
    This class models payment card details according to UN/CEFACT standards,
    with appropriate security measures for handling sensitive data.
    
    Attributes:
        id: Masked or tokenized card number (last 4-6 digits only)
        cardholder_name: Name of the cardholder (optional)
    """
    
    model_config = ConfigDict(
        validate_assignment=True,
        strict=True,
        frozen=True  # Immutable to prevent modification of sensitive data
    )

    id: str = Field(
        ...,
        description="Masked or tokenized card number",
        min_length=4,
        max_length=50,
        examples=["XXXX-XXXX-XXXX-1234", "XXXXXXXXXXXX5678"]
    )

    cardholder_name: Optional[str] = Field(
        default=None,
        description="Name of the cardholder",
        max_length=70,  # Common limit for card holder names
        pattern=r'^[A-Za-z\s\-\'\.]+$'  # Allow letters, spaces, hyphens, apostrophes, and dots
    )

    @field_validator('id')
    def validate_card_id(cls, v: str) -> str:
        """Validates the card identifier.
        
        Ensures the card number is properly masked/tokenized and
        contains only allowed characters.
        
        Args:
            v: The card identifier to validate
            
        Returns:
            str: The validated card identifier
            
        Raises:
            ValueError: If the card identifier format is invalid
        """
        # Remove any spaces or hyphens for validation
        cleaned = re.sub(r'[\s\-]', '', v)
        
        # Check for valid format (masked number)
        if not re.match(r'^[X*]{6,12}\d{4,6}$', cleaned):
            raise ValueError(
                "Card ID must be masked with X or * and show only last 4-6 digits"
            )
        
        return v.strip()

    @field_validator('cardholder_name')
    def validate_cardholder_name(cls, v: Optional[str]) -> Optional[str]:
        """Validates the cardholder name.
        
        Args:
            v: The cardholder name to validate
            
        Returns:
            Optional[str]: The validated cardholder name
            
        Raises:
            ValueError: If the name format is invalid
        """
        if v is not None:
            v = v.strip()
            if not v:
                raise ValueError("Cardholder name cannot be empty or whitespace only")
            
            # Check for minimum name length (at least 2 characters)
            if len(v) < 2:
                raise ValueError("Cardholder name must be at least 2 characters long")
            
            # Check for reasonable word count (1-4 words)
            words = v.split()
            if not 1 <= len(words) <= 4:
                raise ValueError("Cardholder name must contain 1-4 words")
            
            # Check each word for minimum length
            if any(len(word) < 2 for word in words):
                raise ValueError("Each name part must be at least 2 characters long")
        
        return v

    @override
    def to_xml(self, element_name: str, profile: InvoiceProfile) -> ET.Element:
        """Converts the financial card information to XML representation.

        Creates an XML element representing the card details according to
        the Cross Industry Invoice (CII) XML schema.

        Args:
            element_name: The name to use for the root XML element
            profile: The invoice profile containing serialization settings

        Returns:
            ET.Element: An XML element representing the card details

        Example:
            ```xml
            <ram:ApplicableTradeSettlementFinancialCard>
                <ram:ID>XXXX-XXXX-XXXX-1234</ram:ID>
                <ram:CardholderName>John Doe</ram:CardholderName>
            </ram:ApplicableTradeSettlementFinancialCard>
            ```
        """
        root = ET.Element(f"{{{NAMESPACES[RAM]}}}{element_name}")

        # ID
        ET.SubElement(root, f"{{{NAMESPACES[RAM]}}}ID").text = self.id

        # CardholderName
        if self.cardholder_name:
            ET.SubElement(
                root,
                f"{{{NAMESPACES[RAM]}}}CardholderName"
            ).text = self.cardholder_name

        return root

    def __str__(self) -> str:
        """Returns a human-readable string representation.

        Returns:
            str: Description of the financial card
        """
        parts = [f"Card: {self.id}"]
        if self.cardholder_name:
            parts.append(f"Holder: {self.cardholder_name}")
        return " | ".join(parts)

    def __repr__(self) -> str:
        """Returns a secure string representation.

        Returns:
            str: Secure representation of the financial card
        """
        # Use a more secure representation that doesn't show the full card number
        return f"TradeSettlementFinancialCard(id='***{self.id[-4:]}'"