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

auto_refresh_enabled = False
auto_refresh_job = None
REFRESH_INTERVAL = 30000  # 30 seconds in milliseconds


def refresh_price():
    global auto_refresh_job
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
    
    if auto_refresh_enabled:
        auto_refresh_job = root.after(REFRESH_INTERVAL, refresh_price)


def toggle_auto_refresh():
    global auto_refresh_enabled, auto_refresh_job
    auto_refresh_enabled = not auto_refresh_enabled
    
    if auto_refresh_enabled:
        auto_refresh_button.config(text="Auto-Refresh: ON", bg="green")
        refresh_price()
    else:
        auto_refresh_button.config(text="Auto-Refresh: OFF", bg="red")
        if auto_refresh_job is not None:
            root.after_cancel(auto_refresh_job)
            auto_refresh_job = None

def get_crypto_price(crypto_symbol):
    url = api_url.format(crypto_symbol=crypto_symbol)
    response = req.get(url, timeout=10)
    response.raise_for_status()
    data = response.json()
    return data[crypto_symbol]['usd']

root = tk.Tk()
root.title("Crypto Price Tracker")
root.geometry("360x280")

selected_crypto_var = tk.StringVar(root)
selected_crypto_var.set("bitcoin")

crypto_dropdown = tk.OptionMenu(root, selected_crypto_var, *crypto_symbol.keys())
crypto_dropdown.pack(pady=10)
label = tk.Label(root, text="Current price of BTC: $0")
label.pack(pady=20)

refresh_button = tk.Button(root, text="Refresh Now", command=refresh_price)
refresh_button.pack(pady=10)

auto_refresh_button = tk.Button(root, text="Auto-Refresh: OFF", command=toggle_auto_refresh, bg="red")
auto_refresh_button.pack(pady=5)

status_label = tk.Label(root, text="(Auto-refresh every 30 seconds when enabled)", font=("Arial", 8))
status_label.pack(pady=5)

def on_closing():
    global auto_refresh_job
    if auto_refresh_job is not None:
        root.after_cancel(auto_refresh_job)
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()