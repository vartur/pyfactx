from typing import Optional

from pydantic import BaseModel, Field


class Note(BaseModel):
    content: str = Field(...)
    subject_code: Optional[str] = Field(default=None)  # https://service.unece.org/trade/untdid/d00a/tred/tred4451.htm

    def to_xml(self):
        xml_string = "<ram:IncludedNote>"
        xml_string += f"<ram:Content>{self.content}</ram:Content>"

        if self.subject_code is not None:
            xml_string += f"<ram:SubjectCode>{self.subject_code}</ram:SubjectCode>"

        xml_string += "</ram:IncludedNote>"
        return xml_string
