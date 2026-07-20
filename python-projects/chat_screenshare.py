"""
Screen sharing application with live video display in tkinter GUI.
Captures the primary monitor and displays it in real-time at 30 FPS.
"""

from tkinter import *
import mss  # Fast screen capture library
import numpy as np
import cv2  # For color conversion and image resizing
from PIL import Image, ImageTk  # Required for displaying images in tkinter

# Global state variables
streaming = False  # Controls whether screen capture is active
sct = None  # MSS screen capture object (initialized when streaming starts)
video_label = None  # Tkinter label widget that displays the video feed
stream_button = None  # Reference to the start/stop button

def start_stream():
    """
    Toggles screen streaming on/off. When starting, initializes the MSS
    screen capture object and begins the frame update loop.
    """
    global streaming, sct
    if not streaming:
        streaming = True
        stream_button.config(text="Stop Streaming", bg="red")
        sct = mss.mss()  # Create screen capture instance
        update_frame()  # Start the capture loop
    else:
        stop_stream()

def stop_stream():
    """
    Stops screen streaming, closes the MSS capture object, and clears
    the video display. Prevents memory leaks by properly closing resources.
    """
    global streaming, sct
    streaming = False
    stream_button.config(text="Start Streaming", bg="SystemButtonFace")
    if sct is not None:
        sct.close()  # Release screen capture resources
        sct = None
    video_label.config(image='')  # Clear displayed image

def update_frame():
    """
    Captures a single frame from the screen, processes it, and displays it in the GUI.
    Called recursively using tkinter's after() method to achieve ~30 FPS streaming.
    Automatically stops streaming if any errors occur during capture.
    """
    global streaming, sct, video_label
    if streaming and sct is not None:
        try:
            # Capture the primary monitor
            monitor = sct.monitors[1]  # Index 0 is all monitors combined, 1 is primary
            img = sct.grab(monitor)
            frame = np.array(img)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2RGB)  # MSS uses BGRA, tkinter needs RGB
            
            # Scale frame to fit within GUI constraints while maintaining aspect ratio
            height, width = frame.shape[:2]
            max_width = 760
            max_height = 500
            scale = min(max_width/width, max_height/height)
            new_width = int(width * scale)
            new_height = int(height * scale)
            frame = cv2.resize(frame, (new_width, new_height))
            
            # Convert numpy array to tkinter-compatible image format
            img_pil = Image.fromarray(frame)
            img_tk = ImageTk.PhotoImage(image=img_pil)
            
            # Update the display (keep reference to prevent garbage collection)
            video_label.config(image=img_tk)
            video_label.image = img_tk
            
            # Schedule next frame (33ms = ~30 FPS)
            video_label.after(33, update_frame)
        except Exception as e:
            print(f"Error: {e}")
            stop_stream()  # Gracefully handle capture errors

def Window():
    """
    Creates and displays the main application window with screen streaming controls.
    Layout: Start/Stop button at top, video display area (760x500) below.
    """
    global video_label, stream_button
    root = Tk()
    root.title("Chat and Screenshare")
    root.geometry("800x600")
    
    # Control panel with start/stop button
    control_frame = Frame(root)
    control_frame.pack(pady=10)
    
    stream_button = Button(control_frame, text="Start Streaming", command=start_stream, font=("Arial", 12))
    stream_button.pack(padx=10, pady=5)
    
    # Fixed-size video display area with black background
    video_frame = Frame(root, bg="black", width=760, height=500)
    video_frame.pack(padx=20, pady=10)
    video_frame.pack_propagate(False)  # Prevent frame from resizing to content
    
    video_label = Label(video_frame, bg="black")
    video_label.pack(expand=True)
    
    def on_closing():
        """Cleanup: stop streaming and release resources before closing"""
        stop_stream()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)  # Handle window close event
    root.mainloop()



if __name__ == "__main__":
    # Application entry point
    Window()