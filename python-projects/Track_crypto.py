import requests as req
import json

api_url = "https://api.coingecko.com/api/v3/simple/price?ids={crypto_symbol}&vs_currencies=usd"

def get_crypto_price(crypto_symbol):
    url = api_url.format(crypto_symbol=crypto_symbol)