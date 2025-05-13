from xml.etree.ElementTree import Element

from .FacturXBasicWL import FacturXBasicWL
from .InvoiceProfile import InvoiceProfile


class FacturXBasic(FacturXBasicWL):

    def to_xml(self, profile: InvoiceProfile = InvoiceProfile.BASIC) -> Element:
        return super().to_xml(InvoiceProfile.BASIC)
