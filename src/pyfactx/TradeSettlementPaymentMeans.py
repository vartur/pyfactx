from typing import Optional

from pydantic import BaseModel, Field

from .CreditorFinancialAccount import CreditorFinancialAccount
from .DebtorFinancialAccount import DebtorFinancialAccount
from .PaymentMeansCode import PaymentMeansCode


class TradeSettlementPaymentMeans(BaseModel):
    payment_means_code: PaymentMeansCode = Field(...)
    payer_party_debtor_financial_account: Optional[DebtorFinancialAccount] = Field(default=None)
    payee_party_creditor_financial_account: Optional[CreditorFinancialAccount] = Field(default=None)
