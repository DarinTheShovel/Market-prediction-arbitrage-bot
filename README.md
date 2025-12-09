# Market Prediction Arbitrage Bot
## Polymarket × Kalshi Price Comparison Tool
### Status: Work in Progress

This project implements a lightweight framework for comparing binary-event prices between Polymarket and Kalshi. It retrieves live market prices from both platforms, aligns outcomes across markets, and computes the probability spread between the two.

# The goal is to demonstrate:

- API-based data ingestion

- Transforming market microstructure differences into comparable metrics

- Building a modular and extendable codebase for cross-exchange analysis

- What the Project Does:

- Fetches live YES probabilities from Polymarket

- Fetches bid/ask prices for each outcome from Kalshi

- Converts Kalshi prices into mid-market probabilities

- Aligns Polymarket YES and Kalshi outcomes, including complementary events

- Computes pricing differences (“spreads”) between platforms

- Supports batch evaluation of multiple events defined in a config file

# Directory Structure (description only):
The project includes:

- A config folder containing event definitions (events.csv)

- A data folder containing sample outputs and scanned results

- A src folder containing modules for Polymarket API access, Kalshi API access, ticker matching tools, spread calculation logic, and the main batch scanner

- A plots folder reserved for future visualizations

# Example Event Configuration:
Each row in events.csv includes:
label: a human-readable description of the event
poly_slug: the Polymarket slug for the outcome
kalshi_ticker: the corresponding Kalshi market ticker
side: indicates whether Kalshi’s price corresponds to the same side or complement of Polymarket’s YES outcome

# Running the Scanner:
From the project root, run the main scanner script.
```bash
python src/scan_events.py 
``` 
Results will be saved inside data/scan_results.csv.

# Example Output Explanation:
For each event, the system prints Polymarket YES probability, Kalshi’s mid price, the aligned side probability (same or complement), and the final spread between the two markets.

# Planned Additions:

- Automatic event matching between Polymarket and Kalshi

- Visualization tools for spreads and time series

- Expanded support for spreads, totals, and other market types

- And More