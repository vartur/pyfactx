from typing import Optional, ClassVar, List
from lxml import etree as ET
from pydantic import Field, ConfigDict, model_validator
from typing_extensions import override

from .InvoiceProfile import InvoiceProfile
from .ReferencedDocument import ReferencedDocument
from .SpecifiedPeriod import SpecifiedPeriod
from .TradeAccountingAccount import TradeAccountingAccount
from .TradeAllowanceCharge import TradeAllowanceCharge
from .TradeParty import TradeParty
from .TradePaymentTerms import TradePaymentTerms
from .TradeSettlementHeaderMonetarySummation import TradeSettlementHeaderMonetarySummation
from .TradeSettlementPaymentMeans import TradeSettlementPaymentMeans
from .TradeTax import TradeTax
from .XMLBaseModel import XMLBaseModel
from .namespaces import NAMESPACES, RAM


class HeaderTradeSettlement(XMLBaseModel):
    """Represents the trade settlement header section of a Factur-X document.

    This class contains information about payment terms, currencies, taxes,
    and monetary summations for the invoice.
    """

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        validate_assignment=True
    )

    # XML element names mapping
    XML_ELEMENTS: ClassVar[dict[str, str]] = {
        'creditor_ref': 'CreditorReferenceID',
        'payment_ref': 'PaymentReference',
        'tax_currency': 'TaxCurrencyCode',
        'invoice_currency': 'InvoiceCurrencyCode',
        'payee': 'PayeeTradeParty',
        'payment_means': 'SpecifiedTradeSettlementPaymentMeans',
        'tax': 'ApplicableTradeTax',
        'period': 'BillingSpecifiedPeriod',
        'allowance': 'SpecifiedTradeAllowanceCharge',
        'payment_terms': 'SpecifiedTradePaymentTerms',
        'monetary_summation': 'SpecifiedTradeSettlementHeaderMonetarySummation',
        'invoice_ref': 'InvoiceReferencedDocument',
        'accounting': 'ReceivableSpecifiedTradeAccountingAccount'
    }

    # Required fields
    invoice_currency_code: str = Field(
        ...,
        description="Currency code for the invoice (e.g., 'EUR', 'USD')"
    )
    
    specified_trade_settlement_header_monetary_summation: TradeSettlementHeaderMonetarySummation = Field(
        ...,
        description="Monetary totals for the invoice"
    )

    # Optional fields (BASICWL and above)
    creditor_reference_id: Optional[str] = Field(
        default=None,
        description="Creditor's reference identifier (BASICWL+)"
    )
    
    payment_reference: Optional[str] = Field(
        default=None,
        description="Payment reference number (BASICWL+)"
    )
    
    tax_currency_code: Optional[str] = Field(
        default=None,
        description="Currency code for tax amounts (BASICWL+)"
    )
    
    payee_trade_party: Optional[TradeParty] = Field(
        default=None,
        description="Party to receive the payment (BASICWL+)"
    )
    
    specified_trade_settlement_payment_means: Optional[List[TradeSettlementPaymentMeans]] = Field(
        default=None,
        description="Payment means details (BASICWL+)"
    )
    
    applicable_trade_tax: Optional[List[TradeTax]] = Field(
        default=None,
        description="Tax details (BASICWL+)"
    )
    
    billing_specified_period: Optional[SpecifiedPeriod] = Field(
        default=None,
        description="Billing period details (BASICWL+)"
    )
    
    specified_trade_allowance_charge: Optional[List[TradeAllowanceCharge]] = Field(
        default=None,
        description="Allowances and charges (BASICWL+)"
    )
    
    specified_trade_payment_terms: Optional[TradePaymentTerms] = Field(
        default=None,
        description="Payment terms (BASICWL+)"
    )
    
    invoice_referenced_documents: Optional[List[ReferencedDocument]] = Field(
        default=None,
        description="Referenced invoice documents (BASICWL+)"
    )
    
    receivable_specified_trade_accounting_account: Optional[TradeAccountingAccount] = Field(
        default=None,
        description="Accounting account details (BASICWL+)"
    )

    @model_validator(mode='after')
    def validate_profile_specific_fields(self) -> 'HeaderTradeSettlement':
        """Validates that fields are appropriate for their profile level."""
        profile = getattr(self, '_current_profile', None)
        if not profile:
            return self

        if profile < InvoiceProfile.BASICWL:
            basicwl_fields = [
                ('creditor_reference_id', self.creditor_reference_id),
                ('payment_reference', self.payment_reference),
                ('tax_currency_code', self.tax_currency_code),
                ('payee_trade_party', self.payee_trade_party),
                ('specified_trade_settlement_payment_means', self.specified_trade_settlement_payment_means),
                ('applicable_trade_tax', self.applicable_trade_tax),
                ('billing_specified_period', self.billing_specified_period),
                ('specified_trade_allowance_charge', self.specified_trade_allowance_charge),
                ('specified_trade_payment_terms', self.specified_trade_payment_terms),
                ('invoice_referenced_documents', self.invoice_referenced_documents),
                ('receivable_specified_trade_accounting_account', self.receivable_specified_trade_accounting_account)
            ]

            for field_name, field_value in basicwl_fields:
                if field_value is not None:
                    raise ValueError(
                        f"{field_name} is only allowed in BASICWL profile and above"
                    )

        return self

    def _add_text_element(
        self,
        root: ET.Element,
        value: Optional[str],
        element_name: str,
        profile: InvoiceProfile,
        min_profile: InvoiceProfile
    ) -> None:
        """Adds a text element to the XML if conditions are met."""
        if value is not None and profile >= min_profile:
            ET.SubElement(root, f"{{{NAMESPACES[RAM]}}}{element_name}").text = value

    def _add_object_element(
        self,
        root: ET.Element,
        obj: Optional[XMLBaseModel],
        element_name: str,
        profile: InvoiceProfile,
        min_profile: InvoiceProfile
    ) -> None:
        """Adds an object element to the XML if conditions are met."""
        if obj is not None and profile >= min_profile:
            root.append(obj.to_xml(element_name, profile))

    def _add_list_elements(
        self,
        root: ET.Element,
        items: Optional[List[XMLBaseModel]],
        element_name: str,
        profile: InvoiceProfile,
        min_profile: InvoiceProfile
    ) -> None:
        """Adds list elements to the XML if conditions are met."""
        if items is not None and profile >= min_profile:
            for item in items:
                root.append(item.to_xml(element_name, profile))

    @override
    def to_xml(self, element_name: str, profile: InvoiceProfile) -> ET.Element:
        """Converts the trade settlement to XML format."""
        root = ET.Element(f"{{{NAMESPACES[RAM]}}}{element_name}")
        
        # Set profile for validation
        self._current_profile = profile

        # Add BASICWL+ text elements
        self._add_text_element(root, self.creditor_reference_id, self.XML_ELEMENTS['creditor_ref'], 
                             profile, InvoiceProfile.BASICWL)
        self._add_text_element(root, self.payment_reference, self.XML_ELEMENTS['payment_ref'],
                             profile, InvoiceProfile.BASICWL)
        self._add_text_element(root, self.tax_currency_code, self.XML_ELEMENTS['tax_currency'],
                             profile, InvoiceProfile.BASICWL)

        # Add required elements
        ET.SubElement(root, f"{{{NAMESPACES[RAM]}}}{self.XML_ELEMENTS['invoice_currency']}").text = \
            self.invoice_currency_code

        # Add BASICWL+ object elements
        self._add_object_element(root, self.payee_trade_party, self.XML_ELEMENTS['payee'],
                               profile, InvoiceProfile.BASICWL)
        self._add_object_element(root, self.billing_specified_period, self.XML_ELEMENTS['period'],
                               profile, InvoiceProfile.BASICWL)
        self._add_object_element(root, self.specified_trade_payment_terms, self.XML_ELEMENTS['payment_terms'],
                               profile, InvoiceProfile.BASICWL)

        # Add BASICWL+ list elements
        self._add_list_elements(root, self.specified_trade_settlement_payment_means, 
                              self.XML_ELEMENTS['payment_means'], profile, InvoiceProfile.BASICWL)
        self._add_list_elements(root, self.applicable_trade_tax, self.XML_ELEMENTS['tax'],
                              profile, InvoiceProfile.BASICWL)
        self._add_list_elements(root, self.specified_trade_allowance_charge, self.XML_ELEMENTS['allowance'],
                              profile, InvoiceProfile.BASICWL)
        self._add_list_elements(root, self.invoice_referenced_documents, self.XML_ELEMENTS['invoice_ref'],
                              profile, InvoiceProfile.BASICWL)

        # Add required monetary summation
        root.append(self.specified_trade_settlement_header_monetary_summation.to_xml(
            self.XML_ELEMENTS['monetary_summation'], profile))

        # Add optional accounting account
        self._add_object_element(root, self.receivable_specified_trade_accounting_account,
                               self.XML_ELEMENTS['accounting'], profile, InvoiceProfile.BASICWL)

        return root