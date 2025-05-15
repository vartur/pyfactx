from enum import StrEnum


class InvoiceProfile(StrEnum):
    MINIMUM = "urn:factur-x.eu:1p0:minimum"
    BASICWL = "urn:factur-x.eu:1p0:basicwl"
    BASIC = "urn:cen.eu:en16931:2017#compliant#urn:factur-x.eu:1p0:basic"
    EN16931 = "urn:cen.eu:en16931:2017"
    EXTENDED = "urn:cen.eu:en16931:2017#conformant#urn:factur-x.eu:1p0:extended"

    def __lt__(self, other):
        if isinstance(other, InvoiceProfile):
            return _invoice_profile_order[self.value] < _invoice_profile_order[other.value]
        return NotImplemented

    def __le__(self, other):
        if isinstance(other, InvoiceProfile):
            return _invoice_profile_order[self.value] <= _invoice_profile_order[other.value]
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, InvoiceProfile):
            return _invoice_profile_order[self.value] > _invoice_profile_order[other.value]
        return NotImplemented

    def __ge__(self, other):
        if isinstance(other, InvoiceProfile):
            return _invoice_profile_order[self.value] >= _invoice_profile_order[other.value]
        return NotImplemented


_invoice_profile_order = {
    InvoiceProfile.MINIMUM.value: 0,
    InvoiceProfile.BASICWL.value: 1,
    InvoiceProfile.BASIC.value: 2,
    InvoiceProfile.EN16931.value: 3,
    InvoiceProfile.EXTENDED.value: 4,
}
