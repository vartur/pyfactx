from typing import Optional
from lxml import etree as ET

from pydantic import Field
from typing_extensions import override

from .InvoiceProfile import InvoiceProfile
from .XMLBaseModel import XMLBaseModel
from .namespaces import NAMESPACES, RAM


class TradeSettlementLineMonetarySummation(XMLBaseModel):
    line_total_amount: float = Field(...)
    currency_code: Optional[str] = Field(default=None)

    @override
    def to_xml(self, element_name: str, _profile: InvoiceProfile) -> ET.Element:
        root = ET.Element(f"{{{NAMESPACES[RAM]}}}{element_name}")

        # LineTotalAmount
        attrib = {"currencyID": self.currency_code} if self.currency_code else {}
        ET.SubElement(root, f"{{{NAMESPACES[RAM]}}}LineTotalAmount", attrib=attrib).text = str(self.line_total_amount)

        return root
