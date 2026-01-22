import cv2 as cv
import numpy as np
import tkinter as tk
from tkinter import filedialog
import os as os



def file_upload():
    file_path = filedialog.askopenfilename(
        title = "Select an Image",
        initialdir = os.path.expanduser("~"),
        filetypes = [("Text Files", "*.txt"), ("All Files", "*.*")]
    )

    print(file_path)

    
    # if file_path:
    #
    #     print("Selected file:", file_path)
    #
    #     # with open(file_path, "r") as file:
    #     #     content = file.read()
    #     #     print(f"File content length: {len(content)} characters")
    #     
    #     path_label.config(text = f"Selected File: {file_path}")

root = tk.Tk()
root.title("Image Viewer")
root.geometry("400x200")

path_label = tk.Label(root, text = "No file selected")
path_label.pack(pady = 10)

select_button = tk.Button(root, text = "Select Image", command = file_upload)
select_button.pack(pady = 10)

root.mainloop()


# image = cv.imread("apple.jpg")
#
# cv.imshow("Apple", image)
# cv.waitKey(0)
# cv.destroyAllWindows()