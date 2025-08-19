## Objective
**Build a BTC-USD order book aggregator** that fetches live data from multiple crypto exchanges (Coinbase Pro and Gemini) and calculates the best execution price to buy or sell a given quantity of Bitcoin.  
This project demonstrates working with real-world APIs, handling raw data, and writing clean Python scripts.

---

## Real-World Scenario
This simulates a pricing engine for a crypto platform that aggregates liquidity from multiple exchanges.  
**Goal:** Determine how much it would cost to buy or sell a specified quantity of BTC (default 10 BTC) using the best available offers.

---

## Features / Task Implementation
- **Fetches order books from:**
  - Coinbase Pro: `https://api.exchange.coinbase.com/products/BTC-USD/book?level=2`
  - Gemini: `https://api.gemini.com/v1/book/BTCUSD`
- **Parses responses** into normalized lists:
  ```python
  bids = [[price, size], ...]  # sorted descending
  asks = [[price, size], ...]  # sorted ascending
**Custom RateLimiter** (closure-based) to limit API calls to once every 2 seconds per exchange
- **Calculates execution prices:**
  - **Buy:** Walk down the asks (lowest prices first) to sum the cost
  - **Sell:** Walk up the bids (highest prices first) to sum the revenue
  - Combines liquidity from both exchanges
- **Supports CLI argument `--qty`** to specify BTC quantity (default 10 BTC)
- **Outputs results in readable format**, e.g.:
To buy 10 BTC: $XXX,XXX.XX
To sell 10 BTC: $YYY,YYY.YY
---

## Code Explanation

- **Imports:** `requests` for API calls, `argparse` for CLI arguments, `time` for rate limiting
- **Rate Limiter:** Ensures each API is called at most once every 2 seconds
- **Fetching Order Books:** `coinbase()` and `gemini()` fetch data and normalize it into `[price, size]` lists; handles errors gracefully
- **Combining Order Books:** `combine_orderbook()` merges bids and asks from both exchanges
- **Calculating Execution Prices:** `calculate_execution_prices()` computes total cost to buy or total revenue to sell the requested BTC quantity
- **Command-Line Interface:** `--qty` allows specifying BTC quantity; prints formatted output

---

## **Setup Instructions**

1. **Clone the repo:**
 ```bash
 git clone https://github.com/Fathimashada99/OrderBookAggregator.git
 cd OrderBookAggregator
```
2. **Create and Activate a Virtual Environment:**
```powershell
python -m venv myvenv
.\myvenv\Scripts\activate
```
3. **Install dependencies:**
```powershell
 pip install requests
```
5. **Run the script**
```powershell
 python order_book_aggregator.py --qty 10
```

---

## **Sample Output**
```bash
Backend Coding Challenge – Order Book Aggregator
To buy 5 BTC: $150,000.00
To sell 5 BTC: $150,500.00
```
