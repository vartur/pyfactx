import datetime
from xml.etree.ElementTree import tostring, Element
from xml.dom import minidom

from src.pyfactx.ExchangedDocument import ExchangedDocument
from src.pyfactx.FacturXBasicWL import FacturXBasicWL
from src.pyfactx.FacturXMinimum import FacturXMinimum
from src.pyfactx.ExchangedDocumentContext import ExchangedDocumentContext
from src.pyfactx.HeaderTradeAgreement import HeaderTradeAgreement
from src.pyfactx.HeaderTradeDelivery import HeaderTradeDelivery
from src.pyfactx.HeaderTradeSettlement import HeaderTradeSettlement
from src.pyfactx.InvoiceProfile import InvoiceProfile
from src.pyfactx.PaymentMeansCode import PaymentMeansCode
from src.pyfactx.SupplyChainTradeTransaction import SupplyChainTradeTransaction
from src.pyfactx.TaxCategoryCode import TaxCategoryCode
from src.pyfactx.TaxTypeCode import TaxTypeCode
from src.pyfactx.TradeParty import TradeParty
from src.pyfactx.TradePaymentTerms import TradePaymentTerms
from src.pyfactx.TradeSettlementHeaderMonetarySummation import TradeSettlementHeaderMonetarySummation
from src.pyfactx.TradeAddress import TradeAddress
from src.pyfactx.LegalOrganization import LegalOrganization
from src.pyfactx.TradeSettlementPaymentMeans import TradeSettlementPaymentMeans
from src.pyfactx.TradeTax import TradeTax


def generate_facturx_minimum() -> Element:
    doc_context = ExchangedDocumentContext(guideline_specified_document_context_parameter=InvoiceProfile.MINIMUM)
    document = ExchangedDocument(id="INV-ABCDEF", issue_date_time=datetime.datetime(year=2025, month=4, day=25))

    trade_address = TradeAddress(country="FR")
    legal_org = LegalOrganization(id="123456789")
    seller = TradeParty(name="John Seller", specified_legal_organisation=legal_org, trade_address=trade_address)
    buyer = TradeParty(name="John Buyer")
    monetary_summation = TradeSettlementHeaderMonetarySummation(tax_basis_total_amount=100, tax_total_amount=4.90,
                                                                grand_total_amount=104.90, due_payable_amount=104.90)

    trade_agreement = HeaderTradeAgreement(seller_trade_party=seller, buyer_trade_party=buyer)
    trade_delivery = HeaderTradeDelivery()
    trade_settlement = HeaderTradeSettlement(invoice_currency_code="EUR",
                                             specified_trade_settlement_header_monetary_summation=monetary_summation)

    transaction = SupplyChainTradeTransaction(applicable_header_trade_agreement=trade_agreement,
                                              applicable_header_trade_delivery=trade_delivery,
                                              applicable_header_trade_settlement=trade_settlement)

    facturx_minimum = FacturXMinimum(exchanged_document_context=doc_context, exchanged_document=document,
                                     supply_chain_transaction=transaction)

    return facturx_minimum.to_xml()


def generate_facturx_basic_wl() -> Element:
    doc_context = ExchangedDocumentContext(guideline_specified_document_context_parameter=InvoiceProfile.BASICWL)
    document = ExchangedDocument(id="INV-ABCDEF", issue_date_time=datetime.datetime(year=2025, month=4, day=25))

    trade_address = TradeAddress(country="FR")
    legal_org = LegalOrganization(id="123456789")
    seller = TradeParty(name="John Seller", specified_legal_organisation=legal_org, trade_address=trade_address)
    buyer = TradeParty(name="John Buyer", trade_address=trade_address)
    monetary_summation = TradeSettlementHeaderMonetarySummation(tax_basis_total_amount=100.0, tax_total_amount=4.90,
                                                                grand_total_amount=104.90, due_payable_amount=104.90,
                                                                line_total_amount=100.0)
    applicable_trade_tax = TradeTax(calculated_amount=4.90, type_code=TaxTypeCode.VALUE_ADDED_TAX, basis_amount=100.0,
                                    category_code=TaxCategoryCode.STANDARD_RATE, rate_applicable_percent=4.90)
    payment_means = TradeSettlementPaymentMeans(payment_means_code=PaymentMeansCode.CASH)
    trade_agreement = HeaderTradeAgreement(seller_trade_party=seller, buyer_trade_party=buyer)
    trade_payment_terms = TradePaymentTerms(due_date=datetime.datetime(year=2025, month=4, day=30))
    trade_delivery = HeaderTradeDelivery()
    trade_settlement = HeaderTradeSettlement(invoice_currency_code="EUR",
                                             applicable_trade_tax=[applicable_trade_tax],
                                             specified_trade_settlement_payment_means=[payment_means],
                                             specified_trade_payment_terms=trade_payment_terms,
                                             specified_trade_settlement_header_monetary_summation=monetary_summation)

    transaction = SupplyChainTradeTransaction(applicable_header_trade_agreement=trade_agreement,
                                              applicable_header_trade_delivery=trade_delivery,
                                              applicable_header_trade_settlement=trade_settlement)

    facturx_basic_wl = FacturXBasicWL(exchanged_document_context=doc_context, exchanged_document=document,
                                      supply_chain_transaction=transaction)

    return facturx_basic_wl.to_xml()


if __name__ == '__main__':
    xml = generate_facturx_minimum()

    xml_string = tostring(xml, encoding='utf-8')
    pretty_xml_string = minidom.parseString(xml_string).toprettyxml(indent="  ")
    print(pretty_xml_string)
