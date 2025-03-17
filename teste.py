from src.Brokers.Bybit.get_wallet_balance import get_wallet_balance
from src.Brokers.Bybit.get_positions import get_positions
from src.Brokers.Bybit.get_kline import get_kline
from src.Brokers.Bybit.get_instruments_info import get_instrument_info
import math
import time
from enum import Enum
from src.indicators.trend_indicatores.ewm import calculate_ewm
from src.Brokers.Bybit.place_order import place_order

# Trading Constants
SYMBOL = "SOLUSDT"
INTERVAL = "1"
LIMIT = 1000
STOP_PERCENT = 0.01
SLEEP_TIME = 5

class TradeState(Enum):
    NO_TRADES = "No_Trades"
    PURCHASED = "Purchased"
    SOLD = "Sold"

trade_state = TradeState.NO_TRADES
entry_price = None
stop_loss = None
take_profit = None
trade_amount = 0.0

def trading_bot():
    global trade_state, entry_price, stop_loss, take_profit, trade_amount

    while True:
        print("\n📊 Fetching account balance...")
        balance = get_wallet_balance()
        wallet_balance = float(balance.get("walletBalance", 0.0))
        print(f"💰 Wallet Balance: {wallet_balance:.2f} USDT")

        print("\n📈 Checking open trades...")
        position_info = get_positions()
        open_position = False

        if "error" in position_info:
            print(f"❌ Error retrieving positions: {position_info['error']}")
        elif "message" in position_info and position_info["message"] == "No open trades.":
            print("🔒 No open trades.")
        else:
            # We assume "status": "success" and "position": {...}
            pos = position_info.get("position", {})
            print("🔓 Open Trade Found:")
            print(f"   Symbol: {pos.get('symbol')}")
            print(f"   Side: {pos.get('side')}")
            print(f"   Size: {pos.get('size')}")
            print(f"   Avg. Price: {pos.get('avgPrice')}")
            print(f"   Leverage: {pos.get('leverage')}")
            print(f"   Position Value: {pos.get('positionValue')}")
            print(f"   Unrealised PnL: {pos.get('unrealisedPnl')}")
            open_position = True  # There's an active position on the exchange

        print("\n🔍 Fetching instrument info...")
        instrument_data = get_instrument_info(symbol=SYMBOL, category="linear")
        symbol_      = instrument_data.get("symbol")
        min_order_qty = float(instrument_data.get("minOrderQty", "0.0"))
        
        print(f"🔹 Symbol: {symbol_}")
        print(f"🔹 Min Order Qty: {min_order_qty}")

        print("\n📉 Fetching market data...")
        df_candles = get_kline(symbol=SYMBOL, interval=INTERVAL, limit=LIMIT)

        if not isinstance(df_candles, dict) and len(df_candles) >= 1:
            last_price = float(df_candles.iloc[-1]["close"])
            print(f"✅ Last Price: {last_price}")

            # ================
            # If NO position, BUY
            # ================
            if not open_position:
                # Calculate how many SOL with entire wallet
                raw_trade_amount = wallet_balance / last_price

                # Truncate to multiple of min_order_qty
                # Example: If raw_trade_amount=0.238, min_order_qty=0.1
                # floor(0.238 / 0.1)=2 -> 2*0.1=0.2
                trade_amount = math.floor(raw_trade_amount / min_order_qty) * min_order_qty
                trade_amount = round(trade_amount, 3)  # Round to 3 decimals

                # If can't buy at least min_order_qty, skip
                if trade_amount < min_order_qty:
                    print(f"❌ Not enough balance to buy minimum. trade_amount={trade_amount}")
                    time.sleep(SLEEP_TIME)
                    continue

                # Define Stop-Loss and Take-Profit at 1%
                entry_price = last_price
                stop_loss   = entry_price * (1 - STOP_PERCENT)
                take_profit = entry_price * (1 + STOP_PERCENT)

                print(f"\n🚀 BUY Signal! Market order using entire balance.")
                print(f"   Entry Price: {entry_price:.4f}")
                print(f"   Stop Loss:   {stop_loss:.4f}  (-1%)")
                print(f"   Take Profit: {take_profit:.4f}  (+1%)")
                print(f"   trade_amount: {trade_amount} SOL (~{wallet_balance:.2f} USDT)")

                order_response = place_order(
                    symbol=SYMBOL,
                    side="Buy",
                    qty=trade_amount,
                    order_type="Market",
                    stop_loss=stop_loss,
                    take_profit=take_profit,
                    position_idx=1  # One-Way Mode
                )

                if order_response.get("retCode") == 0:
                    print("✅ Buy order placed successfully!")
                else:
                    print(f"\n❌ Order Failed: {order_response.get('retMsg')}")

        else:
            print("❌ Error or insufficient data in df_candles")

        print("\n⏳ Waiting for the next candle...")
        time.sleep(SLEEP_TIME)

if __name__ == "__main__":
    trading_bot()