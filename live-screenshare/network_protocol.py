"""
Network protocol for sending and receiving video frames.
"""

import socket
import cv2
import numpy as np
from config import BUFFER_SIZE, CONNECTION_TIMEOUT, JPEG_QUALITY, HOST, PORT

def send_frame(sock, frame):
    """Send a frame over the network."""
    try:
        # Convert frame to JPEG format
        ret, buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), JPEG_QUALITY])
        if not ret:
            raise Exception("Failed to encode frame")
        buffer = buffer.tobytes()
        # Send frame size first
        sock.sendall(len(buffer).to_bytes(4, 'big'))
        # Send frame data
        sock.sendall(buffer)
        return True
    except Exception as e:
        print(f"Error sending frame: {e}")
        return False

def receive_frame(sock):
    """Receive a frame from the network."""
    try:
        # Receive frame size (4 bytes)
        size_data = b''
        while len(size_data) < 4:
            chunk = sock.recv(4 - len(size_data))
            if not chunk:
                return None
            size_data += chunk
        
        frame_size = int.from_bytes(size_data, 'big')
        
        # Receive frame data
        buffer = b''
        while len(buffer) < frame_size:
            chunk = sock.recv(min(BUFFER_SIZE, frame_size - len(buffer)))
            if not chunk:
                return None
            buffer += chunk
        
        # Decode frame
        frame = cv2.imdecode(np.frombuffer(buffer, np.uint8), cv2.IMREAD_COLOR)
        return frame
    except Exception as e:
        print(f"Error receiving frame: {e}")
        return None

def create_server_socket(host, port):
    """Create a server socket."""
    # Add your server socket creation logic here
    pass

def create_client_socket(host, port):
    """Create a client socket."""
    # Add your client socket creation logic here
    pass
