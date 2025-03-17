from src.Brokers.Bybit.client import session

def get_wallet_balance():
    """
    Retrieves the wallet balance, equity, and total equity of the subaccount.

    Returns:
        dict: {
            "walletBalance": float,
            "equity": float,
            "totalEquity": float
        }
    """
    try:
        response = session.get_wallet_balance(accountType="UNIFIED", coin="USDT")

        if response.get("retCode") == 0:
            balances = response["result"].get("list", [])

            if balances:
                for account in balances:
                    for asset in account.get("coin", []):
                        if asset["coin"] == "USDT":  # ✅ Change if needed for other assets
                            return {
                                "walletBalance": float(asset.get("walletBalance", 0)),
                            }

        return {}  # ✅ Return empty dict if no data found

    except Exception as e:
        return {"error": f"Error retrieving wallet balance: {e}"}
