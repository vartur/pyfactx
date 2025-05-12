from typing_extensions import override

from .FacturXMinimum import FacturXMinimum
from .InvoiceProfile import InvoiceProfile


class FacturXBasicWL(FacturXMinimum):

    @override
    def to_xml(self):
        return f'''<?xml version='1.0' encoding='UTF-8'?>
                            <rsm:CrossIndustryInvoice xmlns:qdt="urn:un:unece:uncefact:data:standard:QualifiedDataType:100"
                            xmlns:ram="urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100"
                            xmlns:rsm="urn:un:unece:uncefact:data:standard:CrossIndustryInvoice:100"
                            xmlns:udt="urn:un:unece:uncefact:data:standard:UnqualifiedDataType:100"
                            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
                                {self.exchanged_document_context.to_xml()}
                                {self.exchanged_document.to_xml(profile=InvoiceProfile.BASICWL)}
                                {self.supply_chain_transaction.to_xml()}
                            </rsm:CrossIndustryInvoice>
                            '''