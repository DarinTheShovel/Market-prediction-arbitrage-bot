# src/kalshi_demo.py
from kalshi_api import list_some_markets, get_market


def main():
    print("=== Some NFL / Pro Football markets ===")
    list_some_markets(search_term="pro football", limit=200)


if __name__ == "__main__":
    main()
