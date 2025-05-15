from datetime import datetime
from typing import Optional, override
from lxml import etree as ET

from pydantic import Field

from .InvoiceProfile import InvoiceProfile
from .TaxCategoryCode import TaxCategoryCode
from .TaxTypeCode import TaxTypeCode
from .TimeReferenceCode import TimeReferenceCode
from .VATExemptionReasonCode import VATExemptionReasonCode
from .XMLBaseModel import XMLBaseModel
from .namespaces import NAMESPACES, RAM, UDT


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
    def to_xml(self, element_name: str, profile: InvoiceProfile) -> ET.Element:
        root = ET.Element(f"{{{NAMESPACES[RAM]}}}{element_name}")

        # CalculatedAmount
        if self.calculated_amount:
            ET.SubElement(root, f"{{{NAMESPACES[RAM]}}}CalculatedAmount").text = str(self.calculated_amount)

        # TypeCode
        ET.SubElement(root, f"{{{NAMESPACES[RAM]}}}TypeCode").text = self.type_code

        # ExemptionReason
        if self.exemption_reason:
            ET.SubElement(root, f"{{{NAMESPACES[RAM]}}}ExemptionReason").text = self.exemption_reason

        # BasisAmount
        if self.basis_amount:
            ET.SubElement(root, f"{{{NAMESPACES[RAM]}}}BasisAmount").text = str(self.basis_amount)

        # CategoryCode
        ET.SubElement(root, f"{{{NAMESPACES[RAM]}}}CategoryCode").text = self.category_code

        # ExemptionReasonCode
        if self.exemption_reason_code:
            ET.SubElement(root, f"{{{NAMESPACES[RAM]}}}ExemptionReasonCode").text = self.exemption_reason_code

        if profile >= InvoiceProfile.EN16931:
            # TaxPointDate
            if self.tax_point_date:
                tax_point_element = ET.SubElement(root, f"{{{NAMESPACES[RAM]}}}TaxPointDate")
                ET.SubElement(tax_point_element, f"{{{NAMESPACES[UDT]}}}DateString",
                              attrib={"format": "102"}).text = self.tax_point_date.strftime("%Y%m%d")

        # DueDateTypeCode
        if self.due_date_type_code:
            ET.SubElement(root, f"{{{NAMESPACES[RAM]}}}DueDateTypeCode").text = self.due_date_type_code.value

        # RateApplicablePercent
        if self.rate_applicable_percent:
            ET.SubElement(root, f"{{{NAMESPACES[RAM]}}}RateApplicablePercent").text = str(self.rate_applicable_percent)

        return root
