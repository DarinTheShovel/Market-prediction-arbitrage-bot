# Usage Guide

This project evaluates pricing differences between Polymarket and Kalshi for binary events. This guide explains how to run the scanner and interpret the output.

1. Install Dependencies Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. Configure Events 
Events are pre-loaded here, for different events tickers for Kalshi and Polymarket varies. Events can be configured in 
```bash
config/events.csv. 
```
Each row defines one outcome to evaluate.

3. Run the Scanner
```bash
python src/scan_events.py
```
Results will be written to 
```bash
data/scan_results.csv
```
4. Example Output 
```bash
=== BAL vs CIN – BAL win ===
Polymarket YES:      0.565
Kalshi mid (raw):    0.565
Kalshi aligned:      0.565
Spread:              0.000
```
5. Notes 

This Project is a work in progress Only binary events are supported currently Data reflects live market conditions and may change rapidly