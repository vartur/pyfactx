from xml.etree.ElementTree import Element

from .FacturXMinimum import FacturXMinimum
from .InvoiceProfile import InvoiceProfile


class FacturXBasicWL(FacturXMinimum):

    def to_xml(self, profile: InvoiceProfile = InvoiceProfile.BASICWL) -> Element:
        return super().to_xml(InvoiceProfile.BASICWL)
