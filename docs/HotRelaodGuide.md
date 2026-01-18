# 🚀 FastAPI Hot Reload User Guide
## Access Your Dev Server from Any Device on Your Local Network

---

## 📋 **Prerequisites**
- Python 3.8+ installed
- FastAPI and uvicorn installed (`pip install "fastapi[standard]"`)
- Windows 10/11 (this guide is Windows-specific)

---

## 🗂️ **Step 1: Set Up Project Structure**

Create this folder structure:
```
MyBackend/
├── app/
│   ├── __init__.py
│   └── main.py
├── run_dev.py
└── requirements.txt
```

### **1.1 Create `app/main.py`**
```python
# app/main.py
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI!"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}
```

### **1.2 Create `run_dev.py`** (Improved Version)
```python
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

import socket          # For getting the local network IP address
import subprocess      # For running the uvicorn server as a subprocess
import sys             # For getting the Python executable path
import os              # For file system operations and path handling
import platform        # For detecting the operating system
import signal          # For handling keyboard interrupts (CTRL+C)

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
    print(f"💻 Local: http://127.0.0.1:8000")           # For access from this machine
    print(f"🌐 Network: http://{local_ip}:8000")        # For access from other devices
    print(f"🔄 Hot reload enabled")                     # File changes auto-restart server
    print(f"📍 Project root: {project_root}")           # Show where server is running from
    print(f"🖥️ OS: {platform.system()}\n")            # Display operating system info
    print("✨ Press CTRL+C to stop the server\n")       # Clear instruction for stopping
    
    # Change working directory to project root
    # Why: Ensures uvicorn can find the app module and watch files correctly
    # Without this, imports might fail if script is run from different directory
    os.chdir(project_root)
    
    try:
        # Run the uvicorn server with specific configuration
        subprocess.run([
            sys.executable,                  # Use the same Python interpreter as this script
            "-m", "uvicorn",                 # Run uvicorn as a module
            "app.main:app",                  # Import path: app/main.py file, 'app' variable
            "--reload",                      # Enable hot reload on file changes
            "--host", "0.0.0.0",             # Bind to all network interfaces (not just localhost)
            "--port", "8000",                # Use port 8000 (standard for development)
            "--reload-dir", "app"            # Only watch the app directory for changes
        ])
        # Why --reload-dir "app":
        # - Reduces CPU usage by only watching relevant files
        # - Prevents unnecessary restarts from changes in other directories
        # - Makes hot reload faster and more reliable
        
    except KeyboardInterrupt:
        # Fallback handler in case signal handling doesn't catch the interrupt
        # This provides an extra layer of clean shutdown
        print("\n✨ Server stopped gracefully")
```

---

## 🔥 **Step 2: Configure Windows Firewall**

**Run PowerShell as Administrator:**
1. Search for "PowerShell" in Windows search
2. Right-click → "Run as administrator"
3. Click "Yes" when User Account Control appears

**Create firewall rule:**
```powershell
New-NetFirewallRule -DisplayName "FastAPI Dev" -Direction Inbound -Protocol TCP -LocalPort 8000 -Action Allow -Profile Any
```

✅ **Expected output:** A rule with `Enabled: True` and `Action: Allow`

---

## 🌐 **Step 3: Set Network Profile to Private**

1. Press `Win + I` → **Network & Internet** → **Wi-Fi**
2. Click your active Wi-Fi connection
3. Under **"Network profile type"**:
   - Click **"Properties"**
   - Change **"Network profile"** from **"Public"** to **"Private"**
   - Click **Save**

> ⚠️ **Security Note**: Only do this for trusted home/office networks. Never set public WiFi to "Private".

---

## 🚀 **Step 4: Start Your Development Server**

**From your project root directory:**
```powershell
python run_dev.py
```

✅ **Expected output:**
```
🚀 FastAPI Dev Server
💻 Local: http://127.0.0.1:8000
🌐 Network: http://192.168.68.60:8000
🔄 Hot reload enabled
📍 Project root: C:\Users\kbsim\PycharmProjects\MyBackend
🖥️ OS: Windows

✨ Press CTRL+C to stop the server

INFO:     Will watch for changes in these directories: ['C:\\Users\\kbsim\\PycharmProjects\\MyBackend\\app']
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [XXXX] using WatchFiles
INFO:     Started server process [XXXX]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

---

## 📱 **Step 5: Connect from Other Devices**

### **From your own PC (test first):**
```powershell
curl http://192.168.68.60:8000 -UseBasicParsing
```
✅ Should return: `{"message":"Hello from FastAPI!"}`

### **From other devices on same network:**
Open a browser and go to:
- `http://192.168.68.60:8000` (replace with your actual IP)
- OR `http://<your-pc-name>.local:8000` (find PC name with `hostname` command)

---

## 🔄 **Step 6: Test Hot Reload**

1. **From another device**, open `http://192.168.68.60:8000` in browser
2. **On your PC**, edit `app/main.py`:
   ```python
   # Change the message
   return {"message": "Hello from FastAPI! Hot reload works!"}
   ```
3. **Save the file**
4. **Refresh the browser** on your other device
5. ✅ You should see the updated message immediately

---

## 🏠 **Optional: Make Your IP Address Static**

### **Method A: Windows Settings (Simple)**
1. Press `Win + I` → **Network & Internet** → **Wi-Fi**
2. Click your connection → **Properties**
3. Click **"Edit"** next to **"IP assignment"**
4. Change to **"Manual"** → turn on **"IPv4"**
5. Enter:
   - **IP address**: `192.168.68.60` (your current IP)
   - **Subnet prefix length**: `24`
   - **Gateway**: `192.168.68.1` (your router)
   - **Preferred DNS**: `192.168.68.1`
6. Click **Save**

### **Method B: Router DHCP Reservation (Recommended)**
1. Find your PC's MAC address:
   ```powershell
   getmac
   ```
2. Open router admin page (usually `192.168.68.1` in browser)
3. Log in with admin credentials
4. Find **"DHCP Reservation"** or **"Static IP Assignment"**
5. Reserve your PC's MAC address to always get `192.168.68.60`
6. Save and restart router

---

## 🔧 **Troubleshooting Guide**

| Issue | Solution |
|-------|----------|
| ❌ Other devices can't connect | Check Windows firewall rule exists and network profile is "Private" |
| ❌ Connection times out | Verify router doesn't have "AP Isolation" enabled |
| ❌ `curl` shows security warning | Always use `-UseBasicParsing` flag |
| ❌ IP address changes after restart | Set static IP via router (Method B) |
| ❌ Server not starting | Check for port conflicts (another app using 8000) |
| ❌ Hot reload not working | Ensure `--reload-dir app` points to correct folder |

### **Quick Diagnostic Commands:**
```powershell
# Check if server is listening on all interfaces
netstat -ano | findstr ":8000"

# Test connection from your own PC using network IP
curl http://192.168.68.60:8000 -UseBasicParsing

# Check your current IP
ipconfig | findstr "IPv4"
```

---

## 💡 **Pro Tips**

1. **Use hostname instead of IP**:
   - Other devices can use: `http://<your-pc-name>.local:8000`
   - Find your PC name: `hostname` command

2. **For mobile testing**:
   - Android: Install "Termux" app for curl testing
   - iOS: Use Safari browser for direct access

3. **When done developing**:
   - Leave network profile as "Private" if it's your home/office network
   - The firewall rule only affects port 8000, which is only used during development

4. **For production**:
   - Never use `--host 0.0.0.0` without proper security
   - Use proper hosting (Render, Railway, AWS, etc.)

---

## ✅ **Success Checklist**
- [ ] Project structure created correctly
- [ ] Firewall rule created for port 8000
- [ ] Network profile set to "Private"
- [ ] Server shows both local and network URLs
- [ ] Other devices can access the server
- [ ] Hot reload works when editing code
- [ ] (Optional) IP address is static

---

**🎉 You're all set!** Your FastAPI server now has hot reload and is accessible from any device on your local network - perfect for mobile testing, demoing to colleagues, or testing on multiple browsers simultaneously.

> **Note about CTRL+C**: The improved `run_dev.py` script now handles CTRL+C gracefully with a clean shutdown message. No more scary tracebacks!