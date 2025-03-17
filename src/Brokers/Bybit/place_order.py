from src.Brokers.Bybit.client import session

def place_order(
    symbol,
    side,
    qty,
    price=None,
    order_type="Market",
    stop_loss=None,
    take_profit=None,
    position_idx=0  # <-- For One-Way Mode by default
):
    """
    Places a buy or sell order on Bybit and prints debug information.
    
    :param symbol: The trading pair (e.g., "BTCUSDT")
    :param side: "Buy" or "Sell"
    :param qty: Order quantity (e.g., 0.001 BTC)
    :param price: Limit order price (None for Market)
    :param order_type: "Market" (default) or "Limit"
    :param stop_loss: Optional stop-loss price
    :param take_profit: Optional take-profit price
    :param position_idx: 0 (One-Way Mode), 1 or 2 (Hedge Mode)
    :return: API response
    """
    try:
        order_params = {
            "category": "linear",
            "symbol": symbol,
            "side": side,
            "orderType": order_type,
            "qty": str(qty),
            "timeInForce": "GoodTillCancel",
            "positionIdx": position_idx  # ✅ Required for Bybit v5
        }

        if order_type == "Limit":
            if price is None:
                print("❌ ERROR: Limit orders require a price.")
                return {"error": "Limit orders require a price."}
            order_params["price"] = str(price)

        if stop_loss:
            order_params["stopLoss"] = str(stop_loss)
            order_params["slTriggerBy"] = "LastPrice"

        if take_profit:
            order_params["takeProfit"] = str(take_profit)
            order_params["tpTriggerBy"] = "LastPrice"

        # Debug printing
        print("\n🛒 Attempting to place order with the following details:")
        for k, v in order_params.items():
            print(f"   {k}: {v}")

        response = session.place_order(**order_params)

        print("\n📩 Full API Response from Bybit:")
        print(response)

        if response.get("retCode") == 0:
            print(f"✅ Order Successful: {side} {qty} {symbol} at {price if price else 'Market Price'}")
        else:
            print(f"❌ Order Failed: {response.get('retMsg')} (Error Code: {response.get('retCode')})")

        return response

    except Exception as e:
        print(f"\n⚠️ Exception occurred while placing order: {e}")
        return {"error": f"Error placing order: {e}"}
