from polymarket_api import get_market_by_slug, get_yes_price_from_market

def main():
    slug = "will-trump-win-the-2020-us-presidential-election"

    market = get_market_by_slug(slug)
    price = get_yes_price_from_market(market)

    print("Market question:", market.get("question"))
    print("YES price:", price)

if __name__ == "__main__":
    main()
