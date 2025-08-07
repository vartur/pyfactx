from datetime import datetime
from typing import Optional, override
from lxml import etree as ET

from pydantic import Field, field_validator

from .InvoiceProfile import InvoiceProfile
from .XMLBaseModel import XMLBaseModel
from .namespaces import NAMESPACES, RAM, UDT


class TradePaymentTerms(XMLBaseModel):
    """Represents payment terms in a trade context according to UN/CEFACT standards.
    
    This class models the conditions under which payment should be made,
    including description, due date, and direct debit information.
    
    Attributes:
        description: Textual description of payment terms
        due_date: The date by which payment should be made
        direct_debit_mandate_id: Identifier for direct debit mandate
    """

    description: Optional[str] = Field(
        default=None,
        description="Textual description of payment terms",
        max_length=512
    )

    due_date: Optional[datetime] = Field(
        default=None,
        description="Date by which payment should be made"
    )

    direct_debit_mandate_id: Optional[str] = Field(
        default=None,
        description="Identifier for direct debit mandate",
        max_length=70  # Common limit for mandate IDs
    )

    @field_validator('description')
    def validate_description(cls, v: Optional[str]) -> Optional[str]:
        """Validates the payment terms description.
        
        Args:
            v: The description to validate
            
        Returns:
            Optional[str]: The validated description
            
        Raises:
            ValueError: If the description is empty or contains only whitespace
        """
        if v is not None:
            v = v.strip()
            if not v:
                raise ValueError("Description cannot be empty or contain only whitespace")
        return v

    @field_validator('direct_debit_mandate_id')
    def validate_mandate_id(cls, v: Optional[str]) -> Optional[str]:
        """Validates the direct debit mandate ID.
        
        Args:
            v: The mandate ID to validate
            
        Returns:
            Optional[str]: The validated mandate ID
            
        Raises:
            ValueError: If the mandate ID contains invalid characters
        """
        if v is not None:
            v = v.strip()
            if not v:
                raise ValueError("Mandate ID cannot be empty or contain only whitespace")
            if not v.isalnum() and not set(v).issubset(
                    set('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_+')):
                raise ValueError("Mandate ID contains invalid characters")
        return v

    @override
    def to_xml(self, element_name: str, _profile: InvoiceProfile) -> ET.Element:
        """Converts the payment terms to XML representation.

        Creates an XML element representing payment terms according to
        the Cross Industry Invoice (CII) XML schema.

        Args:
            element_name: The name to use for the root XML element
            _profile: The invoice profile (unused in this implementation)

        Returns:
            ET.Element: An XML element representing the payment terms

        Example:
            ```xml
            <ram:SpecifiedTradePaymentTerms>
                <ram:Description>Payment within 30 days</ram:Description>
                <ram:DueDateDateTime>
                    <udt:DateTimeString format="102">20240906</udt:DateTimeString>
                </ram:DueDateDateTime>
                <ram:DirectDebitMandateID>MANDATE123</ram:DirectDebitMandateID>
            </ram:SpecifiedTradePaymentTerms>
            ```
        """
        root = ET.Element(f"{{{NAMESPACES[RAM]}}}{element_name}")

        # Description
        if self.description:
            ET.SubElement(root, f"{{{NAMESPACES[RAM]}}}Description").text = self.description

        # DueDateDateTime
        if self.due_date:
            due_date_elem = ET.SubElement(root, f"{{{NAMESPACES[RAM]}}}DueDateDateTime")
            ET.SubElement(
                due_date_elem,
                f"{{{NAMESPACES[UDT]}}}DateTimeString",
                attrib={"format": "102"}
            ).text = self.due_date.strftime("%Y%m%d")

        # DirectDebitMandateID
        if self.direct_debit_mandate_id:
            ET.SubElement(
                root,
                f"{{{NAMESPACES[RAM]}}}DirectDebitMandateID"
            ).text = self.direct_debit_mandate_id

        return root

    def __str__(self) -> str:
        """Returns a human-readable string representation.

        Returns:
            str: Description of the payment terms
        """
        parts = []
        if self.description:
            parts.append(self.description)
        if self.due_date:
            parts.append(f"Due: {self.due_date.strftime('%Y-%m-%d')}")
        if self.direct_debit_mandate_id:
            parts.append(f"Mandate: {self.direct_debit_mandate_id}")
        return " | ".join(parts) if parts else "No payment terms specified"
