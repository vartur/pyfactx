from typing import Optional

from pydantic import BaseModel, Field

from .InvoiceProfile import InvoiceProfile


class ExchangedDocumentContext(BaseModel):
    business_process_specified_document_context_parameter: Optional[str] = Field(default=None)
    guideline_specified_document_context_parameter: InvoiceProfile = Field(...)

    def to_xml(self):
        xml_string = "<rsm:ExchangedDocumentContext>"

        if self.business_process_specified_document_context_parameter is not None:
            xml_string += f'''<ram:BusinessProcessSpecifiedDocumentContextParameter>
                                    <ram:ID>{self.business_process_specified_document_context_parameter}</ram:ID>
                                </ram:BusinessProcessSpecifiedDocumentContextParameter>'''

        xml_string += f'''<ram:GuidelineSpecifiedDocumentContextParameter>
                                {self.guideline_specified_document_context_parameter.to_xml()}
                            </ram:GuidelineSpecifiedDocumentContextParameter>'''

        xml_string += "</rsm:ExchangedDocumentContext>"
        return xml_string
