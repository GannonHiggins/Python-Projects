# ========== IMPORTS ==========
import cv2 as cv  # OpenCV library for image processing and face detection
import numpy as np  # NumPy for numerical operations and array handling
import tkinter as tk  # Tkinter for creating the GUI window
from tkinter import filedialog  # File dialog for selecting image files
import os as os  # Operating system interface for file path operations
import matplotlib.pyplot as plt  # Matplotlib for plotting images


# Global variable to store the file path
selected_file_path = None

def file_upload():
    """
    Opens a file dialog to allow the user to select an image file.
    Updates the path label with the selected file path or a message if no file is selected.
    Stores the file path in the global variable.
    """
    global selected_file_path  # Access the global variable
    
    # Open file dialog to select an image file
    file_path = filedialog.askopenfilename(
        title = "Select an Image",  # Dialog window title
        initialdir = os.path.expanduser("~"),  # Start in user's home directory
        filetypes = [("Image Files", "*.jpg *.jpeg *.png *.bmp *.gif"), ("All Files", "*.*")]  # Image file type filters
    )

    # If a file is selected, update the label and store the path
    if file_path:
        path_label.config(text = f"Selected File: {file_path}")
        selected_file_path = file_path  # Store the file path globally
    else:
        # If no file is selected, update label
        path_label.config(text = "No file selected")
        selected_file_path = None  # Clear the path

def Plot_Image(image):
    plt.imshow(image)
    plt.axis("off")
    plt.show()



def process_image():
    """
    Loads and displays the selected image using OpenCV.
    Only processes if a file is selected.
    """
    global selected_file_path  # Access the global variable
    
    # Check if a file is selected
    if selected_file_path:
        # Load the image
        image = cv.imread(selected_file_path)
        image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
        cascade_path = cv.data.haarcascades + 'haarcascade_frontalface_default.xml'
        face_detect = cv.CascadeClassifier(cascade_path)

        faces = face_detect.detectMultiScale(image, 1.3, 5)

        
        for (x, y, w, h) in faces:
            cv.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)        
            # Crop the face
            roi = image[y:y+h, x:x+w]
            roi = cv.medianBlur(roi, 15)
            image[y:y+h, x:x+w] = roi
        
        
        Plot_Image(image)

        # Check if image is loaded
        if image is not None:
            # Display the image
            cv.imshow("Selected Image", image)
            # Wait for a key press
            cv.waitKey(0)
            # Close the window
            cv.destroyAllWindows()
        else:
            # Show error message if image couldn't be loaded
            path_label.config(text = f"Error: Could not load image from {selected_file_path}")
    else:
        # Show if no file is selected
        path_label.config(text = "Please select an image first")

# GUI SETUP
# Create the main Tkinter window
root = tk.Tk()
root.title("Image Viewer")  # Set window title
root.geometry("600x400")  # Set window size (width x height)

# Create a label to display the file path
path_label = tk.Label(root, text = "No file selected")
path_label.pack(pady = 10)  # Add padding and pack into window

# Create a button to trigger file selection
select_button = tk.Button(root, text = "Select Image", command = file_upload)
select_button.pack(pady = 10)  # Add padding and pack into window

# Create a button to process the selected image
process_button = tk.Button(root, text = "Process Image", command = process_image)
process_button.pack(pady = 10)  # Add padding and pack into window

# START GUI LOOP 
# This keeps the window open and handles user interactions
root.mainloop()