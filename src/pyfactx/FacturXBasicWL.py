from xml.etree.ElementTree import Element

from typing_extensions import override

from .FacturXMinimum import FacturXMinimum
from .InvoiceProfile import InvoiceProfile


class FacturXBasicWL(FacturXMinimum):

    @override
    def to_xml(self, element_name: str = "CrossIndustryInvoice",
               profile: InvoiceProfile = InvoiceProfile.BASICWL) -> Element:
        return super().to_xml(element_name, profile)
