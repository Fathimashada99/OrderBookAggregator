import requests
import argparse
import time

def RateLimiter(interval):
    api_last_called = {}
    def call_api(key):
        current_time = time.time()
        if key not in api_last_called or current_time - api_last_called[key] >= interval:
            api_last_called[key] = current_time
            return True
        return False
    return call_api

limiter = RateLimiter(2)

def coinbase():
    endpoint = "https://api.exchange.coinbase.com/products/BTC-USD/book?level=2"
    if limiter("coinbase"):
        try:
            response = requests.get(endpoint, timeout=5).json()
            bids = [[float(price), float(amount)] for price, amount, _ in response["bids"]]
            asks = [[float(price), float(amount)] for price, amount, _ in response["asks"]]
            return bids, asks
        except (requests.RequestException, ValueError, KeyError) as e:
            print(f"[Error] Coinbase API failed: {e}")
    return [], []

def gemini():
    endpoint = "https://api.gemini.com/v1/book/BTCUSD"
    if limiter("gemini"): 
        try:
            response = requests.get(endpoint, timeout=5).json()
            bids = [[float(entry['price']), float(entry['amount'])] for entry in response['bids']]
            asks = [[float(entry['price']), float(entry['amount'])] for entry in response['asks']]
            return bids, asks
        except (requests.RequestException, ValueError, KeyError) as e:
            print(f"[Error] Gemini API failed: {e}")
    return [], []

def combine_orderbook(bids_list, asks_list):
    combined_bids = []
    combined_asks = []
    for bids in bids_list:
        combined_bids += bids
    for asks in asks_list:
        combined_asks += asks
    combined_bids.sort(key=lambda x: x[0], reverse=True)
    combined_asks.sort(key=lambda x: x[0])
    return combined_bids, combined_asks

def calculate_execution_prices(orderbook, qty_required):
    total_qty = 0.0
    total_price = 0.0
    for price, size in orderbook:
        use_qty = min(size, qty_required - total_qty)
        total_qty += use_qty
        total_price += use_qty * price
        if total_qty >= qty_required:
            break
    return total_price

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="BTC-USD Order Book Aggregator")
    parser.add_argument("--qty", type=float, default=10, help="Quantity of BTC to buy/sell")
    args = parser.parse_args()
    qty_required = args.qty
    coinbase_bids, coinbase_asks = coinbase()
    gemini_bids, gemini_asks = gemini()
    combined_bids, combined_asks = combine_orderbook(
        [coinbase_bids, gemini_bids],
        [coinbase_asks, gemini_asks])
    cost_price = calculate_execution_prices(combined_asks, qty_required)
    selling_price = calculate_execution_prices(combined_bids, qty_required)
    print("Backend Coding Challenge-Order Book Aggregator")
    print(f"To buy {qty_required} BTC: ${cost_price:,.2f}")
    print(f"To sell {qty_required} BTC: ${selling_price:,.2f}")

