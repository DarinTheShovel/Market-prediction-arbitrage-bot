import csv
from pathlib import Path
from arb_engine import compute_spread_for_event


CONFIG_PATH = Path(__file__).resolve().parents[1] / "config" / "events.csv"


def main():
    rows = []

    with CONFIG_PATH.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            label = row["label"]
            poly_slug = row["poly_slug"]
            kalshi_ticker = row["kalshi_ticker"]
            side = row.get("side") or "auto"

            print(f"\n=== {label} ===")
            result = compute_spread_for_event(
                poly_slug,
                kalshi_ticker,
                label=label,
                side=side,
            )

            poly_p = result["poly_price"]
            kalshi_mid_raw = result["kalshi_mid_raw"]
            kalshi_same = result["kalshi_same_side"]
            spread = result["spread"]
            side_used = result.get("side_effective")

            print(f"Polymarket YES:      {poly_p}")
            print(f"Kalshi mid (raw):    {kalshi_mid_raw}")
            print(f"Kalshi same-side p:  {kalshi_same}")
            print(f"Side used:           {side_used}")
            print(f"Spread (Kalshi-Poly): {spread}")

            rows.append({
                "label": label,
                "poly_slug": poly_slug,
                "kalshi_ticker": kalshi_ticker,
                "side_input": side,
                "side_effective": side_used,
                "poly_price": poly_p,
                "kalshi_mid_raw": kalshi_mid_raw,
                "kalshi_same_side": kalshi_same,
                "spread": spread,
            })

    out_path = Path(__file__).resolve().parents[1] / "data" / "scan_results.csv"
    if rows:
        with out_path.open("w", newline="", encoding="utf-8") as f:
            fieldnames = list(rows[0].keys())
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

        print(f"\nSaved results to {out_path}")
    else:
        print("\nNo rows produced; check events.csv content.")


if __name__ == "__main__":
    main()
