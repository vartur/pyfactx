from typing import Optional
from xml.etree.ElementTree import Element, SubElement

from pydantic import Field
from typing_extensions import override

from .InvoiceProfile import InvoiceProfile
from .XMLBaseModel import XMLBaseModel
from .namespaces import RAM, RSM


class ExchangedDocumentContext(XMLBaseModel):
    business_process_specified_document_context_parameter: Optional[str] = Field(default=None)
    guideline_specified_document_context_parameter: InvoiceProfile = Field(...)

    @override
    def to_xml(self, element_name: str, profile: InvoiceProfile) -> Element:
        root = Element(f"{RSM}:{element_name}")

        # BusinessProcessSpecifiedDocumentContextParameter
        if self.business_process_specified_document_context_parameter:
            business_spec_param_elem = SubElement(root, f"{RAM}:BusinessProcessSpecifiedDocumentContextParameter")
            SubElement(business_spec_param_elem,
                       f"{RAM}:ID").text = self.business_process_specified_document_context_parameter

        # GuidelineSpecifiedDocumentContextParameter
        guideline_spec_param_elem = SubElement(root, f"{RAM}:GuidelineSpecifiedDocumentContextParameter")
        SubElement(guideline_spec_param_elem,
                   f"{RAM}:ID").text = profile

        return root
