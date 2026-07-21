"""
Network protocol for sending and receiving video frames.
Wire format: 4-byte big-endian size header followed by JPEG-encoded frame data.
"""

import socket
import cv2
import numpy as np
from config import BUFFER_SIZE, CONNECTION_TIMEOUT, JPEG_QUALITY

def send_frame(sock, frame):
    """Send a frame over the network."""
    try:
        # Compress to JPEG to reduce network bandwidth (raw frames would be too large)
        ret, buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), JPEG_QUALITY])
        if not ret:
            raise Exception("Failed to encode frame")
        buffer = buffer.tobytes()
        # Send size header first so receiver knows how many bytes to expect
        sock.sendall(len(buffer).to_bytes(4, 'big'))
        sock.sendall(buffer)
        return True
    except Exception as e:
        print(f"Error sending frame: {e}")
        return False

def receive_frame(sock):
    """Receive a frame from the network."""
    try:
        # Loop to collect all 4 bytes (recv may return fewer than requested)
        size_data = b''
        while len(size_data) < 4:
            chunk = sock.recv(4 - len(size_data))
            if not chunk:
                return None
            size_data += chunk
        
        frame_size = int.from_bytes(size_data, 'big')
        
        # Loop to collect complete frame (TCP stream may deliver data in chunks)
        buffer = b''
        while len(buffer) < frame_size:
            # Limit recv size to BUFFER_SIZE to avoid memory issues with large frames
            chunk = sock.recv(min(BUFFER_SIZE, frame_size - len(buffer)))
            if not chunk:
                return None
            buffer += chunk
        
        frame = cv2.imdecode(np.frombuffer(buffer, np.uint8), cv2.IMREAD_COLOR)
        return frame
    except Exception as e:
        print(f"Error receiving frame: {e}")
        return None

def create_server_socket(host, port):
    """Create a server socket and accept one client connection."""
    try:
        server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Allow immediate reuse of address (prevents "address already in use" errors on restart)
        server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_sock.settimeout(CONNECTION_TIMEOUT)
        server_sock.bind((host, port))
        server_sock.listen(1)
        print(f"Server listening on {host}:{port}")
        conn, addr = server_sock.accept()
        print(f"Connected by {addr}")
        # Remove timeout for data transfer (we want blocking I/O for frames)
        conn.settimeout(None)
        # Close listening socket but keep connection open for data transfer
        server_sock.close()
        return conn
    except Exception as e:
        print(f"Error creating server socket: {e}")
        return None

def create_client_socket(host, port):
    """Create a client socket and connect to server."""
    try:
        client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_sock.settimeout(CONNECTION_TIMEOUT)
        client_sock.connect((host, port))
        print(f"Connected to {host}:{port}")
        # Remove timeout after connection for blocking I/O during frame transfer
        client_sock.settimeout(None)
        return client_sock
    except Exception as e:
        print(f"Error creating client socket: {e}")
        return None

def close_socket(sock):
    """Safely close a socket with proper shutdown."""
    if sock is None:
        return
    try:
        # Shutdown both send and receive to signal connection termination
        sock.shutdown(socket.SHUT_RDWR)
    except:
        pass
    try:
        sock.close()
    except:
        pass

def is_socket_connected(sock):
    """Check if a socket is still connected."""
    if sock is None:
        return False
    original_timeout = None
    try:
        # Temporarily set short timeout for non-blocking check
        original_timeout = sock.gettimeout()
        sock.settimeout(0.1)
        # Use MSG_PEEK to check connection without consuming data
        data = sock.recv(1, socket.MSG_PEEK | socket.MSG_DONTWAIT)
        # Restore original timeout
        sock.settimeout(original_timeout)
        # Empty bytes means socket closed, any data means connected
        return data != b''
    except BlockingIOError:
        # No data available but socket is alive
        if original_timeout is not None:
            sock.settimeout(original_timeout)
        return True
    except:
        # Any other error means disconnected
        # Restore timeout before returning
        if original_timeout is not None:
            try:
                sock.settimeout(original_timeout)
            except:
                pass
        return False