import asyncio
from tcgdexsdk import TCGdex  # SDK for querying the TCGdex Pokémon card database
from tkinter import Tk, Label, Entry, Button, Text, Scrollbar, messagebox


def Window():
    """Build and run the main application window."""
    root = Tk()
    root.title("Pokemon Card Search")
    root.geometry("800x600")

    # Text field where the user types a card name or search query
    search_entry = Entry(root)
    search_entry.pack()

    # Triggers the search when clicked
    search_button = Button(root, text="Search", command=on_search_button_click)
    search_button.pack()

    # Scrollable area for displaying search results
    card_list = Text(root)
    card_list.pack(fill="both", expand=True)

    root.mainloop()


def on_search_button_click():
    """Handle the Search button click; fetch and display matching cards."""
    return 0  # TODO: Implement search logic


if __name__ == "__main__":
    Window()
