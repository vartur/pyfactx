from datetime import datetime
from typing import Optional, override
from xml.etree.ElementTree import Element, SubElement

from pydantic import Field

from .InvoiceProfile import InvoiceProfile
from .TaxCategoryCode import TaxCategoryCode
from .TaxTypeCode import TaxTypeCode
from .TimeReferenceCode import TimeReferenceCode
from .VATExemptionReasonCode import VATExemptionReasonCode
from .XMLBaseModel import XMLBaseModel
from .namespaces import RAM, UDT


class TradeTax(XMLBaseModel):
    calculated_amount: Optional[float] = Field(default=None)
    type_code: TaxTypeCode = Field(...)
    exemption_reason: Optional[str] = Field(default=None)
    basis_amount: Optional[float] = Field(default=None)
    category_code: TaxCategoryCode = Field(...)
    exemption_reason_code: Optional[VATExemptionReasonCode] = Field(default=None)
    tax_point_date: Optional[datetime] = Field(default=None)  # From EN16931
    due_date_type_code: Optional[TimeReferenceCode] = Field(default=None)
    rate_applicable_percent: Optional[float] = Field(default=None)

    @override
    def to_xml(self, element_name: str, profile: InvoiceProfile) -> Element:
        root = Element(f"{RAM}:{element_name}")

        # CalculatedAmount
        if self.calculated_amount:
            SubElement(root, f"{RAM}:CalculatedAmount").text = str(self.calculated_amount)

        # TypeCode
        SubElement(root, f"{RAM}:TypeCode").text = self.type_code

        # ExemptionReason
        if self.exemption_reason:
            SubElement(root, f"{RAM}:ExemptionReason").text = self.exemption_reason

        # BasisAmount
        if self.basis_amount:
            SubElement(root, f"{RAM}:BasisAmount").text = str(self.basis_amount)

        # CategoryCode
        SubElement(root, f"{RAM}:CategoryCode").text = self.category_code

        # ExemptionReasonCode
        if self.exemption_reason_code:
            SubElement(root, f"{RAM}:ExemptionReasonCode").text = self.exemption_reason_code

        if profile >= InvoiceProfile.EN16931:
            # TaxPointDate
            if self.tax_point_date:
                tax_point_element = SubElement(root, f"{RAM}:TaxPointDate")
                SubElement(tax_point_element, f"{UDT}:DateString",
                           attrib={"format": "102"}).text = self.tax_point_date.strftime("%Y%m%d")

        # DueDateTypeCode
        if self.due_date_type_code:
            SubElement(root, f"{RAM}:DueDateTypeCode").text = self.due_date_type_code.value

        # RateApplicablePercent
        if self.rate_applicable_percent:
            SubElement(root, f"{RAM}:RateApplicablePercent").text = str(self.rate_applicable_percent)

        return root
