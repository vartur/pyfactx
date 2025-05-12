from typing import Optional
from xml.etree.ElementTree import Element, SubElement

from pydantic import BaseModel, Field

from .InvoiceProfile import InvoiceProfile
from .TaxCategoryCode import TaxCategoryCode
from .TaxTypeCode import TaxTypeCode
from .TimeReferenceCode import TimeReferenceCode
from .VATExemptionReasonCode import VATExemptionReasonCode
from .namespaces import RAM


class TradeTax(BaseModel):
    calculated_amount: Optional[float] = Field(default=None)
    type_code: TaxTypeCode = Field(...)
    exemption_reason: Optional[str] = Field(default=None)
    basis_amount: Optional[float] = Field(default=None)
    category_code: TaxCategoryCode = Field(...)
    exemption_reason_code: Optional[VATExemptionReasonCode] = Field(default=None)
    due_date_type_code: Optional[TimeReferenceCode] = Field(default=None)
    rate_applicable_percent: Optional[float] = Field(default=None)

    def to_xml(self, element_name: str, profile: InvoiceProfile = InvoiceProfile.MINIMUM) -> Element:
        root = Element(f"{RAM}:{element_name}")

        # CalculatedAmount
        if self.calculated_amount:
            SubElement(root, f"{RAM}:CalculatedAmount").text = str(self.calculated_amount)

        # TypeCode
        SubElement(root, f"{RAM}:TypeCode").text = self.type_code.value()

        # ExemptionReason
        if self.exemption_reason:
            SubElement(root, f"{RAM}:ExemptionReason").text = self.exemption_reason

        # BasisAmount
        if self.basis_amount:
            SubElement(root, f"{RAM}:BasisAmount").text = str(self.basis_amount)

        # CategoryCode
        SubElement(root, f"{RAM}:CategoryCode").text = self.category_code.value()

        # ExemptionReasonCode
        if self.exemption_reason_code:
            SubElement(root, f"{RAM}:ExemptionReasonCode").text = self.exemption_reason_code.value()

        # DueDateTypeCode
        if self.due_date_type_code:
            SubElement(root, f"{RAM}:DueDateTypeCode").text = self.due_date_type_code.value()

        # RateApplicablePercent
        if self.rate_applicable_percent:
            SubElement(root, f"{RAM}:RateApplicablePercent").text = str(self.rate_applicable_percent)

        return root
