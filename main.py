from src.pyfactx.ExchangedDocument import ExchangedDocument
from src.pyfactx.FacturXMinimum import FacturXMinimum
from src.pyfactx.ExchangedDocumentContext import ExchangedDocumentContext
from src.pyfactx.HeaderTradeAgreement import HeaderTradeAgreement
from src.pyfactx.HeaderTradeDelivery import HeaderTradeDelivery
from src.pyfactx.HeaderTradeSettlement import HeaderTradeSettlement
from src.pyfactx.InvoiceProfile import InvoiceProfile
from src.pyfactx.SupplyChainTradeTransaction import SupplyChainTradeTransaction
from src.pyfactx.TradeParty import TradeParty
from src.pyfactx.TradeSettlementHeaderMonetarySummation import TradeSettlementHeaderMonetarySummation
from src.pyfactx.TradeAddress import TradeAddress
from src.pyfactx.LegalOrganization import LegalOrganization


def generate_facturx_minimum():
    doc_context = ExchangedDocumentContext(guideline_specified_document_context_parameter=InvoiceProfile.MINIMUM)
    document = ExchangedDocument(id="INV-ABCDEF", issue_date_time="20250425")

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


if __name__ == '__main__':
    xml_string = generate_facturx_minimum()

    print(xml_string)
