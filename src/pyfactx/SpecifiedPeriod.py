from datetime import datetime
from typing import Optional, override
from lxml import etree as ET

from pydantic import Field, field_validator, ConfigDict, model_validator

from .InvoiceProfile import InvoiceProfile
from .XMLBaseModel import XMLBaseModel
from .namespaces import NAMESPACES, RAM, UDT


class SpecifiedPeriod(XMLBaseModel):
    """Represents a time period specification in the invoice.

    This class models a time period with optional start and end dates according
    to the Factur-X standard. Used for specifying invoice periods, delivery periods,
    or other time-based ranges.

    Attributes:
        start_date: The beginning date of the period
        end_date: The ending date of the period

    Examples:
        >>> period = SpecifiedPeriod(
        ...     start_date=datetime(2025, 1, 1),
        ...     end_date=datetime(2025, 12, 31)
        ... )
    """

    model_config = ConfigDict(
        validate_assignment=True,
        str_strip_whitespace=True
    )

    start_date: Optional[datetime] = Field(
        default=None,
        description="The beginning date of the period",
        examples=["2025-01-01"]
    )

    end_date: Optional[datetime] = Field(
        default=None,
        description="The ending date of the period",
        examples=["2025-12-31"]
    )

    @field_validator('start_date', 'end_date')
    def validate_date(cls, value: Optional[datetime]) -> Optional[datetime]:
        """Validates date values.

        Args:
            value: Date to validate

        Returns:
            Optional[datetime]: Validated date or None

        Raises:
            ValueError: If date validation fails
        """
        if value is not None:
            # Ensure date is not in the far future or past
            if value.year < 1900 or value.year > 2100:
                raise ValueError("Date must be between years 1900 and 2100")
            
            # Normalize time to midnight for consistent date handling
            return datetime(value.year, value.month, value.day)
        return value

    @model_validator(mode='after')
    def validate_period(self) -> 'SpecifiedPeriod':
        """Validates the period as a whole.

        Returns:
            SpecifiedPeriod: The validated period instance

        Raises:
            ValueError: If period validation fails
        """
        if self.start_date and self.end_date:
            if self.start_date > self.end_date:
                raise ValueError("Start date must not be later than end date")
            
            # Check for reasonable period length (e.g., 100 years)
            years_diff = self.end_date.year - self.start_date.year
            if years_diff > 100:
                raise ValueError("Period cannot exceed 100 years")

        return self

    @override
    def to_xml(self, element_name: str, _profile: InvoiceProfile) -> ET.Element:
        """Converts the period to XML format.

        Creates an XML element representing the period according to
        the Factur-X specification.

        Args:
            element_name: Name of the root XML element
            _profile: Factur-X profile (unused but required by interface)

        Returns:
            ET.Element: XML element containing the period data
        """
        root = ET.Element(f"{{{NAMESPACES[RAM]}}}{element_name}")

        # StartDateTime
        if self.start_date:
            start_elem = ET.SubElement(
                root,
                f"{{{NAMESPACES[RAM]}}}StartDateTime"
            )
            ET.SubElement(
                start_elem,
                f"{{{NAMESPACES[UDT]}}}DateTimeString",
                attrib={"format": "102"}
            ).text = self.start_date.strftime("%Y%m%d")

        # EndDateTime
        if self.end_date:
            end_elem = ET.SubElement(
                root,
                f"{{{NAMESPACES[RAM]}}}EndDateTime"
            )
            ET.SubElement(
                end_elem,
                f"{{{NAMESPACES[UDT]}}}DateTimeString",
                attrib={"format": "102"}
            ).text = self.end_date.strftime("%Y%m%d")

        return root

    def __str__(self) -> str:
        """Returns a string representation of the period.

        Returns:
            str: Period in readable format
        """
        if self.start_date and self.end_date:
            return f"From {self.start_date.date()} to {self.end_date.date()}"
        elif self.start_date:
            return f"Starting from {self.start_date.date()}"
        elif self.end_date:
            return f"Until {self.end_date.date()}"
        return "Unspecified period"

    def duration_days(self) -> Optional[int]:
        """Calculates the duration of the period in days.

        Returns:
            Optional[int]: Number of days in the period, or None if incomplete
        """
        if self.start_date and self.end_date:
            return (self.end_date - self.start_date).days
        return None

    def contains_date(self, date: datetime) -> bool:
        """Checks if a given date falls within the period.

        Args:
            date: Date to check

        Returns:
            bool: True if the date is within the period
        """
        # Normalize input date to midnight
        date = datetime(date.year, date.month, date.day)
        
        if self.start_date and self.end_date:
            return self.start_date <= date <= self.end_date
        elif self.start_date:
            return date >= self.start_date
        elif self.end_date:
            return date <= self.end_date
        return True  # Unspecified period contains all dates

    def overlaps(self, other: 'SpecifiedPeriod') -> bool:
        """Checks if this period overlaps with another period.

        Args:
            other: Another period to check for overlap

        Returns:
            bool: True if the periods overlap
        """
        if not (self.start_date or self.end_date or 
                other.start_date or other.end_date):
            return True  # Both periods unspecified

        # Handle cases where one or both periods have no start/end
        if not self.start_date and not other.end_date:
            return True
        if not self.end_date and not other.start_date:
            return True
            
        if self.start_date and self.end_date and \
           other.start_date and other.end_date:
            return (self.start_date <= other.end_date and 
                    other.start_date <= self.end_date)
                    
        return False