import requests
import json

BASE_URL = "https://gamma-api.polymarket.com"


def get_market_by_slug(slug: str) -> dict:
    url = f"{BASE_URL}/markets/slug/{slug}"
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    return resp.json()


def _maybe_parse_json(value):
    """
    如果 value 是类似 "[...]" 或 "{...}" 的字符串，就尝试 json.loads，否则原样返回。
    """
    if isinstance(value, str):
        s = value.strip()
        if (s.startswith("[") and s.endswith("]")) or (s.startswith("{") and s.endswith("}")):
            try:
                return json.loads(s)
            except Exception:
                return value
    return value


def get_yes_price_from_market(market: dict):
    """
    获取 Polymarket 市场的一个代表性 YES 价格。

    支持：
    1. Event 包一层 "markets": [...]（sports 常见） -> 递归第一个子市场
    2. Sports / orderbook 结构：yes_bid / yes_ask
    3. 普通 outcomePrices 结构：outcomes + outcomePrices（可能是 JSON 字符串）
    """

    # ---- Case 0: event -> markets[0] ----
    if "markets" in market and isinstance(market["markets"], list) and market["markets"]:
        first_sub_market = market["markets"][0]
        return get_yes_price_from_market(first_sub_market)

    # ---- Case 1: yes_bid / yes_ask ----
    if "yes_bid" in market and "yes_ask" in market:
        try:
            yes_bid = float(market.get("yes_bid") or 0)
            yes_ask = float(market.get("yes_ask") or 0)
        except Exception:
            yes_bid = yes_ask = 0.0

        if yes_bid == 0 and yes_ask == 0:
            return None

        return (yes_bid + yes_ask) / 2.0

    # ---- Case 2: outcomes + outcomePrices ----
    raw_outcomes = market.get("outcomes") or []
    raw_prices = market.get("outcomePrices") or []

    outcomes = _maybe_parse_json(raw_outcomes)
    prices = _maybe_parse_json(raw_prices)

    # 确保最终是 list
    if not isinstance(outcomes, (list, tuple)) or not isinstance(prices, (list, tuple)):
        return None
    if len(outcomes) == 0 or len(prices) == 0:
        return None

    # 找 YES 的 index
    yes_index = None
    for i, name in enumerate(outcomes):
        if isinstance(name, str) and name.lower() == "yes":
            yes_index = i
            break
    if yes_index is None:
        yes_index = 0  # fallback：没有 YES 就取第一个

    if yes_index >= len(prices):
        return None

    raw_p = prices[yes_index]

    try:
        p = float(raw_p)
    except Exception:
        return None

    # 如果价格大于 1，大概率是 0~100 的“美分”
    if p > 1.0:
        p = p / 100.0

    return p

def list_some_markets(limit: int = 10):
   
    url = f"{BASE_URL}/markets"
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    data = resp.json()

    print(f"Total markets returned: {len(data)}")
    print("Showing first few markets:\n")

    for m in data[:limit]:
        print("slug:", m.get("slug"))
        print("question:", m.get("question"))
        print("-" * 40)

def get_yes_price_from_slug(slug: str):
    try:
        market = get_market_by_slug(slug)
        return get_yes_price_from_market(market)
    except Exception as e:
        print(f"[Poly Error in get_yes_price_from_slug] {e}")
        return None
