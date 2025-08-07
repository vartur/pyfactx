from typing import Optional, ClassVar
from lxml import etree as ET
from pydantic import Field, ConfigDict, model_validator
from typing_extensions import override

from .ExchangedDocument import ExchangedDocument
from .ExchangedDocumentContext import ExchangedDocumentContext
from .InvoiceProfile import InvoiceProfile
from .SupplyChainTradeTransaction import SupplyChainTradeTransaction
from .XMLBaseModel import XMLBaseModel
from .namespaces import NAMESPACES, RSM


class FacturXData(XMLBaseModel):
    """Represents the root structure of a Factur-X XML invoice document.

    This class encapsulates the three main components of a Factur-X invoice:
    - Document context (metadata and profile information)
    - Exchanged document (core invoice data)
    - Supply chain transaction (detailed business transaction data)

    Attributes:
        exchanged_document_context (ExchangedDocumentContext): The document context information
        exchanged_document (ExchangedDocument): The core invoice document data
        supply_chain_transaction (SupplyChainTradeTransaction): The detailed transaction data
    """

    model_config = ConfigDict(
        validate_assignment=True,
        frozen=True
    )

    # XML element names as constants
    CONTEXT_ELEMENT: ClassVar[str] = "ExchangedDocumentContext"
    DOCUMENT_ELEMENT: ClassVar[str] = "ExchangedDocument"
    TRANSACTION_ELEMENT: ClassVar[str] = "SupplyChainTradeTransaction"
    ROOT_ELEMENT: ClassVar[str] = "CrossIndustryInvoice"

    exchanged_document_context: ExchangedDocumentContext = Field(
        ...,
        description="Document context containing profile and business process information"
    )

    exchanged_document: ExchangedDocument = Field(
        ...,
        description="Core invoice document data"
    )

    supply_chain_transaction: SupplyChainTradeTransaction = Field(
        ...,
        description="Detailed business transaction data"
    )

    @model_validator(mode='after')
    def validate_profile_consistency(self) -> 'FacturXData':
        """Validates that the profile is consistent across all components.

        Returns:
            FacturXData: The validated instance.

        Raises:
            ValueError: If profile consistency validation fails.
        """
        context_profile = self.exchanged_document_context.guideline_specified_document_context_parameter
        if (hasattr(self.exchanged_document, 'profile') and
                self.exchanged_document.profile != context_profile):
            raise ValueError(
                f"Profile mismatch between context ({context_profile}) and "
                f"document ({self.exchanged_document.profile})"
            )
        return self

    @override
    def to_xml(self, element_name: str, profile: InvoiceProfile) -> ET.Element:
        """Converts the Factur-X data to XML format.

        Args:
            element_name (str): Name of the root XML element.
            profile (InvoiceProfile): The Factur-X profile being used.

        Returns:
            ET.Element: The root XML element containing the complete invoice data.

        Raises:
            ValueError: If XML creation fails.
        """
        try:
            # Create root element with namespaces
            root = ET.Element(
                f"{{{NAMESPACES[RSM]}}}{element_name}",
                nsmap=NAMESPACES
            )

            # Append child elements in the required order
            root.append(self.exchanged_document_context.to_xml(
                self.CONTEXT_ELEMENT,
                profile
            ))

            root.append(self.exchanged_document.to_xml(
                self.DOCUMENT_ELEMENT,
                profile
            ))

            root.append(self.supply_chain_transaction.to_xml(
                self.TRANSACTION_ELEMENT,
                profile
            ))

            return root

        except (ET.XMLSyntaxError, ValueError) as e:
            raise ValueError(f"Failed to create XML document: {str(e)}")

    def get_invoice_number(self) -> str:
        """Returns the invoice number from the exchanged document.

        Returns:
            str: The invoice number.
        """
        return self.exchanged_document.invoice_number

    def get_invoice_date(self) -> str:
        """Returns the invoice date from the exchanged document.

        Returns:
            str: The invoice date.
        """
        return self.exchanged_document.issue_date

    @classmethod
    def create(
            cls,
            profile: InvoiceProfile,
            document: ExchangedDocument,
            transaction: SupplyChainTradeTransaction,
            business_process_id: Optional[str] = None
    ) -> 'FacturXData':
        """Creates a new FacturXData instance with the given components.

        Args:
            profile (InvoiceProfile): The Factur-X profile to use.
            document (ExchangedDocument): The exchanged document data.
            transaction (SupplyChainTradeTransaction): The transaction data.
            business_process_id (Optional[str]): Optional business process identifier.

        Returns:
            FacturXData: A new FacturXData instance.
        """
        context = (
            ExchangedDocumentContext.create_with_business_process(profile, business_process_id)
            if business_process_id
            else ExchangedDocumentContext.create_default(profile)
        )

        return cls(
            exchanged_document_context=context,
            exchanged_document=document,
            supply_chain_transaction=transaction
        )

    def __str__(self) -> str:
        """Returns a human-readable string representation."""
        return (
            f"FacturXData(profile={self.exchanged_document_context.guideline_specified_document_context_parameter}, "
            f"invoice_number={self.get_invoice_number()}, "
            f"date={self.get_invoice_date()})"
        )
