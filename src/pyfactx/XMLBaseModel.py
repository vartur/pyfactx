from abc import ABC, abstractmethod
from xml.etree.ElementTree import Element

from pydantic import BaseModel

from .InvoiceProfile import InvoiceProfile


class XMLBaseModel(BaseModel, ABC):

    @abstractmethod
    def to_xml(self, element_name: str, profile: InvoiceProfile) -> Element:
        pass
