from lxml import etree as ET

from typing_extensions import override

from .FacturXBasicWL import FacturXBasicWL
from .InvoiceProfile import InvoiceProfile


class FacturXBasic(FacturXBasicWL):

    @override
    def to_xml(self, element_name: str = "CrossIndustryInvoice",
               profile: InvoiceProfile = InvoiceProfile.BASIC) -> ET.Element:
        return super().to_xml(element_name, profile)
