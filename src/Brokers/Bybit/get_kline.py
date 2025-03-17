import pandas as pd
from src.Brokers.Bybit.client import session

def get_kline(symbol="BTCUSDT", interval="1", limit=1000):
    """
    Retrieves historical candlestick (K-line) data for a given symbol.
    """
    try:
        response = session.get_kline(category="linear", symbol=symbol, interval=interval, limit=limit)

        candles = response.get("result", {}).get("list", [])
        if not candles:
            return {"error": "No candlestick data found."}

        df = pd.DataFrame(candles, columns=["timestamp", "open", "high", "low", "close", "volume", "turnover"])

        # ✅ Ensure timestamps are numeric before converting
        df["timestamp"] = pd.to_numeric(df["timestamp"], errors="coerce")  # Convert to numeric first
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")  # Then convert to datetime

        # Convert numerical columns to float
        numeric_cols = ["open", "high", "low", "close", "volume", "turnover"]
        df[numeric_cols] = df[numeric_cols].astype(float)

        df = df.sort_values(by="timestamp", ascending=True)
        return df

    except Exception as e:
        return {"error": f"Error retrieving candlestick data: {e}"}
