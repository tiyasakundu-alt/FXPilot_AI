from app.schemas.transaction import Transaction


DEMO_TRANSACTIONS = [
    Transaction(
        id="FX-1001",
        date="2026-11-05",
        time="10:30 AM",
        currencyPair="USD/INR",
        fromCurrency="USD",
        toCurrency="INR",
        fromAmount=1000,
        toAmount=91000,
        midMarketRate=94.00,
        providerRate=91.00,
        fxMarkupPercent=3.19,
        fxMarkupLoss=31.91,
        status="High Markup",
        merchantName="Amazon",
        paymentMethod="PayPal",
        referenceId="DEMO-PP-1001"
    ),
    Transaction(
        id="FX-1002",
        date="2026-11-06",
        time="02:15 PM",
        currencyPair="EUR/INR",
        fromCurrency="EUR",
        toCurrency="INR",
        fromAmount=500,
        toAmount=46600,
        midMarketRate=95.00,
        providerRate=93.20,
        fxMarkupPercent=1.89,
        fxMarkupLoss=9.47,
        status="Optimized",
        merchantName="Microsoft",
        paymentMethod="PayPal",
        referenceId="DEMO-PP-1002"
    )
]


def get_all_transactions():
    return DEMO_TRANSACTIONS