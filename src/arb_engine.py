from typing import Optional

from polymarket_api import get_yes_price_from_slug
from kalshi_api import get_market as get_kalshi_market


def get_kalshi_mid_price(ticker: str) -> Optional[float]:
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
            mid /= 100.0

        return mid
    except Exception as e:
        print(f"[Kalshi Error in get_kalshi_mid_price] {e}")
        return None


def _parse_teams_from_poly_slug(poly_slug: str):
    parts = poly_slug.split("-")
    yes_team = ""
    other_team = ""

    if len(parts) >= 3:
        yes_team = parts[1].upper()
        other_team = parts[2].upper()

    return yes_team, other_team


def _team_from_kalshi_ticker(kalshi_ticker: str) -> str:
    try:
        return kalshi_ticker.split("-")[-1].upper().strip()
    except Exception:
        return ""


def compute_spread_for_event(
    poly_slug: str,
    kalshi_ticker: str,
    label: Optional[str] = None,
    side: Optional[str] = None,
):
    poly_yes = get_yes_price_from_slug(poly_slug)
    kalshi_mid = get_kalshi_mid_price(kalshi_ticker)

    if poly_yes is None or kalshi_mid is None:
        return {
            "poly_price": poly_yes,
            "kalshi_mid_raw": kalshi_mid,
            "kalshi_same_side": None,
            "spread": None,
            "side_effective": None,
            "poly_team": None,
            "kalshi_team": None,
        }

    yes_team, other_team = _parse_teams_from_poly_slug(poly_slug)
    kalshi_team = _team_from_kalshi_ticker(kalshi_ticker)

    poly_yes_team = yes_team

    if kalshi_team == yes_team and yes_team:
        poly_prob_for_team = poly_yes
        side_effective = "poly_same_as_yes_team"
    elif kalshi_team == other_team and other_team:
        poly_prob_for_team = 1.0 - poly_yes
        side_effective = "poly_complement_of_yes_team"
    else:
        poly_prob_for_team = poly_yes
        side_effective = "poly_unknown_team_fallback"

    kalshi_prob_for_team = kalshi_mid

    spread = kalshi_prob_for_team - poly_prob_for_team

    return {
        "poly_price": poly_prob_for_team,
        "kalshi_mid_raw": kalshi_mid,
        "kalshi_same_side": kalshi_prob_for_team,
        "spread": spread,
        "side_effective": side_effective,
        "poly_team": poly_yes_team,
        "kalshi_team": kalshi_team,
    }
