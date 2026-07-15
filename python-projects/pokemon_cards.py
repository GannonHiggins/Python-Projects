"""
Pokemon Card Search Application
Allows users to search for Pokemon trading cards using the TCGdex API
and view detailed information including card images in a GUI.
"""

# TCGdex SDK: fetches Pokémon TCG card data from the TCGdex API
from tcgdexsdk import TCGdex, Query
from tcgdexsdk.enums import Quality

# Tkinter: GUI framework for the application interface
from tkinter import Tk, Entry, Button, Text, messagebox, Toplevel, Label, Frame

# PIL (Pillow): image processing library for displaying card images
from PIL import Image, ImageTk

# BytesIO: handles in-memory binary data for image processing
from io import BytesIO

# Initialize the SDK client with English language setting
sdk = TCGdex("en")

def Window():
    """
    Build and run the main application window.
    Creates the GUI with a search bar, search button, and results display area.
    """
    # Initialize main window
    root = Tk()
    root.title("Pokemon Card Search")
    root.geometry("800x600")

    # Create search input field
    search_entry = Entry(root)
    search_entry.pack()
    
    # Allow Enter key to trigger search for better UX
    search_entry.bind("<Return>", lambda event: on_search_button_click(search_entry, card_list))

    # Create search button (lambda captures card_list widget defined below)
    search_button = Button(
        root,
        text="Search",
        command=lambda: on_search_button_click(search_entry, card_list),
    )
    search_button.pack()

    # Create scrollable text widget for displaying search results
    # spacing1/spacing3 add vertical space between lines for easier clicking
    card_list = Text(root, spacing1=5, spacing3=5, padx=10, pady=10)
    card_list.pack(fill="both", expand=True)

    # Start the GUI event loop
    root.mainloop()


def on_search_button_click(search_entry, card_list):
    """
    Handle search button click or Enter key press.
    Fetches matching cards from the API and displays them in the card list.
    """
    # Get the search query and remove extra whitespace
    query = search_entry.get().strip()
    
    # Validate that user entered something
    if not query:
        messagebox.showwarning("Search", "Please enter a card name.")
        return

    try:
        # Search for cards matching the query (partial name match)
        # listSync blocks execution until API responds
        cards = sdk.card.listSync(Query().contains("name", query))
    except Exception as e:
        # Display error if API call fails
        messagebox.showerror("Error", f"An error occurred: {e}")
        return

    # Clear any previous search results
    card_list.delete("1.0", "end")

    # Handle case where no cards match the search
    if not cards:
        card_list.insert("end", f"No cards found for '{query}'.\n")
        return
    
    # Display each card as "Name — ID" on a new line
    for card in cards:
        card_list.insert("end", f"{card.name} — {card.id}\n")
    
    # Set up click handler to show card details when user clicks a result
    # Each click will determine which line was clicked and display that card
    card_list.bind("<Button-1>", lambda event: on_card_click(event, card_list, cards))


def on_card_click(event, card_list, cards):
    """
    Handle user clicking on a card in the results list.
    Determines which card was clicked and opens its detail pop-up.
    """
    # Convert mouse click coordinates to line number in the text widget
    # Text widget index format is "line.column", we only need the line number
    clicked_line = card_list.index(f"@{event.x},{event.y}").split(".")[0]
    
    # Convert from 1-indexed (tkinter) to 0-indexed (Python list)
    line_number = int(clicked_line) - 1
    
    # Validate the click was on a valid card line
    if 0 <= line_number < len(cards):
        selected_card = cards[line_number]
        display_card(selected_card, card_list)


def display_card(current_card, card_list):
    """
    Display detailed card information in a pop-up window.
    Shows card name, ID, set, rarity, HP, and image.
    """
    # Create new pop-up window (Toplevel creates a window separate from the main window)
    popup = Toplevel()
    popup.title(f"Card Details: {current_card.name}")
    popup.geometry("600x700")
    
    # Create frame container with padding for cleaner layout
    main_frame = Frame(popup, padx=20, pady=20)
    main_frame.pack(fill="both", expand=True)
    
    # Display card name (larger, bold font for emphasis)
    name_label = Label(main_frame, text=f"Name: {current_card.name}", font=("Arial", 14, "bold"))
    name_label.pack(anchor="w", pady=5)
    
    # Display card ID
    id_label = Label(main_frame, text=f"Card ID: {current_card.id}", font=("Arial", 10))
    id_label.pack(anchor="w", pady=5)
    
    # Display optional card attributes (only if they exist on the card object)
    if hasattr(current_card, 'set') and current_card.set:
        set_label = Label(main_frame, text=f"Set: {current_card.set.name}", font=("Arial", 10))
        set_label.pack(anchor="w", pady=5)
    
    if hasattr(current_card, 'rarity') and current_card.rarity:
        rarity_label = Label(main_frame, text=f"Rarity: {current_card.rarity}", font=("Arial", 10))
        rarity_label.pack(anchor="w", pady=5)
    
    if hasattr(current_card, 'hp') and current_card.hp:
        hp_label = Label(main_frame, text=f"HP: {current_card.hp}", font=("Arial", 10))
        hp_label.pack(anchor="w", pady=5)
    
    # Attempt to download and display the card image
    try:
        if hasattr(current_card, 'get_image'):
            # Request high-quality PNG image from the API
            # Returns HTTPResponse object that needs to be read
            response = current_card.get_image(Quality.HIGH, 'png')
            
            if response:
                # Extract image bytes from the HTTP response
                image_bytes = response.read()
                
                # Load image using PIL from the byte stream
                image = Image.open(BytesIO(image_bytes))
            
                # Resize to fit window while maintaining aspect ratio
                # LANCZOS provides high-quality downsampling
                max_width = 400
                max_height = 500
                image.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
                
                # Convert PIL image to tkinter-compatible format
                photo = ImageTk.PhotoImage(image)
                
                # Display image in label widget
                image_label = Label(main_frame, image=photo)
                # Store reference to prevent garbage collection (tkinter requirement)
                image_label.image = photo
                image_label.pack(pady=10)
            else:
                # Handle case where API returns no image data
                info_label = Label(main_frame, text="No image available for this card", font=("Arial", 9), fg="gray")
                info_label.pack(pady=5)
        else:
            # Handle cards that don't support image loading
            info_label = Label(main_frame, text="Image loading not supported", font=("Arial", 9), fg="gray")
            info_label.pack(pady=5)
    except Exception as e:
        # Display error message if image loading fails
        error_label = Label(main_frame, text=f"Could not load image: {e}", font=("Arial", 9), fg="red")
        error_label.pack(pady=5)
    
    # Add close button to dismiss the pop-up
    close_button = Button(popup, text="Close", command=popup.destroy)
    close_button.pack(pady=10)


# Entry point: run the application when script is executed directly
if __name__ == "__main__":
    Window()
