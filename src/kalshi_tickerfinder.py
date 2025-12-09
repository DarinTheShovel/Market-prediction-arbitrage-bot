import requests

BASE_URL = "https://api.elections.kalshi.com/trade-api/v2"


def search_nfl_markets(series_ticker: str = "KXNFLGAME", team_filter: str | None = None):
    url = f"{BASE_URL}/markets"
    params = {
        "series_ticker": series_ticker,
        "status": "open",
        "limit": 100,
    }

    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    markets = data.get("markets", [])

    print(f"Total markets in {series_ticker} (status=open): {len(markets)}\n")

    team_filter_l = team_filter.lower() if team_filter else None

    for m in markets:
        ticker = m.get("ticker", "")
        title = m.get("title", "")
        category = m.get("category", "")
        yes_bid = m.get("yes_bid")
        yes_ask = m.get("yes_ask")

        text = (ticker + " " + title + " " + category).lower()
        if team_filter_l and team_filter_l not in text:
            continue

        print("ticker  :", ticker)
        print("title   :", title)
        print("category:", category)
        print("yes_bid :", yes_bid, " yes_ask:", yes_ask)
        print("-" * 60)

    return markets


if __name__ == "__main__":
    search_nfl_markets(team_filter="PHI")
