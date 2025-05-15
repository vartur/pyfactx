from abc import ABC, abstractmethod
from lxml import etree as ET

from pydantic import BaseModel

from .InvoiceProfile import InvoiceProfile


class XMLBaseModel(BaseModel, ABC):

    @abstractmethod
    def to_xml(self, element_name: str, profile: InvoiceProfile) -> ET.Element:
        pass
