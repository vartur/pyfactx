from typing import override
from lxml import etree as ET

from .InvoiceProfile import InvoiceProfile
from .FacturXBasic import FacturXBasic


class FacturXEN16931(FacturXBasic):

    @override
    def to_xml(self, element_name: str = "CrossIndustryInvoice",
               profile: InvoiceProfile = InvoiceProfile.EN16931) -> ET.Element:
        return super().to_xml(element_name, profile)
