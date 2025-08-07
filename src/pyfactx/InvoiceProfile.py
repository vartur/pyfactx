from enum import StrEnum
from typing import Dict


class InvoiceProfile(StrEnum):
    """Represents Factur-X invoice profiles as defined by the European standard.
    
    This enum defines the different conformance levels for Factur-X invoices,
    from minimum requirements to extended functionality. Each profile builds upon
    the previous one, adding more required fields and features.
    
    Attributes:
        MINIMUM: The simplest profile with minimal required fields
        BASICWL: Basic profile with whitelist of allowed fields
        BASIC: Basic profile compliant with EN16931
        EN16931: Full European standard implementation
        EXTENDED: Extended profile with additional business fields
        
    The profiles are ordered hierarchically, where each higher level includes
    all the requirements of the lower levels plus additional ones.
    """
    
    MINIMUM = "urn:factur-x.eu:1p0:minimum"
    BASICWL = "urn:factur-x.eu:1p0:basicwl"
    BASIC = "urn:cen.eu:en16931:2017#compliant#urn:factur-x.eu:1p0:basic"
    EN16931 = "urn:cen.eu:en16931:2017"
    EXTENDED = "urn:cen.eu:en16931:2017#conformant#urn:factur-x.eu:1p0:extended"

    def __lt__(self, other: object) -> bool:
        """Compare if this profile is less than another profile.

        Args:
            other: The profile to compare against

        Returns:
            bool: True if this profile is lower than other, False otherwise

        Raises:
            TypeError: If other is not an InvoiceProfile instance
        """
        if not isinstance(other, InvoiceProfile):
            return NotImplemented
        return _invoice_profile_order[str(self.value)] < _invoice_profile_order[str(other.value)]

    def __le__(self, other: object) -> bool:
        """Compare if this profile is less than or equal to another profile.

        Args:
            other: The profile to compare against

        Returns:
            bool: True if this profile is lower or equal to other, False otherwise

        Raises:
            TypeError: If other is not an InvoiceProfile instance
        """
        if not isinstance(other, InvoiceProfile):
            return NotImplemented
        return _invoice_profile_order[str(self.value)] <= _invoice_profile_order[str(other.value)]

    def __gt__(self, other: object) -> bool:
        """Compare if this profile is greater than another profile.

        Args:
            other: The profile to compare against

        Returns:
            bool: True if this profile is higher than other, False otherwise

        Raises:
            TypeError: If other is not an InvoiceProfile instance
        """
        if not isinstance(other, InvoiceProfile):
            return NotImplemented
        return _invoice_profile_order[str(self.value)] > _invoice_profile_order[str(other.value)]

    def __ge__(self, other: object) -> bool:
        """Compare if this profile is greater than or equal to another profile.

        Args:
            other: The profile to compare against

        Returns:
            bool: True if this profile is higher or equal to other, False otherwise

        Raises:
            TypeError: If other is not an InvoiceProfile instance
        """
        if not isinstance(other, InvoiceProfile):
            return NotImplemented
        return _invoice_profile_order[str(self.value)] >= _invoice_profile_order[str(other.value)]


# Define the profile order mapping outside the class
_invoice_profile_order: Dict[str, int] = {
    str(InvoiceProfile.MINIMUM.value): 0,
    str(InvoiceProfile.BASICWL.value): 1,
    str(InvoiceProfile.BASIC.value): 2,
    str(InvoiceProfile.EN16931.value): 3,
    str(InvoiceProfile.EXTENDED.value): 4,
}