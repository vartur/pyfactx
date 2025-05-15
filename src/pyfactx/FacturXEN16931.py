from typing import override
from xml.etree.ElementTree import Element

from .InvoiceProfile import InvoiceProfile
from .FacturXBasic import FacturXBasic


class FacturXEN16931(FacturXBasic):

    @override
    def to_xml(self, element_name: str = "CrossIndustryInvoice",
               profile: InvoiceProfile = InvoiceProfile.EN16931) -> Element:
        return super().to_xml(element_name, profile)
