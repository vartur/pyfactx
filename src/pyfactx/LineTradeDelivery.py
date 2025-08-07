from typing import Optional
from decimal import Decimal
from lxml import etree as ET

from pydantic import Field, field_validator, ConfigDict
from typing_extensions import override

from .InvoiceProfile import InvoiceProfile
from .UnitCode import UnitCode
from .XMLBaseModel import XMLBaseModel
from .namespaces import NAMESPACES, RAM


class LineTradeDelivery(XMLBaseModel):
    """Represents delivery details for an invoice line item.

    This class models the delivery information for individual line items according to
    Factur-X standards, including quantity and unit of measure.

    Attributes:
        billed_quantity: The quantity being billed for this line item.
            Must be a positive number.
        unit: Unit of measure for the billed quantity (e.g., PCE for pieces).
            Optional but recommended for clarity.

    Examples:
        >>> delivery = LineTradeDelivery(billed_quantity=10.5, unit=UnitCode.PIECE)
        >>> delivery.billed_quantity
        10.5
    """

    model_config = ConfigDict(
        validate_assignment=True,
        str_strip_whitespace=True
    )

    billed_quantity: float = Field(
        ...,
        description="Quantity being billed",
        gt=0,
        lt=1e12,  # Reasonable upper limit to prevent overflow
    )

    unit: Optional[UnitCode] = Field(
        default=None,
        description="Unit of measure for the billed quantity"
    )

    @field_validator('billed_quantity')
    def validate_quantity(cls, value: float) -> float:
        """Validates the billed quantity.

        Args:
            value: Quantity to validate

        Returns:
            The validated quantity

        Raises:
            ValueError: If quantity is invalid or has too many decimal places
        """
        # Convert to Decimal for precise decimal place counting
        decimal_value = Decimal(str(value))
        
        # Check decimal places (max 6 as per common business practice)
        if abs(int(decimal_value.as_tuple().exponent)) > 6:
            raise ValueError("Billed quantity cannot have more than 6 decimal places")
            
        # Ensure it's a finite number
        if not decimal_value.is_finite():
            raise ValueError("Billed quantity must be a finite number")

        return value

    @override
    def to_xml(self, element_name: str, _profile: InvoiceProfile) -> ET.Element:
        """Converts the trade delivery to XML format.

        Creates an XML element representing the line trade delivery according to
        the Factur-X specification.

        Args:
            element_name: Name of the root XML element
            _profile: Factur-X profile (unused but required by interface)

        Returns:
            ET.Element: XML element containing the delivery data

        Examples:
            >>> delivery = LineTradeDelivery(billed_quantity=5, unit=UnitCode.PIECE)
            >>> xml = delivery.to_xml("LineTradeDelivery", InvoiceProfile.MINIMUM)
            >>> xml.find(".//BilledQuantity").text
            '5'
        """
        root = ET.Element(f"{{{NAMESPACES[RAM]}}}{element_name}")

        # Create BilledQuantity element
        quantity_element = ET.SubElement(
            root,
            f"{{{NAMESPACES[RAM]}}}BilledQuantity"
        )

        # Add unit code if present
        if self.unit:
            quantity_element.set("unitCode", self.unit.value)

        # Format quantity with appropriate precision
        quantity_str = format(self.billed_quantity, '.6f').rstrip('0').rstrip('.')
        quantity_element.text = quantity_str

        return root

    def __str__(self) -> str:
        """Returns a string representation of the trade delivery.

        Returns:
            str: Delivery details in readable format
        """
        unit_str = f" {self.unit.value}" if self.unit else ""
        return f"Quantity: {self.billed_quantity}{unit_str}"

    def get_formatted_quantity(self) -> str:
        """Returns the billed quantity formatted according to business rules.

        Returns:
            str: Formatted quantity string with appropriate precision
        """
        return format(self.billed_quantity, '.6f').rstrip('0').rstrip('.')