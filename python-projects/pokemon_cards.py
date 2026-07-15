# TCGdex SDK: fetches Pokémon TCG card data from the TCGdex API.
from tcgdexsdk import TCGdex, Query
from tcgdexsdk.enums import Quality
from tkinter import Tk, Entry, Button, Text, messagebox, Toplevel, Label, Frame
from PIL import Image, ImageTk
from io import BytesIO

# Shared SDK client; "en" selects English card names and metadata.
sdk = TCGdex("en")

def Window():
    """Build and run the main application window."""
    root = Tk()
    root.title("Pokemon Card Search")
    root.geometry("800x600")

    search_entry = Entry(root)
    search_entry.pack()
    
    # Bind Enter key to trigger search
    search_entry.bind("<Return>", lambda event: on_search_button_click(search_entry, card_list))

    # Lambda captures widgets defined below; card_list exists before the button is clicked.
    search_button = Button(
        root,
        text="Search",
        command=lambda: on_search_button_click(search_entry, card_list),
    )
    search_button.pack()

    # Scrollable read-only area for search results (name and card ID per line).
    # Add spacing between lines to make items easier to select
    card_list = Text(root, spacing1=5, spacing3=5, padx=10, pady=10)
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
    
    # Bind click event to detect which line was clicked and display the corresponding card
    card_list.bind("<Button-1>", lambda event: on_card_click(event, card_list, cards))


def on_card_click(event, card_list, cards):
    """Handle click on a card in the list; determine which card was clicked."""
    # Get the line number where the user clicked (1-indexed)
    clicked_line = card_list.index(f"@{event.x},{event.y}").split(".")[0]
    line_number = int(clicked_line) - 1  # Convert to 0-indexed
    
    # Make sure the click is within the range of available cards
    if 0 <= line_number < len(cards):
        selected_card = cards[line_number]
        display_card(selected_card, card_list)


def display_card(current_card, card_list):
    """Display detailed information about a single card in a pop-up window."""
    # Create a new pop-up window
    popup = Toplevel()
    popup.title(f"Card Details: {current_card.name}")
    popup.geometry("600x700")
    
    # Create a frame with padding for better layout
    main_frame = Frame(popup, padx=20, pady=20)
    main_frame.pack(fill="both", expand=True)
    
    # Display card name
    name_label = Label(main_frame, text=f"Name: {current_card.name}", font=("Arial", 14, "bold"))
    name_label.pack(anchor="w", pady=5)
    
    # Display card ID
    id_label = Label(main_frame, text=f"Card ID: {current_card.id}", font=("Arial", 10))
    id_label.pack(anchor="w", pady=5)
    
    # Display additional card information if available
    if hasattr(current_card, 'set') and current_card.set:
        set_label = Label(main_frame, text=f"Set: {current_card.set.name}", font=("Arial", 10))
        set_label.pack(anchor="w", pady=5)
    
    if hasattr(current_card, 'rarity') and current_card.rarity:
        rarity_label = Label(main_frame, text=f"Rarity: {current_card.rarity}", font=("Arial", 10))
        rarity_label.pack(anchor="w", pady=5)
    
    if hasattr(current_card, 'hp') and current_card.hp:
        hp_label = Label(main_frame, text=f"HP: {current_card.hp}", font=("Arial", 10))
        hp_label.pack(anchor="w", pady=5)
    
    # Download and display the card image
    try:
        if hasattr(current_card, 'get_image'):
            # get_image() returns an HTTPResponse object, so we need to read it
            response = current_card.get_image(Quality.HIGH, 'png')
            
            if response:
                # Read the bytes from the HTTPResponse
                image_bytes = response.read()
                image = Image.open(BytesIO(image_bytes))
            
                # Resize image to fit nicely in the window (maintain aspect ratio)
                max_width = 400
                max_height = 500
                image.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
                
                # Convert to PhotoImage for tkinter
                photo = ImageTk.PhotoImage(image)
                
                # Display the image
                image_label = Label(main_frame, image=photo)
                image_label.image = photo  # Keep a reference to prevent garbage collection
                image_label.pack(pady=10)
            else:
                info_label = Label(main_frame, text="No image available for this card", font=("Arial", 9), fg="gray")
                info_label.pack(pady=5)
        else:
            info_label = Label(main_frame, text="Image loading not supported", font=("Arial", 9), fg="gray")
            info_label.pack(pady=5)
    except Exception as e:
        error_label = Label(main_frame, text=f"Could not load image: {e}", font=("Arial", 9), fg="red")
        error_label.pack(pady=5)
    
    # Close button
    close_button = Button(popup, text="Close", command=popup.destroy)
    close_button.pack(pady=10)


if __name__ == "__main__":
    Window()
