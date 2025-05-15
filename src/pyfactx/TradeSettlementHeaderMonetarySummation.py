from typing import Optional, override
from lxml import etree as ET

from pydantic import Field

from .InvoiceProfile import InvoiceProfile
from .XMLBaseModel import XMLBaseModel
from .namespaces import NAMESPACES, RAM


class TradeSettlementHeaderMonetarySummation(XMLBaseModel):
    line_total_amount: Optional[float] = Field(default=None)  # From BASICWL
    charge_total_amount: Optional[float] = Field(default=None)  # From BASICWL
    allowance_total_amount: Optional[float] = Field(default=None)  # From BASICWL
    tax_basis_total_amount: float = Field(...)
    tax_total_amount: Optional[float] = Field(default=None)
    rounding_amount: Optional[float] = Field(default=None)  # From EN16931
    tax_currency_code: Optional[str] = Field(default="EUR")
    grand_total_amount: float = Field(...)
    total_prepaid_amount: Optional[float] = Field(default=None)  # From BASICWL
    due_payable_amount: float = Field(...)

    @override
    def to_xml(self, element_name: str, profile: InvoiceProfile) -> ET.Element:
        root = ET.Element(f"{{{NAMESPACES[RAM]}}}{element_name}")

        if profile >= InvoiceProfile.BASICWL:
            # LineTotalAmount
            if self.line_total_amount:
                ET.SubElement(root, f"{{{NAMESPACES[RAM]}}}LineTotalAmount").text = str(self.line_total_amount)

            # ChargeTotalAmount
            if self.charge_total_amount:
                ET.SubElement(root, f"{{{NAMESPACES[RAM]}}}ChargeTotalAmount").text = str(self.charge_total_amount)

            # AllowanceTotalAmount
            if self.allowance_total_amount:
                ET.SubElement(root, f"{{{NAMESPACES[RAM]}}}AllowanceTotalAmount").text = str(self.allowance_total_amount)

        # TaxBasisTotalAmount
        ET.SubElement(root, f"{{{NAMESPACES[RAM]}}}TaxBasisTotalAmount").text = str(self.tax_basis_total_amount)

        # TaxTotalAmount
        if self.tax_total_amount:
            attrib = {"currencyID": self.tax_currency_code} if self.tax_currency_code else {}
            ET.SubElement(root, f"{{{NAMESPACES[RAM]}}}TaxTotalAmount", attrib=attrib).text = str(self.tax_total_amount)

        if profile >= InvoiceProfile.EN16931:
            if self.rounding_amount:
                ET.SubElement(root, f"{{{NAMESPACES[RAM]}}}RoundingAmount").text = str(self.rounding_amount)

        # GrandTotalAmount
        ET.SubElement(root, f"{{{NAMESPACES[RAM]}}}GrandTotalAmount").text = str(self.grand_total_amount)

        if profile >= InvoiceProfile.BASICWL:
            # TotalPrepaidAmount
            if self.total_prepaid_amount:
                ET.SubElement(root, f"{{{NAMESPACES[RAM]}}}TotalPrepaidAmount").text = str(self.total_prepaid_amount)

        # DuePayableAmount
        ET.SubElement(root, f"{{{NAMESPACES[RAM]}}}DuePayableAmount").text = str(self.due_payable_amount)

        return root
