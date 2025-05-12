from typing import Optional

from pydantic import BaseModel, Field

from .InvoiceProfile import InvoiceProfile
from .InvoiceTypeCode import InvoiceTypeCode
from .Note import Note

class ExchangedDocument(BaseModel):
    id: str = Field(...)
    type_code: InvoiceTypeCode = Field(default=InvoiceTypeCode.COMMERCIAL_INVOICE)
    issue_date_time: str = Field(...)
    included_notes: Optional[list[Note]] = Field(default=None)

    def to_xml(self, profile: InvoiceProfile = InvoiceProfile.MINIMUM):
        xml_string = "<rsm:ExchangedDocument>"
        xml_string += f"<ram:ID>{self.id}</ram:ID>"
        xml_string += self.type_code.to_xml()

        xml_string += f'''<ram:IssueDateTime>
                                <udt:DateTimeString format="102">{self.issue_date_time}</udt:DateTimeString>
                            </ram:IssueDateTime>'''

        if profile != InvoiceProfile.MINIMUM:
            for note in self.included_notes:
                xml_string += note.to_xml()

        xml_string += "</rsm:ExchangedDocument>"
        return xml_string
