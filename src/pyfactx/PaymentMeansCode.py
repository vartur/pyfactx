from enum import Enum
from typing import Dict, Optional


class PaymentMeansCode(Enum):
    """Payment means codes according to UN/CEFACT 4461.

    Each enum value represents a standardized payment method code.
    The numeric values correspond to the official UN/CEFACT codes.

    Common codes:
        CREDIT_TRANSFER (30): Standard credit transfer
        SEPA_CREDIT_TRANSFER (58): SEPA credit transfer
        SEPA_DIRECT_DEBIT (59): SEPA direct debit
        CREDIT_CARD (54): Payment by credit card
        DEBIT_CARD (55): Payment by debit card
        CASH (10): Cash payment
    """

    # Generic payment methods
    INSTRUMENT_NOT_DEFINED = 1
    CASH = 10
    PAYMENT_TO_BANK_ACCOUNT = 42

    # Credit transfers
    CREDIT_TRANSFER = 30
    SEPA_CREDIT_TRANSFER = 58
    URGENT_COMMERCIAL_PAYMENT = 52
    URGENT_TREASURY_PAYMENT = 53

    # Direct debits
    DIRECT_DEBIT = 49
    SEPA_DIRECT_DEBIT = 59

    # Card payments
    BANK_CARD = 48
    CREDIT_CARD = 54
    DEBIT_CARD = 55

    # Cheques and drafts
    CHEQUE = 20
    BANKERS_DRAFT = 21
    CERTIFIED_BANKERS_DRAFT = 22
    BANK_CHEQUE = 23
    CERTIFIED_CHEQUE = 25
    LOCAL_CHEQUE = 26
    NOT_TRANSFERABLE_BANKERS_DRAFT = 91
    NOT_TRANSFERABLE_LOCAL_CHEQUE = 92

    # Electronic methods
    ONLINE_PAYMENT_SERVICE = 68
    REFERENCED_HOME_BANKING_CREDIT_TRANSFER = 45
    HOME_BANKING_DEBIT_TRANSFER = 47

    # ACH transactions
    AUTOMATED_CLEARING_HOUSE_CREDIT = 2
    AUTOMATED_CLEARING_HOUSE_DEBIT = 3
    ACH_DEMAND_DEBIT_REVERSAL = 4
    ACH_DEMAND_CREDIT_REVERSAL = 5
    ACH_DEMAND_CREDIT = 6
    ACH_DEMAND_DEBIT = 7
    ACH_SAVINGS_CREDIT_REVERSAL = 11
    ACH_SAVINGS_DEBIT_REVERSAL = 12
    ACH_SAVINGS_CREDIT = 13
    ACH_SAVINGS_DEBIT = 14
    ACH_DEMAND_CCD_CREDIT = 17
    ACH_DEMAND_CCD_DEBIT = 18
    ACH_DEMAND_CTP_CREDIT = 19
    ACH_DEMAND_CTP_DEBIT = 27
    ACH_DEMAND_CTX_CREDIT = 28
    ACH_DEMAND_CTX_DEBIT = 29
    ACH_DEMAND_CCD_PLUS_CREDIT = 32
    ACH_DEMAND_CCD_PLUS_DEBIT = 33
    ACH_PPD = 34
    ACH_SAVINGS_CCD_CREDIT = 35
    ACH_SAVINGS_CCD_DEBIT = 36
    ACH_SAVINGS_CTP_CREDIT = 37
    ACH_SAVINGS_CTP_DEBIT = 38
    ACH_SAVINGS_CTX_CREDIT = 39
    ACH_SAVINGS_CTX_DEBIT = 40
    ACH_SAVINGS_CCD_PLUS_CREDIT = 41
    ACH_SAVINGS_CCD_PLUS_DEBIT = 43

    # Bills and promissory notes
    BILL_OF_EXCHANGE_AWAITING_ACCEPTANCE = 24
    ACCEPTED_BILL_OF_EXCHANGE = 44
    PROMISSORY_NOTE = 60
    PROMISSORY_NOTE_SIGNED_BY_DEBTOR = 61
    PROMISSORY_NOTE_SIGNED_BY_DEBTOR_ENDORSED_BY_BANK = 62
    PROMISSORY_NOTE_SIGNED_BY_DEBTOR_ENDORSED_BY_THIRD_PARTY = 63
    PROMISSORY_NOTE_SIGNED_BY_BANK = 64
    PROMISSORY_NOTE_SIGNED_BY_BANK_ENDORSED_BY_ANOTHER_BANK = 65
    PROMISSORY_NOTE_SIGNED_BY_THIRD_PARTY = 66
    PROMISSORY_NOTE_SIGNED_BY_THIRD_PARTY_ENDORSED_BY_BANK = 67
    BILL_DRAWN_BY_CREDITOR_ON_DEBTOR = 70
    BILL_DRAWN_BY_CREDITOR_ON_BANK = 74
    BILL_DRAWN_BY_CREDITOR_ENDORSED_BY_ANOTHER_BANK = 75
    BILL_DRAWN_BY_CREDITOR_ON_BANK_ENDORSED_BY_THIRD_PARTY = 76
    BILL_DRAWN_BY_CREDITOR_ON_THIRD_PARTY = 77
    BILL_DRAWN_BY_CREDITOR_ON_THIRD_PARTY_ENDORSED_BY_BANK = 78

    # Other methods
    HOLD = 8
    NATIONAL_OR_REGIONAL_CLEARING = 9
    BOOKENTRY_CREDIT = 15
    BOOKENTRY_DEBIT = 16
    PAYMENT_BY_POSTGIRO = 50
    FR_NORME_6_97_TELEREGLEMENT_CFONB = 51
    BANKGIRO = 56
    STANDING_AGREEMENT = 57
    REFERENCE_GIRO = 93
    URGENT_GIRO = 94
    FREE_FORMAT_GIRO = 95
    REQUESTED_METHOD_FOR_PAYMENT_WAS_NOT_USED = 96
    CLEARING_BETWEEN_PARTNERS = 97
    JP_ELECTRONICALLY_RECORDED_MONETARY_CLAIMS = 98

    @classmethod
    def get_description(cls, code: int) -> Optional[str]:
        """Returns a human-readable description for a payment means code.

        Args:
            code: The payment means code value

        Returns:
            Optional[str]: Description of the payment means or None if not found

        Examples:
            >>> PaymentMeansCode.get_description(30)
            'Credit transfer'
            >>> PaymentMeansCode.get_description(54)
            'Payment by credit card'
        """
        descriptions: Dict[int, str] = {
            30: "Credit transfer",
            58: "SEPA credit transfer",
            59: "SEPA direct debit",
            54: "Payment by credit card",
            55: "Payment by debit card",
            10: "Cash payment",
            49: "Direct debit",
            20: "Payment by cheque",
            68: "Online payment service",
            # Add more descriptions as needed
        }
        return descriptions.get(code)

    @classmethod
    def is_electronic_payment(cls, code: int) -> bool:
        """Determines if a payment means code represents an electronic payment method.

        Args:
            code: The payment means code value

        Returns:
            bool: True if the payment method is electronic

        Examples:
            >>> PaymentMeansCode.is_electronic_payment(58)
            True
            >>> PaymentMeansCode.is_electronic_payment(10)
            False
        """
        electronic_methods = {
            30, 31, 42, 45, 47, 48, 49, 54, 55, 58, 59, 68
        }
        return code in electronic_methods

    def __str__(self) -> str:
        """Returns a human-readable string representation of the payment means code.

        Returns:
            str: Description of the payment means or the enum name if no description
                 is available
        """
        description = self.get_description(self.value)
        return description or self.name.replace('_', ' ').title()