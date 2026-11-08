
from datetime import datetime, timezone, timedelta
from typing import Literal

import httpx
from fastapi import APIRouter, HTTPException, Query

from app.services.rate_service import (
    fetch_exchange_rate,
    fetch_historical_rates
)


# Existing current-rate router
router = APIRouter(
    prefix="/api/v1/fx",
    tags=["FX Rates"]
)

# New historical-rate router
history_router = APIRouter(
    prefix="/api/v1/rates",
    tags=["FX History"]
)

DEFAULT_PROVIDER_MARKUP = 3.0

PERIOD_DAYS = {
    "1D": 1,
    "1W": 7,
    "1M": 30,
    "3M": 90,
    "1Y": 365
}


# Existing current exchange-rate API
@router.get("/rates")
async def get_exchange_rate(
    base: str = Query(default="USD", min_length=3, max_length=3),
    target: str = Query(default="INR", min_length=3, max_length=3)
):

    base = base.upper()
    target = target.upper()

    try:
        data = await fetch_exchange_rate(base, target)

        return {
            "currency_pair": f"{base}/{target}",
            "base_currency": data["base"],
            "target_currency": data["quote"],
            "exchange_rate": data["rate"],
            "rate_date": data["date"],
            "source": "Frankfurter",
            "rate_type": "Reference mid-market rate"
        }

    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))

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


# New historical exchange-rate API
@history_router.get("/history")
async def get_rate_history(
    pair: str = Query(default="USD/INR"),
    period: Literal["1D", "1W", "1M", "3M", "1Y"] = Query(default="1M")
):

    # Step 1: Validate currency pair
    currencies = pair.upper().split("/")

    if len(currencies) != 2:
        raise HTTPException(
            status_code=400,
            detail="Invalid pair. Use format USD/INR"
        )

    base, target = currencies

    # Step 2: Calculate date range
    end_date = datetime.now(timezone.utc).date()
    start_date = end_date - timedelta(
        days=PERIOD_DAYS[period]
    )

    try:
        # Step 3: Fetch historical rates
        history = await fetch_historical_rates(
            base=base,
            target=target,
            start_date=start_date.isoformat(),
            end_date=end_date.isoformat()
        )

        # Step 4: Format data for frontend
        result = []

        for item in history:

            mid_rate = float(item["rate"])

            provider_rate = mid_rate * (
                1 - DEFAULT_PROVIDER_MARKUP / 100
            )

            # Timestamp in milliseconds for JavaScript frontend
            date_value = datetime.strptime(
                item["date"], "%Y-%m-%d"
            ).replace(tzinfo=timezone.utc)

            timestamp = int(date_value.timestamp() * 1000)

            result.append({
                "date": item["date"],
                "timestamp": timestamp,

                "midMarket": round(mid_rate, 6),
                "provider": round(provider_rate, 6),

                "spread": round(
                    mid_rate - provider_rate, 6
                ),

                "markupPercent": DEFAULT_PROVIDER_MARKUP,

                # Frankfurter provides daily observations,
                # not intraday OHLC high/low values.
                "high": round(mid_rate, 6),
                "low": round(mid_rate, 6)
            })

        return result

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    except httpx.HTTPStatusError as error:
        if error.response.status_code == 404:
            raise HTTPException(
                status_code=404,
                detail="Historical currency data not found"
            )

        raise HTTPException(
            status_code=502,
            detail="Historical rate service error"
        )

    except httpx.RequestError:
        raise HTTPException(
            status_code=503,
            detail="Historical rate service unavailable"
        )
