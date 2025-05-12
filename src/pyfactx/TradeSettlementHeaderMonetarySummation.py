from typing import Optional

from pydantic import BaseModel, Field

from .InvoiceProfile import InvoiceProfile


class TradeSettlementHeaderMonetarySummation(BaseModel):
    line_total_amount: Optional[float] = Field(default=None)  # From BASICWL
    charge_total_amount: Optional[float] = Field(default=None)  # From BASICWL
    allowance_total_amount: Optional[float] = Field(default=None)  # From BASICWL
    tax_basis_total_amount: float = Field(...)
    tax_total_amount: Optional[float] = Field(default=None)
    grand_total_amount: float = Field(...)
    total_prepaid_amount: Optional[float] = Field(default=None)  # From BASICWL
    due_payable_amount: float = Field(...)

    def to_xml(self, profile: InvoiceProfile = InvoiceProfile.MINIMUM):
        xml_string = "<ram:SpecifiedTradeSettlementHeaderMonetarySummation>"

        if profile != InvoiceProfile.MINIMUM:
            if self.line_total_amount is not None:
                xml_string += f"<ram:LineTotalAmount>{self.line_total_amount}</ram:LineTotalAmount>"

            if self.charge_total_amount is not None:
                xml_string += f"<ram:ChargeTotalAmount>{self.charge_total_amount}</ram:ChargeTotalAmount>"

            if self.allowance_total_amount is not None:
                xml_string += f"<ram:AllowanceTotalAmount>{self.allowance_total_amount}</ram:AllowanceTotalAmount>"

        xml_string += f"<ram:TaxBasisTotalAmount>{self.tax_basis_total_amount}</ram:TaxBasisTotalAmount>"

        if self.tax_total_amount is not None:
            xml_string += f"<ram:TaxTotalAmount currencyID=\"EUR\">{self.tax_total_amount}</ram:TaxTotalAmount>"

        xml_string += f"<ram:GrandTotalAmount>{self.grand_total_amount}</ram:GrandTotalAmount>"

        if profile != InvoiceProfile.MINIMUM:
            if self.total_prepaid_amount is not None:
                xml_string += f"<ram:TotalPrepaidAmount>{self.total_prepaid_amount}</ram:TotalPrepaidAmount>"

        xml_string += f'''<ram:DuePayableAmount>{self.due_payable_amount}</ram:DuePayableAmount>
                            </ram:SpecifiedTradeSettlementHeaderMonetarySummation>'''

        return xml_string
