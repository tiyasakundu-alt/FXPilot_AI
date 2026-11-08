import httpx

BASE_URL = "https://api.frankfurter.dev/v2"

SUPPORTED_CURRENCIES = {
    "USD", "INR", "EUR", "GBP",
    "JPY", "AUD", "CAD", "SGD"
}


async def fetch_exchange_rate(base: str, target: str):

    base = base.upper()
    target = target.upper()

    # Validate currency codes
    if base not in SUPPORTED_CURRENCIES:
        raise ValueError(f"Unsupported base currency: {base}")

    if target not in SUPPORTED_CURRENCIES:
        raise ValueError(f"Unsupported target currency: {target}")

    url = f"{BASE_URL}/rate/{base.lower()}/{target.lower()}"

    async with httpx.AsyncClient(timeout=10.0) as client:

        response = await client.get(url)
        response.raise_for_status()

        data = response.json()

    # Validate API response
    required_fields = {"date", "base", "quote", "rate"}

    if not required_fields.issubset(data.keys()):
        raise ValueError("Invalid response from exchange-rate API")

    if data["base"] != base or data["quote"] != target:
        raise ValueError("Currency pair mismatch in API response")

    rate = float(data["rate"])

    if rate <= 0:
        raise ValueError("Invalid exchange rate received")

    return {
        "date": data["date"],
        "base": data["base"],
        "quote": data["quote"],
        "rate": rate
    }

async def fetch_historical_rates(
    base: str,
    target: str,
    start_date: str,
    end_date: str
):
    base = base.upper()
    target = target.upper()

    if base not in SUPPORTED_CURRENCIES:
        raise ValueError(f"Unsupported base currency: {base}")

    if target not in SUPPORTED_CURRENCIES:
        raise ValueError(f"Unsupported target currency: {target}")

    url = f"{BASE_URL}/rates"

    params = {
        "base": base,
        "quotes": target,
        "from": start_date,
        "to": end_date
    }

    async with httpx.AsyncClient(timeout=15.0) as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
        data = response.json()

    if not isinstance(data, list):
        raise ValueError("Invalid historical rates response")

    for item in data:
        if not {"date", "base", "quote", "rate"}.issubset(item):
            raise ValueError("Invalid historical rate record")

        if item["base"] != base or item["quote"] != target:
            raise ValueError("Currency pair mismatch")

        if float(item["rate"]) <= 0:
            raise ValueError("Invalid historical exchange rate")

    return data

