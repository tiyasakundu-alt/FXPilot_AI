
from typing import Literal
from pydantic import BaseModel, Field

CurrencyCode = Literal[
    "USD", "INR", "EUR", "GBP",
    "JPY", "AUD", "CAD", "SGD"
]

TransactionStatus = Literal[
    "Optimized",
    "Standard",
    "High Markup",
    "Pending Review"
]

class Transaction(BaseModel):
    id: str
    date: str
    time: str
    currencyPair: str
    fromCurrency: CurrencyCode
    toCurrency: CurrencyCode
    fromAmount: float = Field(gt=0)
    toAmount: float = Field(ge=0)
    midMarketRate: float = Field(gt=0)
    providerRate: float = Field(gt=0)
    fxMarkupPercent: float = Field(ge=0)
    fxMarkupLoss: float = Field(ge=0)
    status: TransactionStatus
    merchantName: str
    paymentMethod: str
    referenceId: str
