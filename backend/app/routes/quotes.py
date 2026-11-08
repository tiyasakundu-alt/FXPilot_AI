from datetime import datetime, timezone
from uuid import uuid4
from typing import Literal

import httpx
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.services.rate_service import fetch_exchange_rate


router = APIRouter(
    prefix="/api/v1/quotes",
    tags=["FX Quotes"]
)


# Supported currencies
CurrencyCode = Literal[
    "USD", "INR", "EUR", "GBP",
    "JPY", "AUD", "CAD", "SGD"
]


# Demo assumption, NOT a verified PayPal markup
DEFAULT_PROVIDER_MARKUP = 3.0


# Illustrative assumptions, NOT live provider quotes
BENCHMARK_MARKUPS = {
    "wise": 0.6,
    "bankWire": 2.5,
    "stripe": 2.0
}


# Request validation
class QuoteRequest(BaseModel):
    from_currency: CurrencyCode
    to_currency: CurrencyCode
    amount: float = Field(
        gt=0,
        le=1_000_000_000,
        description="Amount to convert"
    )


# Benchmark calculation
def calculate_benchmark(amount, mid_rate, markup):

    rate = mid_rate * (1 - markup / 100)
    received = amount * rate

    return {
        "rate": round(rate, 6),
        "received": round(received, 2),
        "fee": 0.0,
        "markupPercent": markup
    }


# Main FX quote API
@router.post("/calculate")
async def calculate_quote(request: QuoteRequest):

    base = request.from_currency
    target = request.to_currency

    # Step 1: Get reference exchange rate
    if base == target:

        mid_rate = 1.0
        rate_date = datetime.now(timezone.utc).date().isoformat()
        rate_source = "Identity conversion"

    else:

        try:
            rate_data = await fetch_exchange_rate(base, target)

            mid_rate = float(rate_data["rate"])
            rate_date = rate_data["date"]
            rate_source = "Frankfurter"

        except httpx.HTTPStatusError as error:

            if error.response.status_code == 404:
                raise HTTPException(
                    status_code=404,
                    detail="Currency pair not found"
                )

            raise HTTPException(
                status_code=502,
                detail="External exchange-rate service error"
            )

        except httpx.RequestError:

            raise HTTPException(
                status_code=503,
                detail="Exchange-rate service unavailable"
            )

        except (KeyError, TypeError, ValueError):

            raise HTTPException(
                status_code=502,
                detail="Invalid exchange-rate response"
            )

    # Step 2: Apply assumed provider markup
    markup = DEFAULT_PROVIDER_MARKUP

    provider_rate = mid_rate * (1 - markup / 100)

    # Step 3: Calculate converted amounts
    converted_mid = request.amount * mid_rate

    converted_provider = request.amount * provider_rate

    # Step 4: Calculate conversion difference
    difference = converted_mid - converted_provider

    # Step 5: Calculate benchmark estimates
    benchmarks = {
        "wise": calculate_benchmark(
            request.amount,
            mid_rate,
            BENCHMARK_MARKUPS["wise"]
        ),

        "bankWire": calculate_benchmark(
            request.amount,
            mid_rate,
            BENCHMARK_MARKUPS["bankWire"]
        ),

        "stripe": calculate_benchmark(
            request.amount,
            mid_rate,
            BENCHMARK_MARKUPS["stripe"]
        )
    }

    # Step 6: Return quote
    return {
        "id": str(uuid4()),

        "fromCurrency": base,
        "toCurrency": target,
        "amount": request.amount,

        "midMarketRate": round(mid_rate, 6),
        "providerRate": round(provider_rate, 6),

        "markupPercent": markup,
        "markupAmount": round(difference, 2),

        "convertedMidMarket": round(converted_mid, 2),
        "convertedProvider": round(converted_provider, 2),

        "differenceAmount": round(difference, 2),

        "timestamp": datetime.now(timezone.utc).isoformat(),

        "providerName": "Demo provider estimate",

        "rateDate": rate_date,
        "rateSource": rate_source,

        "benchmarkNote": (
            "Wise, Bank Wire and Stripe values are illustrative estimates, "
            "not live provider quotes. Actual provider fees may differ."
        ),

        "benchmarks": benchmarks
    }
