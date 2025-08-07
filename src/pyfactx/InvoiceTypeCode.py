from enum import Enum


class InvoiceTypeCode(Enum):
    """UN/EDIFACT codes for document types used in Factur-X invoices.

    This enumeration represents standard document type codes as defined by
    UN/EDIFACT code list 1001. These codes are used to identify different
    types of business documents in electronic invoice processing.

    Values:
        REQUEST_FOR_PAYMENT (71):
            Document requesting payment for goods or services.

        DEBIT_NOTE_GOODS_SERVICES (80):
            Debit notification for goods or services transaction.

        METERED_SERVICES_INVOICE (82):
            Invoice issued for metered services (e.g., utilities).

        DEBIT_NOTE_FINANCIAL_ADJUSTMENTS (84):
            Debit notification for financial adjustments.

        TAX_NOTIFICATION (102):
            Document notifying of tax requirements.

        FINAL_PAYMENT_REQUEST_BASED_ON_COMPLETION_OF_WORK (218):
            Final payment request upon work completion.

        PAYMENT_REQUEST_FOR_COMPLETED_UNITS (219):
            Request for payment based on completed unit count.

        COMMERCIAL_INVOICER_WITH_PACKING_LIST (331):
            Commercial invoice including packing list details.

        COMMERCIAL_INVOICE (380):
            Standard commercial invoice for goods or services.

        COMMISSION_NOTE (382):
            Document stating earned commission.

        DEBIT_NOTE (383):
            General debit notification document.

        PREPAYMENT_INVOICE (386):
            Invoice requesting payment in advance.

        TAX_INVOICE (388):
            Invoice specifically for tax purposes.

        FACTORED_INVOICE (393):
            Invoice assigned to a third party for collection.

        CONSIGNMENT_INVOICE (395):
            Invoice for goods on consignment.

        FORWARDERS_INVOICER_DISCREPANCY_REPORT (553):
            Report of discrepancies from forwarding agent.

        INSURERS_INVOICE (575):
            Invoice issued by an insurance provider.

        FORWARDERS_INVOICE (623):
            Invoice from freight forwarding service.

        FREIGHT_INVOICE (780):
            Invoice for freight charges.

        CLAIM_NOTIFICATION (817):
            Document notifying of a claim.

        CONSULAR_INVOICE (870):
            Invoice certified by consular authority.

        PARTIAL_CONSTRUCTION_INVOICE (875):
            Interim invoice for construction work.

        PARTIAL_FINAL_CONSTRUCTION_INVOICE (876):
            Combined partial and final construction invoice.

        FINAL_CONSTRUCTION_INVOICE (877):
            Final invoice for completed construction work.

    References:
        - UN/EDIFACT code list 1001: https://unece.org/trade/uncefact/vocabulary/invoice-type-code
        - Factur-X Documentation: https://www.factur-x.org/

    Example:
        >>> doc_type = InvoiceTypeCode.COMMERCIAL_INVOICE
        >>> doc_type.value
        380
    """

    REQUEST_FOR_PAYMENT = 71
    DEBIT_NOTE_GOODS_SERVICES = 80
    METERED_SERVICES_INVOICE = 82
    DEBIT_NOTE_FINANCIAL_ADJUSTMENTS = 84
    TAX_NOTIFICATION = 102
    FINAL_PAYMENT_REQUEST_BASED_ON_COMPLETION_OF_WORK = 218
    PAYMENT_REQUEST_FOR_COMPLETED_UNITS = 219
    COMMERCIAL_INVOICER_WITH_PACKING_LIST = 331
    COMMERCIAL_INVOICE = 380
    COMMISSION_NOTE = 382
    DEBIT_NOTE = 383
    PREPAYMENT_INVOICE = 386
    TAX_INVOICE = 388
    FACTORED_INVOICE = 393
    CONSIGNMENT_INVOICE = 395
    FORWARDERS_INVOICER_DISCREPANCY_REPORT = 553
    INSURERS_INVOICE = 575
    FORWARDERS_INVOICE = 623
    FREIGHT_INVOICE = 780
    CLAIM_NOTIFICATION = 817
    CONSULAR_INVOICE = 870
    PARTIAL_CONSTRUCTION_INVOICE = 875
    PARTIAL_FINAL_CONSTRUCTION_INVOICE = 876
    FINAL_CONSTRUCTION_INVOICE = 877