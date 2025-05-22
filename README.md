# PyFactX

**PyFactX** is a Python library that leverages [Pydantic](https://docs.pydantic.dev/) models to generate fully
compliant [Factur-X](https://www.factur-x.org/) (EN 16931) e-invoices. This library generates a structured XML file,
suitable for machine processing, which can then be embedded in a hybrid PDF A/3 electronic invoice for full compliance
with the European e-invoicing standards.

---

## ✨ Features

- ✅ Full support for **EN 16931** compliant Factur-X invoices
- 📦 Clean and robust **Pydantic models** for structured invoice data
- 🧾 Generates **Factur-X-compliant XML** from Python dictionaries or Pydantic models
- 🇪🇺 Compatible with European e-invoicing standards
- 📄 Can be easily embedded into PDF invoices (e.g., via [facturelibre](https://github.com/vartur/facturelibre))

---

## 📦 Installation

```bash
pip install pyfactx
```

## ✅ Compliance

PyFactX aims for full compliance with the following:

* Factur-X **_MINIMUM_**, **_BASIC_WL_**, **_BASIC_** AND **_EN16931_** invoice profiles
* Schematron validation support

## 🚀 Quick Start

```python
import datetime
from lxml import etree as ET

from src.pyfactx.BinaryObject import BinaryObject
from src.pyfactx.DocumentLineDocument import DocumentLineDocument
from src.pyfactx.DocumentTypeCode import DocumentTypeCode
from src.pyfactx.ExchangedDocument import ExchangedDocument
from src.pyfactx.FacturXData import FacturXData
from src.pyfactx.ExchangedDocumentContext import ExchangedDocumentContext
from src.pyfactx.FacturXGenerator import FacturXGenerator
from src.pyfactx.HeaderTradeAgreement import HeaderTradeAgreement
from src.pyfactx.HeaderTradeDelivery import HeaderTradeDelivery
from src.pyfactx.HeaderTradeSettlement import HeaderTradeSettlement
from src.pyfactx.InvoiceProfile import InvoiceProfile
from src.pyfactx.InvoiceTypeCode import InvoiceTypeCode
from src.pyfactx.LineTradeAgreement import LineTradeAgreement
from src.pyfactx.LineTradeDelivery import LineTradeDelivery
from src.pyfactx.LineTradeSettlement import LineTradeSettlement
from src.pyfactx.Note import Note
from src.pyfactx.PaymentMeansCode import PaymentMeansCode
from src.pyfactx.ProcuringProject import ProcuringProject
from src.pyfactx.ReferencedDocument import ReferencedDocument
from src.pyfactx.SupplyChainEvent import SupplyChainEvent
from src.pyfactx.SupplyChainTradeLineItem import SupplyChainTradeLineItem
from src.pyfactx.SupplyChainTradeTransaction import SupplyChainTradeTransaction
from src.pyfactx.TaxCategoryCode import TaxCategoryCode
from src.pyfactx.TaxTypeCode import TaxTypeCode
from src.pyfactx.TradeContact import TradeContact
from src.pyfactx.TradeParty import TradeParty
from src.pyfactx.TradePaymentTerms import TradePaymentTerms
from src.pyfactx.TradePrice import TradePrice
from src.pyfactx.TradeProduct import TradeProduct
from src.pyfactx.TradeSettlementHeaderMonetarySummation import TradeSettlementHeaderMonetarySummation
from src.pyfactx.TradeAddress import TradeAddress
from src.pyfactx.LegalOrganization import LegalOrganization
from src.pyfactx.TradeSettlementLineMonetarySummation import TradeSettlementLineMonetarySummation
from src.pyfactx.TradeSettlementPaymentMeans import TradeSettlementPaymentMeans
from src.pyfactx.TradeTax import TradeTax
from src.pyfactx.UnitCode import UnitCode
from src.pyfactx.UniversalCommunication import UniversalCommunication

doc_context = ExchangedDocumentContext(business_process_specified_document_context_parameter="MyBusiness",
                                       guideline_specified_document_context_parameter=InvoiceProfile.EN16931)
document = ExchangedDocument(id="INV-ABCDEF",
                             type_code=InvoiceTypeCode.COMMERCIAL_INVOICE,
                             issue_date_time=datetime.datetime(year=2025, month=4, day=25),
                             included_notes=[Note(content="Sausages", subject_code="AAA"),
                                             Note(content="RCS Paris 123 456 789", subject_code="ABL")])

trade_address = TradeAddress(postcode="75001", line_one="1 rue des Baguettes", line_two="4è étage",
                             line_three="Appartement 48", city="Paris", country="FR",
                             country_subdivision="Île de France")
legal_org = LegalOrganization(id="123456789", trading_business_name="Saucisses & Co")
trade_contact = TradeContact(person_name="John Contact", department_name="Macro Data Refinement",
                             telephone_universal_communication=UniversalCommunication(complete_number="01 23 45 67 89"),
                             email_uri_universal_communication=UniversalCommunication(uri_id="john@macrodata.com"))

seller = TradeParty(ids=["abc", "def", "ghi"], global_ids=[("0088", "587451236587"), ("0009", "12345678200077")],
                    name="John Seller",
                    description="Self-employed sausage craftsman",
                    specified_legal_organisation=legal_org, trade_address=trade_address,
                    specified_tax_registration="FR123456789",
                    defined_trade_contact=trade_contact,
                    uri_universal_communication=UniversalCommunication(uri_id="john@saucissesandco.fr"))

buyer = TradeParty(ids=["abc"], global_ids=[("0088", "587451236588")],
                   name="John Buyer",
                   specified_legal_organisation=legal_org, trade_address=trade_address,
                   specified_tax_registration="FR123456788",
                   defined_trade_contact=trade_contact,
                   uri_universal_communication=UniversalCommunication(uri_id="john@gmail.com"))

ship_to = TradeParty(ids=["abc"], global_ids=[("0088", "587451236588")],
                     name="John Shipping",
                     trade_address=trade_address)

tax_rep = TradeParty(name="John Tax",
                     trade_address=trade_address,
                     specified_tax_registration="FR123456788")
payee = TradeParty(name="John Payee")

monetary_summation = TradeSettlementHeaderMonetarySummation(tax_basis_total_amount=100.0, tax_total_amount=4.90,
                                                            grand_total_amount=104.90, due_payable_amount=104.90,
                                                            line_total_amount=100.0, charge_total_amount=0.0,
                                                            allowance_total_amount=0.0, rounding_amount=0.0,
                                                            tax_currency_code="EUR", total_prepaid_amount=0.0)
applicable_trade_tax = TradeTax(calculated_amount=4.90, type_code=TaxTypeCode.VALUE_ADDED_TAX, basis_amount=100.0,
                                category_code=TaxCategoryCode.STANDARD_RATE, rate_applicable_percent=4.90)
payment_means = [TradeSettlementPaymentMeans(payment_means_code=PaymentMeansCode.CASH),
                 TradeSettlementPaymentMeans(payment_means_code=PaymentMeansCode.SEPA_CREDIT_TRANSFER)]

ref_doc = ReferencedDocument(issuer_assigned_id="123", uri_id="urn:abc:def", line_id="1",
                             type_code=DocumentTypeCode.RELATED_DOCUMENT, name="Example",
                             attachment_binary_object=BinaryObject(content_b64="1561561561561", mime_code="image/jpeg",
                                                                   filename="cat.jpeg"), reference_type_code="123",
                             issue_date=datetime.datetime(year=2025, month=3, day=1))

ref_doc2 = ReferencedDocument(issuer_assigned_id="123")
ref_doc3 = ReferencedDocument(issuer_assigned_id="123", uri_id="urn:abc:def",
                              type_code=DocumentTypeCode.RELATED_DOCUMENT, name="Example",
                              attachment_binary_object=BinaryObject(content_b64="1561561561561", mime_code="image/jpeg",
                                                                    filename="cat.jpeg"))
trade_agreement = HeaderTradeAgreement(seller_trade_party=seller, buyer_trade_party=buyer,
                                       seller_tax_representative_trade_party=tax_rep,
                                       seller_order_referenced_document=ref_doc2,
                                       buyer_order_referenced_document=ref_doc2,
                                       contract_referenced_document=ref_doc2,
                                       additional_referenced_documents=[ref_doc3, ref_doc3],
                                       specified_procuring_project=ProcuringProject(id="abc", name="My Project"))
trade_payment_terms = TradePaymentTerms(due_date=datetime.datetime(year=2025, month=4, day=30))
trade_delivery = HeaderTradeDelivery(ship_to_trade_party=ship_to, actual_delivery_supply_chain_event=SupplyChainEvent(
    occurrence_date=datetime.datetime(year=2025, month=3, day=1)), despatch_advice_referenced_document=ref_doc2,
                                     receiving_advice_referenced_document=ref_doc2)
trade_settlement = HeaderTradeSettlement(creditor_reference_id="abc", payment_reference="eznfoezf",
                                         invoice_currency_code="EUR",
                                         payee_trade_party=payee,
                                         applicable_trade_tax=[applicable_trade_tax],
                                         specified_trade_settlement_payment_means=payment_means,
                                         specified_trade_payment_terms=trade_payment_terms,
                                         specified_trade_settlement_header_monetary_summation=monetary_summation)

line_item_1 = SupplyChainTradeLineItem(associated_document_line_document=DocumentLineDocument(line_id=1),
                                       specified_trade_product=TradeProduct(name="Vegetarian sausage"),
                                       specified_line_trade_agreement=LineTradeAgreement(
                                           net_price_product_trade_price=TradePrice(charge_amount=10.0,
                                                                                    unit=UnitCode.ONE)),
                                       specified_line_trade_delivery=LineTradeDelivery(billed_quantity=10,
                                                                                       unit=UnitCode.ONE),
                                       specified_line_trade_settlement=LineTradeSettlement(
                                           applicable_trade_tax=TradeTax(type_code=TaxTypeCode.VALUE_ADDED_TAX,
                                                                         category_code=TaxCategoryCode.STANDARD_RATE,
                                                                         rate_applicable_percent=4.9),
                                           specified_trade_settlement_line_monetary_summation=TradeSettlementLineMonetarySummation(
                                               line_total_amount=100)))

transaction = SupplyChainTradeTransaction(included_supply_chain_trade_line_items=[line_item_1],
                                          applicable_header_trade_agreement=trade_agreement,
                                          applicable_header_trade_delivery=trade_delivery,
                                          applicable_header_trade_settlement=trade_settlement)

facturx_data = FacturXData(exchanged_document_context=doc_context, exchanged_document=document,
                           supply_chain_transaction=transaction)

if __name__ == '__main__':
    xml = FacturXGenerator.generate(facturx_data, InvoiceProfile.BASIC)

    xml_string = ET.tostring(xml, pretty_print=True, encoding='utf-8').decode('utf-8')
    print(xml_string)

```

## 🤝 Contributing

Contributions are welcome! Feel free to submit issues, bug reports, or pull requests.

## 📄 License

This project is licensed under the MIT License. See [LICENSE](./LICENSE) for details.

## 🧾 About Factur-X

Factur-X is the Franco-German standard for hybrid electronic invoices, combining PDF and XML to meet the requirements of
both businesses and tax authorities across the EU.

Learn more at: https://www.factur-x.org/