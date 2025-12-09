from polymarket_api import get_market_by_slug, get_yes_price_from_market
from kalshi_api import get_market as get_kalshi_market


POLY_SLUG = "nfl-phi-lac-2025-12-08"
KALSHI_TICKER = "KXNFLGAME-25DEC08PHILAC-PHI"



def get_polymarket_price(slug: str):
    try:
        market = get_market_by_slug(slug)
        price = get_yes_price_from_market(market)
        return price
    except Exception as e:
        print(f"[Polymarket Error] {e}")
        return None


def get_kalshi_mid_price(ticker: str):
    try:
        m = get_kalshi_market(ticker)

        yes_bid_raw = m.get("yes_bid")
        yes_ask_raw = m.get("yes_ask")

        if yes_bid_raw is None or yes_ask_raw is None:
            return None

        yes_bid = float(yes_bid_raw)
        yes_ask = float(yes_ask_raw)

        if yes_bid == 0 and yes_ask == 0:
            return None

        mid = (yes_bid + yes_ask) / 2.0

        if mid > 1.0:
            mid = mid / 100.0

        return mid

    except Exception as e:
        print(f"[Kalshi Error] {e}")
        return None


def main():
    print("=== Cross-Platform Arbitrage Demo ===")

    poly_price = get_polymarket_price(POLY_SLUG)
    print(f"Polymarket YES price: {poly_price}")

    if KALSHI_TICKER:
        kalshi_mid = get_kalshi_mid_price(KALSHI_TICKER)
        print(f"Kalshi mid price:     {kalshi_mid}")
    else:
        kalshi_mid = None
        print("Kalshi ticker = None")

    if poly_price is not None and kalshi_mid is not None:
        spread = kalshi_mid - poly_price
        print(f"Spread (Kalshi - Poly): {spread:.4f}")
    else:
        print("Spread Unavailable（Prices not available）")


if __name__ == "__main__":
    main()
