from src.Brokers.Bybit.client import session

def get_positions():
    """
    Fetches open positions for linear (USDT) contracts. If there's at least one
    open position, returns important fields. Otherwise, returns a message that
    no open trades exist.
    
    Returns:
        dict: 
        {
            "status": "success",
            "position": {
                "symbol": str,
                "side": str,
                "size": str,
                "avgPrice": str,
                "leverage": str,
                "positionValue": str,
                "unrealisedPnl": str,
                ...
            }
        }
        or
        {
            "message": "No open trades."
        }
    """
    try:
        response = session.get_positions(category="linear", settleCoin="USDT")
        positions_list = response.get("result", {}).get("list", [])

        if not positions_list:
            # No open positions
            return {"message": "No open trades."}

        # If there's at least one open position, pick the first
        position = positions_list[0]

        # Extract the key fields you need
        important_data = {
            "symbol": position.get("symbol"),
            "side": position.get("side"),
            "size": position.get("size"),
            "avgPrice": position.get("avgPrice"),
            "leverage": position.get("leverage"),
            "positionValue": position.get("positionValue"),
            "unrealisedPnl": position.get("unrealisedPnl")
        }

        return {
            "status": "success",
            "position": important_data
        }

    except Exception as e:
        return {"error": f"Error retrieving open trades: {e}"}
