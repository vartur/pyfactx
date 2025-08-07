from datetime import datetime
from lxml import etree as ET

from pydantic import Field, field_validator, ConfigDict
from typing_extensions import override

from .InvoiceProfile import InvoiceProfile
from .XMLBaseModel import XMLBaseModel
from .namespaces import NAMESPACES, RAM, UDT


class SupplyChainEvent(XMLBaseModel):
    """Represents a supply chain event in the invoice.

    This class models events in the supply chain according to the Factur-X standard,
    such as delivery dates, shipping events, or other significant timestamps.

    Attributes:
        occurrence_date: The date when the event occurred

    Examples:
        >>> event = SupplyChainEvent(
        ...     occurrence_date=datetime(2025, 8, 7)
        ... )
    """

    model_config = ConfigDict(
        validate_assignment=True,
        str_strip_whitespace=True
    )

    occurrence_date: datetime = Field(
        ...,  # Required field
        description="The date when the event occurred",
        examples=["2025-08-07"]
    )

    @field_validator('occurrence_date')
    def validate_occurrence_date(cls, value: datetime) -> datetime:
        """Validates the occurrence date.

        Args:
            value: Date to validate

        Returns:
            datetime: Validated date

        Raises:
            ValueError: If date validation fails
        """
        # Ensure date is not in the far future or past
        if value.year < 1900 or value.year > 2100:
            raise ValueError("Date must be between years 1900 and 2100")

        # Normalize time to midnight for consistent date handling
        return datetime(value.year, value.month, value.day)

    @override
    def to_xml(self, element_name: str, _profile: InvoiceProfile) -> ET.Element:
        """Converts the supply chain event to XML format.

        Creates an XML element representing the event according to
        the Factur-X specification.

        Args:
            element_name: Name of the root XML element
            _profile: Factur-X profile (unused but required by interface)

        Returns:
            ET.Element: XML element containing the event data
        """
        root = ET.Element(f"{{{NAMESPACES[RAM]}}}{element_name}")

        # OccurrenceDateTime
        occ_date_elem = ET.SubElement(
            root,
            f"{{{NAMESPACES[RAM]}}}OccurrenceDateTime"
        )
        ET.SubElement(
            occ_date_elem,
            f"{{{NAMESPACES[UDT]}}}DateTimeString",
            attrib={"format": "102"}
        ).text = self.occurrence_date.strftime("%Y%m%d")

        return root

    def __str__(self) -> str:
        """Returns a string representation of the event.

        Returns:
            str: Event in readable format
        """
        return f"Supply Chain Event on {self.occurrence_date.date()}"

    def is_future_event(self, reference_date: datetime | None = None) -> bool:
        """Checks if the event occurs in the future.

        Args:
            reference_date: Reference date for comparison (defaults to current date)

        Returns:
            bool: True if the event is in the future
        """
        if reference_date is None:
            reference_date = datetime.now()

        # Normalize reference date to midnight
        reference_date = datetime(
            reference_date.year,
            reference_date.month,
            reference_date.day
        )
        return self.occurrence_date > reference_date

    def days_since(self, reference_date: datetime | None = None) -> int:
        """Calculates days between the event and a reference date.

        Args:
            reference_date: Reference date for calculation (defaults to current date)

        Returns:
            int: Number of days between the event and reference date
        """
        if reference_date is None:
            reference_date = datetime.now()

        # Normalize reference date to midnight
        reference_date = datetime(
            reference_date.year,
            reference_date.month,
            reference_date.day
        )
        return (reference_date - self.occurrence_date).days

    def is_same_day(self, other_date: datetime) -> bool:
        """Checks if the event occurred on the same day as another date.

        Args:
            other_date: Date to compare with

        Returns:
            bool: True if the dates are on the same day
        """
        return (self.occurrence_date.year == other_date.year and
                self.occurrence_date.month == other_date.month and
                self.occurrence_date.day == other_date.day)