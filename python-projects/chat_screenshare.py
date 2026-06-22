from tkinter import *
import mss
import numpy as np
import cv2
import socket
import threading

def screen_capture():
    with mss.mss() as sct:
        monitor = sct.monitors[1]
        print("Streaming screen, press f to stop")
        while True:
            img = sct.grab(monitor)
            frame = np.array(img)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
            cv2.imshow("Screen", frame)
            if cv2.waitKey(1) == ord("f"):
                break
        cv2.destroyAllWindows()

def temp_stream():
    print("Streaming screen, press f to stop")


def Window():
    root = Tk()
    root.title("Chat and Screenshare")
    root.geometry("800x600")
    stream_button = Button(root, text="Start Streaming", command=temp_stream)
    stream_button.pack(padx=10, pady=10)
    root.mainloop()






if __name__ == "__main__":
    Window()