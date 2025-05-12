from enum import StrEnum


class InvoiceProfile(StrEnum):
    MINIMUM = "urn:factur-x.eu:1p0:minimum"
    BASICWL = "urn:factur-x.eu:1p0:basicwl"
    BASIC = "urn:cen.eu:en16931:2017#compliant#urn:factur-x.eu:1p0:basic"
    EN16931 = "urn:cen.eu:en16931:2017"
    EXTENDED = "urn:cen.eu:en16931:2017#conformant#urn:factur-x.eu:1p0:extended"
