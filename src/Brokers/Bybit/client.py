from pybit.unified_trading import HTTP
from dotenv import load_dotenv
import os
load_dotenv()

api_key = os.getenv('BYBIT_API_KEY')
api_secret = os.getenv('BYBIT_SECRET_KEY')
sub_account_id = os.getenv('BYBIT_SUB_ACCOUNT_ID')

session = HTTP(
    testnet=False,  # Defina como True para usar a testnet
    api_key=api_key,
    api_secret=api_secret
)

sub_account_id = sub_account_id