from typing import Optional
from xml.etree.ElementTree import Element, SubElement

from pydantic import BaseModel, Field

from .InvoiceProfile import InvoiceProfile
from .namespaces import RAM


class TradeSettlementHeaderMonetarySummation(BaseModel):
    line_total_amount: Optional[float] = Field(default=None)  # From BASICWL
    charge_total_amount: Optional[float] = Field(default=None)  # From BASICWL
    allowance_total_amount: Optional[float] = Field(default=None)  # From BASICWL
    tax_basis_total_amount: float = Field(...)
    tax_total_amount: Optional[float] = Field(default=None)
    grand_total_amount: float = Field(...)
    total_prepaid_amount: Optional[float] = Field(default=None)  # From BASICWL
    due_payable_amount: float = Field(...)

    def to_xml(self, element_name: str,  profile: InvoiceProfile, tax_currency_code: str = "EUR") -> Element:
        root = Element(f"{RAM}:{element_name}")

        if profile != InvoiceProfile.MINIMUM:
            # LineTotalAmount
            if self.line_total_amount:
                SubElement(root, f"{RAM}:LineTotalAmount").text = str(self.line_total_amount)

            # ChargeTotalAmount
            if self.charge_total_amount:
                SubElement(root, f"{RAM}:ChargeTotalAmount").text = str(self.charge_total_amount)

            # AllowanceTotalAmount
            if self.allowance_total_amount:
                SubElement(root, f"{RAM}:AllowanceTotalAmount").text = str(self.allowance_total_amount)

        # TaxBasisTotalAmount
        SubElement(root, f"{RAM}:TaxBasisTotalAmount").text = str(self.tax_basis_total_amount)

        # TaxTotalAmount
        if self.tax_total_amount:
            SubElement(root, f"{RAM}:TaxTotalAmount", attrib={"currencyID": tax_currency_code}).text = str(
                self.tax_total_amount)

        # GrandTotalAmount
        SubElement(root, f"{RAM}:GrandTotalAmount").text = str(self.grand_total_amount)

        if profile != InvoiceProfile.MINIMUM:
            # TotalPrepaidAmount
            if self.total_prepaid_amount:
                SubElement(root, f"{RAM}:TotalPrepaidAmount").text = str(self.total_prepaid_amount)

        # DuePayableAmount
        SubElement(root, f"{RAM}:DuePayableAmount").text = str(self.due_payable_amount)

        return root
