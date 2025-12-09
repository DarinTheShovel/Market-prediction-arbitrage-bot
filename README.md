# Market Prediction Arbitrage Bot

## Polymarket × Kalshi Price Comparison Tool

### Status: Work in Progress

This project implements a lightweight framework for comparing binary-event prices between Polymarket and Kalshi.
It retrieves live market prices from both platforms, aligns outcomes across markets, and computes the probability spread between the two.

# The project is a work in progress, intended to demonstrate API integration, data processing, and modular code design.

# What the Project Does

Fetches live YES probabilities from Polymarket

Fetches bid/ask prices for each outcome from Kalshi

Converts Kalshi prices into mid-market probabilities

Aligns Polymarket YES and Kalshi outcomes (including complementary events)

Computes pricing differences (“spreads”) between platforms

Supports batch evaluation of multiple events defined in a config file

# Directory Structure
mktprediction_arb/
│
├── config/
│   └── events.csv          # list of events to evaluate
│
├── data/
│   ├── sample_prices.csv
│   └── scan_results.csv    # automatically generated
│
├── src/
│   ├── polymarket_api.py
│   ├── polymarket_demo.py
│   ├── kalshi_api.py
│   ├── kalshi_demo.py
│   ├── kalshi_tickerfinder.py
│   ├── arb_engine.py
│   ├── scan_events.py
│   ├── cross_arb_demo.py
│   └── list_markets_demo.py
│
└── plots/                  # placeholder for visualization

Example Event Configuration (config/events.csv)
```bash
label,poly_slug,kalshi_ticker,side
BAL vs CIN - BAL win,nfl-bal-cin-2025-12-14,KXNFLGAME-25DEC14BALCIN-BAL,same
BAL vs CIN - CIN win,nfl-bal-cin-2025-12-14,KXNFLGAME-25DEC14BALCIN-CIN,complement
```

Each row defines:

the event label

the Polymarket slug

the Kalshi ticker

whether the Kalshi ticker corresponds to the same side or the complementary side of Polymarket’s YES

# Running the Scanner
```bash
python src/scan_events.py
```

Results are written to:
```bash
data/scan_results.csv
```
# Output Example
```bash
=== BAL vs CIN – BAL win ===
Polymarket YES:      0.565
Kalshi mid (raw):    0.565
Kalshi aligned:      0.565
Spread:              0.000
```
Purpose and Status

# This project is meant to demonstrate:

API-based data ingestion

Transforming market microstructure differences into comparable metrics

Building a modular and extendable codebase

The project is ongoing. Planned additions include:

automatic event matching

visualization tools

expanded support for spreads, totals, and other market types

and more