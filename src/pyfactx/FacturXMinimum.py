from typing import ClassVar

from pydantic import BaseModel, Field
from xml.etree.ElementTree import Element, register_namespace

from .InvoiceProfile import InvoiceProfile
from .ExchangedDocumentContext import ExchangedDocumentContext
from .ExchangedDocument import ExchangedDocument
from .SupplyChainTradeTransaction import SupplyChainTradeTransaction
from .namespaces import NAMESPACES, QUALIFIED, RSM


class FacturXMinimum(BaseModel):
    exchanged_document_context: ExchangedDocumentContext = Field(...)
    exchanged_document: ExchangedDocument = Field(...)
    supply_chain_transaction: SupplyChainTradeTransaction = Field(...)

    profile: ClassVar[InvoiceProfile] = InvoiceProfile.MINIMUM

    def to_xml(self) -> Element:
        for prefix, uri in NAMESPACES.items():
            register_namespace(prefix, uri)

        # CrossIndustryInvoice
        root = Element(f"{RSM}CrossIndustryInvoice", {
            f"xmlns:{k}": v for k, v in NAMESPACES.items()
        })

        # ExchangedDocumentContext
        root.append(self.exchanged_document_context.to_xml("ExchangedDocumentContext", self.profile))

        # ExchangedDocument
        root.append(self.exchanged_document.to_xml("ExchangedDocument", self.profile))

        # SupplyChainTradeTransaction
        root.append(self.supply_chain_transaction.to_xml("SupplyChainTradeTransaction", self.profile))

        return root
