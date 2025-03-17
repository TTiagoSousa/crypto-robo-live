from src.Brokers.Bybit.client import session

def get_instrument_info(symbol="BTCUSDT", category="linear"):
    """
    Retrieves specific fields for a given symbol from Bybit's instrument info.

    Returns:
        dict: {
            "symbol": str,
            "minLeverage": str,
            "maxLeverage": str,
            "minOrderQty": str,
            "maxOrderQty": str
        }
    """

    try:
        response = session.get_instruments_info(category=category, symbol=symbol)

        if response.get("retCode") == 0:
            instrument_list = response.get("result", {}).get("list", [])
            if instrument_list:
                data = instrument_list[0]  # The first (and usually only) instrument record

                return {
                    "symbol": data.get("symbol"),
                    "minLeverage": data.get("leverageFilter", {}).get("minLeverage"),
                    "maxLeverage": data.get("leverageFilter", {}).get("maxLeverage"),
                    "minOrderQty": data.get("lotSizeFilter", {}).get("minOrderQty"),
                    "maxOrderQty": data.get("lotSizeFilter", {}).get("maxOrderQty"),
                }
        # If no instrument data is found, return an empty dict
        return {}

    except Exception as e:
        return {"error": f"Error retrieving instrument info: {e}"}
