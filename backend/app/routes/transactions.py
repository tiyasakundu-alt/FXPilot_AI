
from fastapi import APIRouter, HTTPException, Query
from typing import Optional

from app.services.transaction_service import get_all_transactions

router = APIRouter(
    prefix="/api/v1/transactions",
    tags=["Transactions"]
)

@router.get("/")
async def get_transactions(
    status: Optional[str] = Query(default=None),
    currency_pair: Optional[str] = Query(default=None)
):
    try:
        transactions = get_all_transactions()

        if status:
            transactions = [
                tx for tx in transactions
                if tx.status == status
            ]

        if currency_pair:
            transactions = [
                tx for tx in transactions
                if tx.currencyPair.upper() == currency_pair.upper()
            ]

        return {
            "total": len(transactions),
            "transactions": [
                tx.model_dump() for tx in transactions
            ],
            "data_source": "DEMO"
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Unable to fetch transactions: {str(error)}"
        )
