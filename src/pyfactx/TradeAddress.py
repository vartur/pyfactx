from typing import Optional

from pydantic import BaseModel, Field

from .InvoiceProfile import InvoiceProfile


class TradeAddress(BaseModel):
    postcode: Optional[str] = Field(default=None)
    line_one: Optional[str] = Field(default=None)
    line_two: Optional[str] = Field(default=None)
    line_three: Optional[str] = Field(default=None)
    city: Optional[str] = Field(default=None)
    country: str = Field(...)
    country_subdivision: Optional[str] = Field(default=None)

    def to_xml(self, profile: InvoiceProfile = InvoiceProfile.MINIMUM):
        xml_string = "<ram:PostalTradeAddress>"

        if profile != InvoiceProfile.MINIMUM:
            if self.postcode is not None:
                xml_string += f"<ram:PostcodeCode>{self.postcode}</ram:PostcodeCode>"

            if self.line_one is not None:
                xml_string += f"<ram:LineOne>{self.line_one}</ram:LineOne>"

            if self.line_two is not None:
                xml_string += f"<ram:LineTwo>{self.line_two}</ram:LineTwo>"

            if self.line_three is not None:
                xml_string += f"<ram:LineThree>{self.line_three}</ram:LineThree>"

            if self.city is not None:
                xml_string += f"<ram:CityName>{self.city}</ram:CityName>"

        xml_string += f"<ram:CountryID>{self.country}</ram:CountryID>"

        if profile != InvoiceProfile.MINIMUM:
            if self.country_subdivision is not None:
                xml_string += f"<ram:CountrySubDivisionName>{self.country_subdivision}</ram:CountrySubDivisionName>"

        xml_string += "</ram:PostalTradeAddress>"

        return xml_string
