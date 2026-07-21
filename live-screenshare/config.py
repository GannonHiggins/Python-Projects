"""
Configuration settings for the live screen sharing application.
"""

# Network settings
HOST = '127.0.0.1'  # localhost for testing, change to your IP for remote connections
PORT = 5555  # Port for communication
BUFFER_SIZE = 65536  # 64KB buffer for receiving data
CONNECTION_TIMEOUT = 10  # Seconds to wait for connection

# Video settings
FPS = 60  # Frames per second (lower = less bandwidth, higher = smoother)
FRAME_DELAY_MS = int(1000 / FPS)  # Milliseconds between frames

# Compression settings
JPEG_QUALITY = 80  # 0-100, higher = better quality but larger size (60-85 recommended)
MAX_DIMENSION = 1920  # Max width/height to prevent huge files

# Display settings (for GUI windows)
DISPLAY_WIDTH = 1920  # Width of video display
DISPLAY_HEIGHT = 1080  # Height of video display

# Server settings
MAX_CLIENTS = 5  # Maximum simultaneous connections


