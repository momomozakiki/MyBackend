# run_dev.py
"""
FastAPI Development Server with Network Access & Hot Reload

This script provides a development server that:
1. Runs FastAPI with hot reload enabled
2. Binds to 0.0.0.0 to allow access from other devices on the local network
3. Displays both local and network-accessible URLs
4. Handles graceful shutdown on CTRL+C
5. Automatically watches for file changes in the app directory

Usage:
    python run_dev.py

Features:
    ✅ Hot reload - server restarts automatically when code changes
    ✅ Network access - other devices can connect via local IP
    ✅ Graceful shutdown - clean exit on CTRL+C without traceback
    ✅ Auto IP detection - shows correct network IP for device access
    ✅ Focused watching - only monitors the app directory for changes

Security Note:
    This is for development only! Never use --host 0.0.0.0 in production
    without proper firewall rules and security measures.
"""

import socket  # For getting the local network IP address
import subprocess  # For running the uvicorn server as a subprocess
import sys  # For getting the Python executable path
import os  # For file system operations and path handling
import platform  # For detecting the operating system
import signal  # For handling keyboard interrupts (CTRL+C)


def get_local_ip():
    """
    Get the local IP address that's actually on your network.

    Why this is needed:
    - Using 127.0.0.1 (localhost) only works on the same machine
    - For other devices to connect, we need the actual network IP
    - This function finds the IP that can reach the internet (Google DNS)
    - Falls back to localhost if there are network issues

    How it works:
    1. Creates a temporary socket connection to Google DNS (8.8.8.8)
    2. The OS assigns the appropriate local IP for this connection
    3. We extract that IP address
    4. Close the socket immediately (no actual data transfer)

    Returns:
        str: Local network IP address (e.g., '192.168.1.100') or '127.0.0.1' if failed
    """
    try:
        # Create a temporary UDP socket (no actual connection made)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0)  # Don't wait for connection

        # Connect to Google DNS to determine which local IP would be used
        # This doesn't send any data, just determines the routing
        s.connect(('8.8.8.8', 1))

        # Get the local IP address that would be used for this connection
        ip = s.getsockname()[0]
    except Exception:
        # If anything fails (no internet, firewall blocks, etc.), fall back to localhost
        ip = '127.0.0.1'
    finally:
        # Always close the socket to free resources
        s.close()
    return ip


def handle_keyboard_interrupt(signum, frame):
    """
    Handle CTRL+C (SIGINT) signal gracefully.

    Why this is needed:
    - Default behavior shows a long traceback which looks like an error
    - We want a clean, user-friendly shutdown message
    - Ensures proper cleanup of server processes

    How it works:
    - This function is registered as a signal handler for SIGINT
    - When CTRL+C is pressed, this function runs instead of showing traceback
    - Prints a friendly message and exits cleanly

    Parameters:
        signum: Signal number (ignored in this case)
        frame: Current stack frame (ignored in this case)
    """
    print("\n\n✨ Stopping FastAPI server gracefully...")
    sys.exit(0)


if __name__ == "__main__":
    """
    Main execution block - runs when the script is executed directly.
    """

    # Set up signal handler for CTRL+C to provide clean shutdown
    # This replaces the default interrupt handler with our custom one
    signal.signal(signal.SIGINT, handle_keyboard_interrupt)

    # Get the project root directory (where this script is located)
    # Why: Ensures we're in the correct directory for imports and file watching
    project_root = os.path.dirname(os.path.abspath(__file__))

    # Get the local network IP address for device access
    local_ip = get_local_ip()

    # Print startup information with clear, formatted output
    print(f"\n🚀 FastAPI Dev Server")
    print(f"💻 Local: http://127.0.0.1:8000")  # For access from this machine
    print(f"🌐 Network: http://{local_ip}:8000")  # For access from other devices
    print(f"🔄 Hot reload enabled")  # File changes auto-restart server
    print(f"📍 Project root: {project_root}")  # Show where server is running from
    print(f"🖥️ OS: {platform.system()}\n")  # Display operating system info
    print("✨ Press CTRL+C to stop the server\n")  # Clear instruction for stopping

    # Change working directory to project root
    # Why: Ensures uvicorn can find the app module and watch files correctly
    # Without this, imports might fail if script is run from different directory
    os.chdir(project_root)

    try:
        # Run the uvicorn server with specific configuration
        subprocess.run([
            sys.executable,  # Use the same Python interpreter as this script
            "-m", "uvicorn",  # Run uvicorn as a module
            "app.main:app",  # Import path: app/main.py file, 'app' variable
            "--reload",  # Enable hot reload on file changes
            "--host", "0.0.0.0",  # Bind to all network interfaces (not just localhost)
            "--port", "8000",  # Use port 8000 (standard for development)
            "--reload-dir", "app"  # Only watch the app directory for changes
        ])
        # Why --reload-dir "app":
        # - Reduces CPU usage by only watching relevant files
        # - Prevents unnecessary restarts from changes in other directories
        # - Makes hot reload faster and more reliable

    except KeyboardInterrupt:
        # Fallback handler in case signal handling doesn't catch the interrupt
        # This provides an extra layer of clean shutdown
        print("\n✨ Server stopped gracefully")