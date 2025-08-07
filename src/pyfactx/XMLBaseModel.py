from abc import ABC, abstractmethod
from typing import Optional, Any, Dict
from lxml import etree as ET

from pydantic import BaseModel, ConfigDict

from .InvoiceProfile import InvoiceProfile


class XMLBaseModel(BaseModel, ABC):
    """Base class for XML-serializable Pydantic models.
    
    This abstract base class provides a foundation for models that can be
    serialized to XML format according to specific invoice profiles.
    
    All child classes must implement the to_xml method to define their
    XML serialization logic.
    """
    
    model_config = ConfigDict(
        validate_assignment=True,
        frozen=False,
        extra='forbid'
    )

    @abstractmethod
    def to_xml(self, element_name: str, profile: InvoiceProfile) -> ET.Element:
        """Convert the model instance to an XML element.
        
        Args:
            element_name: Name of the root XML element to create
            profile: Invoice profile containing serialization settings
            
        Returns:
            ET.Element: The created XML element containing the model data
            
        Raises:
            NotImplementedError: If the child class doesn't implement this method
        """
        raise NotImplementedError("Child classes must implement to_xml method")

    def to_xml_string(self, element_name: str, profile: InvoiceProfile,
                     pretty_print: bool = False, encoding: str = 'UTF-8') -> str:
        """Convert the model to an XML string representation.
        
        Args:
            element_name: Name of the root XML element
            profile: Invoice profile containing serialization settings
            pretty_print: Whether to format the XML with indentation
            encoding: Character encoding for the XML string
            
        Returns:
            str: XML string representation of the model
        """
        element = self.to_xml(element_name, profile)
        return ET.tostring(
            element,
            pretty_print=pretty_print,
            encoding=encoding
        ).decode(encoding)

    @classmethod
    def from_xml(cls, element: ET.Element) -> 'XMLBaseModel':
        """Create a model instance from an XML element.
        
        This method should be implemented by child classes to support
        XML deserialization.
        
        Args:
            element: XML element to parse
            
        Returns:
            XMLBaseModel: New instance of the model
            
        Raises:
            NotImplementedError: This base implementation always raises
        """
        raise NotImplementedError("XML deserialization not implemented")

    def _create_element(self, ns: str, name: str,
                       text: Optional[Any] = None,
                       attrib: Optional[Dict[str, str]] = None) -> ET.Element:
        """Helper method to create XML elements with namespace support.
        
        Args:
            ns: XML namespace URI
            name: Element name
            text: Optional element text content
            attrib: Optional element attributes
            
        Returns:
            ET.Element: Created XML element
        """
        element = ET.Element(f"{{{ns}}}{name}", attrib=attrib or {})
        if text is not None:
            element.text = str(text)
        return element

    def _add_subelement(self, parent: ET.Element, ns: str, name: str,
                       text: Optional[Any] = None,
                       attrib: Optional[Dict[str, str]] = None) -> ET.Element:
        """Helper method to add child elements with namespace support.
        
        Args:
            parent: Parent XML element
            ns: XML namespace URI
            name: Element name
            text: Optional element text content
            attrib: Optional element attributes
            
        Returns:
            ET.Element: Created child element
        """
        element = ET.SubElement(parent, f"{{{ns}}}{name}", attrib=attrib or {})
        if text is not None:
            element.text = str(text)
        return element

    def __str__(self) -> str:
        """Returns a human-readable string representation.
        
        Returns:
            str: String representation showing key model attributes
        """
        attrs = []
        for name, value in self.__dict__.items():
            if not name.startswith('_') and value is not None:
                attrs.append(f"{name}={value!r}")
        return f"{self.__class__.__name__}({', '.join(attrs)})"