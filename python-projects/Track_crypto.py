import requests as req
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


def refresh_price():
    refresh_button.config(state=tk.DISABLED)
    selected_crypto = selected_crypto_var.get()
    selected_symbol = crypto_symbol[selected_crypto]
    try:
        price = get_crypto_price(selected_crypto)
        label.config(text=f"Current price of {selected_symbol}: ${price}")
    except (req.exceptions.RequestException, KeyError, TypeError, ValueError):
        label.config(text=f"Unable to fetch {selected_symbol} price right now.")
    finally:
        refresh_button.config(state=tk.NORMAL)

def get_crypto_price(crypto_symbol):
    url = api_url.format(crypto_symbol=crypto_symbol)
    response = req.get(url, timeout=10)
    response.raise_for_status()
    data = response.json()
    return data[crypto_symbol]['usd']

root = tk.Tk()
root.title("Crypto Price Tracker")
root.geometry("360x220")

selected_crypto_var = tk.StringVar(root)
selected_crypto_var.set("bitcoin")

crypto_dropdown = tk.OptionMenu(root, selected_crypto_var, *crypto_symbol.keys())
crypto_dropdown.pack(pady=10)
label = tk.Label(root, text="Current price of BTC: $0")
label.pack(pady=20)

refresh_button = tk.Button(root, text="Refresh Now", command=refresh_price)
refresh_button.pack(pady=10)

root.mainloop()