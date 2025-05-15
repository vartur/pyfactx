from typing import Optional
from lxml import etree as ET

from pydantic import Field
from typing_extensions import override

from .InvoiceProfile import InvoiceProfile
from .XMLBaseModel import XMLBaseModel
from .namespaces import NAMESPACES, RAM, RSM


class ExchangedDocumentContext(XMLBaseModel):
    business_process_specified_document_context_parameter: Optional[str] = Field(default=None)
    guideline_specified_document_context_parameter: InvoiceProfile = Field(...)

    @override
    def to_xml(self, element_name: str, profile: InvoiceProfile) -> ET.Element:
        root = ET.Element(f"{{{NAMESPACES[RSM]}}}{element_name}")

        # BusinessProcessSpecifiedDocumentContextParameter
        if self.business_process_specified_document_context_parameter:
            business_spec_param_elem = ET.SubElement(root, f"{{{NAMESPACES[RAM]}}}BusinessProcessSpecifiedDocumentContextParameter")
            ET.SubElement(business_spec_param_elem,
                          f"{{{NAMESPACES[RAM]}}}ID").text = self.business_process_specified_document_context_parameter

        # GuidelineSpecifiedDocumentContextParameter
        guideline_spec_param_elem = ET.SubElement(root, f"{{{NAMESPACES[RAM]}}}GuidelineSpecifiedDocumentContextParameter")
        ET.SubElement(guideline_spec_param_elem,
                      f"{{{NAMESPACES[RAM]}}}ID").text = profile

        return root
