from lxml import etree as ET

from pydantic import Field
from typing_extensions import override

from .ExchangedDocument import ExchangedDocument
from .ExchangedDocumentContext import ExchangedDocumentContext
from .InvoiceProfile import InvoiceProfile
from .SupplyChainTradeTransaction import SupplyChainTradeTransaction
from .XMLBaseModel import XMLBaseModel
from .namespaces import NAMESPACES, RSM


class FacturXData(XMLBaseModel):
    exchanged_document_context: ExchangedDocumentContext = Field(...)
    exchanged_document: ExchangedDocument = Field(...)
    supply_chain_transaction: SupplyChainTradeTransaction = Field(...)

    @override
    def to_xml(self, element_name: str, profile: InvoiceProfile) -> ET.Element:
        # CrossIndustryInvoice
        root = ET.Element(f"{{{NAMESPACES[RSM]}}}{element_name}", nsmap=NAMESPACES)

        # ExchangedDocumentContext
        root.append(self.exchanged_document_context.to_xml("ExchangedDocumentContext", profile))

        # ExchangedDocument
        root.append(self.exchanged_document.to_xml("ExchangedDocument", profile))

        # SupplyChainTradeTransaction
        root.append(self.supply_chain_transaction.to_xml("SupplyChainTradeTransaction", profile))

        return root
