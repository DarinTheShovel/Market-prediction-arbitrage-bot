# src/kalshi_api.py
import requests

BASE_URL = "https://api.elections.kalshi.com/trade-api/v2"


def get_market(ticker: str) -> dict:
    url = f"{BASE_URL}/markets"
    params = {
        "tickers": ticker,
        "limit": 1,
    }
    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    markets = data.get("markets", [])
    if not markets:
        raise ValueError(f"No market found for ticker {ticker}")
    return markets[0]


def list_some_markets(search_term: str | None = None, limit: int = 10):
    url = f"{BASE_URL}/markets"
    params = {
        "limit": limit,
        "status": "open",
    }
    if search_term:
        params["search"] = search_term

    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    markets = data.get("markets", [])

    for m in markets:
        print("ticker  :", m.get("ticker", ""))
        print("title   :", m.get("title", ""))
        print("category:", m.get("category", ""))
        print("yes_bid :", m.get("yes_bid"), " yes_ask:", m.get("yes_ask"))
        print("-" * 60)

    return markets
