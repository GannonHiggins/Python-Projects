# TCGdex SDK: fetches Pokémon TCG card data from the TCGdex API.
from tcgdexsdk import TCGdex, Query, Language
from tcgdexsdk.enums import Quality
from tkinter import Tk, Entry, Button, Text, messagebox

# Shared SDK client; "en" selects English card names and metadata.
sdk = TCGdex("en")

def Window():
    """Build and run the main application window."""
    root = Tk()
    root.title("Pokemon Card Search")
    root.geometry("800x600")

    search_entry = Entry(root)
    search_entry.pack()

    # Lambda captures widgets defined below; card_list exists before the button is clicked.
    search_button = Button(
        root,
        text="Search",
        command=lambda: on_search_button_click(search_entry, card_list),
    )
    search_button.pack()

    # Scrollable read-only area for search results (name and card ID per line).
    card_list = Text(root)
    card_list.pack(fill="both", expand=True)

    root.mainloop()


def on_search_button_click(search_entry, card_list):
    """Handle the Search button click; fetch and display matching cards."""
    query = search_entry.get().strip()
    if not query:
        messagebox.showwarning("Search", "Please enter a card name.")
        return

    try:
        # listSync blocks until the API responds; contains() does a partial name match.
        cards = sdk.card.listSync(Query().contains("name", query))
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        return

    # Clear previous results before showing the new search.
    card_list.delete("1.0", "end")
    if not cards:
        card_list.insert("end", f"No cards found for '{query}'.\n")
        return

    for card in cards:
        card_list.insert("end", f"{card.name} — {card.id}\n")
        card_list.bind("<Button-1>", lambda event: display_card(card))

def display_card(card):
    """TODO: Display detailed information about a single card."""
    return 0



if __name__ == "__main__":
    Window()
