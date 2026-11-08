
import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from app.routes.rates import router as rates_router, history_router
from app.services.rate_service import fetch_exchange_rate
from app.routes.quotes import router as quotes_router
from app.routes.transactions import router as transactions_router
from fastapi.middleware.cors import CORSMiddleware
from app.routes.auth import router as auth_router

app = FastAPI(
    title="FXPilot AI Backend",
    description="Intelligent FX Shield and Smart Route Agent",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(rates_router)
app.include_router(history_router)
app.include_router(quotes_router)
app.include_router(transactions_router)
app.include_router(auth_router)


class FXQuoteRequest(BaseModel):
    amount: float = Field(gt=0, description="Amount in USD")
    markup_percent: float = Field(
        ge=0,
        le=100,
        description="Assumed provider markup percentage"
    )


@app.get("/")
def home():
    return {
        "message": "Welcome to FXPilot AI Backend!",
        "status": "Running",
        "developer": "Member 2 - Backend"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/api/v1/fx/quote")
async def create_fx_quote(request: FXQuoteRequest):

    # Step 1: Fetch the reference USD/INR rate automatically
    try:
        rate_data = await fetch_exchange_rate("USD", "INR")
        mid_market_rate = float(rate_data["rate"])

    except httpx.HTTPStatusError as error:
        if error.response.status_code == 404:
            raise HTTPException(
                status_code=404,
                detail="USD/INR currency pair not found"
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

    # Step 2: Calculate the reference value
    mid_market_amount = request.amount * mid_market_rate

    # Step 3: Apply the assumed provider markup
    provider_rate = mid_market_rate * (
        1 - request.markup_percent / 100
    )

    # Step 4: Calculate the amount received
    received_amount = request.amount * provider_rate

    # Step 5: Calculate conversion cost
    conversion_cost = mid_market_amount - received_amount

    # Step 6: Return the complete quote
    return {
        "currency_pair": "USD/INR",
        "input_amount_usd": round(request.amount, 2),
        "mid_market_rate": mid_market_rate,
        "provider_rate": round(provider_rate, 4),
        "mid_market_value_inr": round(mid_market_amount, 2),
        "received_amount_inr": round(received_amount, 2),
        "conversion_cost_inr": round(conversion_cost, 2),
        "markup_percent": request.markup_percent,
        "rate_date": rate_data["date"],
        "rate_source": "Frankfurter"
    }
