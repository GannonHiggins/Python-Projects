import requests as req
import json
import tkinter as tk

crypto_symbol = {
    "bitcoin": "BTC",
    "ethereum": "ETH",
    "ripple": "XRP",
    "bitcoin-cash": "BCH",
    "litecoin": "LTC",
    "ethereum-classic": "ETC",
}

api_url = "https://api.coingecko.com/api/v3/simple/price?ids={crypto_symbol}&vs_currencies=usd"

def get_crypto_price(crypto_symbol):
    url = api_url.format(crypto_symbol=crypto_symbol)
    response = req.get(url)
    data = response.json()
    return data[crypto_symbol]['usd']

def update_price():
    price = get_crypto_price('bitcoin')
    label.config(text=f"Current price of BTC: ${price}")
    root.after(1000, update_price)

root = tk.Tk()
root.title("Crypto Price Tracker")
root.geometry("300x200")
label = tk.Label(root, text="Current price of BTC: $0")
label.pack(pady=20)

update_price()
root.mainloop()