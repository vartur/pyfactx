from lxml import etree as ET
from pydantic import Field
from typing_extensions import override

from .InvoiceProfile import InvoiceProfile
from .XMLBaseModel import XMLBaseModel
from .namespaces import NAMESPACES, RAM


class TradeAccountingAccount(XMLBaseModel):
    """Represents a trade accounting account according to UN/CEFACT standards.
    
    This class models an accounting account used in trade documents, particularly
    in electronic invoices. It contains the account identifier and handles
    XML serialization according to the Cross Industry Invoice (CII) standard.

    Attributes:
        id (str): The identifier of the accounting account. This could be a general
            ledger account number, cost center code, or other accounting reference.

    Example:
        ```python
        account = TradeAccountingAccount(id="GL-1001")
        xml_element = account.to_xml("AccountingAccount", profile)
        ```
    """

    id: str = Field(
        ...,
        description="The identifier of the accounting account",
        examples=["GL-1001", "CC-2023"]
    )

    @override
    def to_xml(self, element_name: str, _profile: InvoiceProfile) -> ET.Element:
        """Converts the accounting account to its XML representation.

        Creates an XML element representing this accounting account according to
        the Cross Industry Invoice (CII) XML schema.

        Args:
            element_name: The name to use for the root XML element
            _profile: The invoice profile containing serialization settings
                (not used in this implementation but required by interface)

        Returns:
            ET.Element: An XML element representing this accounting account

        Example:
            ```python
            account = TradeAccountingAccount(id="GL-1001")
            xml = account.to_xml("AccountingAccount", profile)
            # Results in:
            # <ram:AccountingAccount>
            #     <ram:ID>GL-1001</ram:ID>
            # </ram:AccountingAccount>
            ```
        """
        # Create the root element with proper namespace
        root = ET.Element(f"{{{NAMESPACES[RAM]}}}{element_name}")

        # Add the ID element with proper namespace
        ET.SubElement(root, f"{{{NAMESPACES[RAM]}}}ID").text = self.id

        return root

    @classmethod
    def from_xml(cls, xml_element: ET.Element) -> "TradeAccountingAccount":
        """Creates a TradeAccountingAccount instance from an XML element.

        Args:
            xml_element: The XML element containing account data

        Returns:
            TradeAccountingAccount: A new instance populated from the XML

        Raises:
            ValueError: If required elements are missing or invalid

        Example:
            ```python
            xml_str = '''
                <ram:AccountingAccount>
                    <ram:ID>GL-1001</ram:ID>
                </ram:AccountingAccount>
            '''
            element = ET.fromstring(xml_str)
            account = TradeAccountingAccount.from_xml(element)
            ```
        """
        # Find the ID element using the proper namespace
        id_element = xml_element.find(f".//{{{NAMESPACES[RAM]}}}ID")
        if id_element is None or not id_element.text:
            raise ValueError("Missing or invalid ID element in XML")

        return cls(id=id_element.text)

    def __str__(self) -> str:
        """Returns a string representation of the accounting account.

        Returns:
            str: String representation of the account
        """
        return f"Account ID: {self.id}"