from lxml import etree as ET

from typing_extensions import override

from .FacturXMinimum import FacturXMinimum
from .InvoiceProfile import InvoiceProfile


class FacturXBasicWL(FacturXMinimum):

    @override
    def to_xml(self, element_name: str = "CrossIndustryInvoice",
               profile: InvoiceProfile = InvoiceProfile.BASICWL) -> ET.Element:
        return super().to_xml(element_name, profile)
