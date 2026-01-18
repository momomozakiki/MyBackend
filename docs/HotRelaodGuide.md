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

### **1.2 Create `run_dev.py`**
```python
# run_dev.py
import socket
import subprocess
import sys
import os
import platform

def get_local_ip():
    """Get the local IP address that's actually on your network"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0)
        s.connect(('8.8.8.8', 1))  # Google DNS
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

if __name__ == "__main__":
    project_root = os.path.dirname(os.path.abspath(__file__))
    local_ip = get_local_ip()
    
    print(f"\n🔧 FastAPI Dev Server")
    print(f"💻 Local: http://127.0.0.1:8000")
    print(f"🌐 Network: http://{local_ip}:8000")
    print(f"🔄 Hot reload enabled")
    print(f"📍 Project root: {project_root}")
    print(f"🖥️ OS: {platform.system()}\n")
    
    os.chdir(project_root)
    
    subprocess.run([
        sys.executable, "-m", "uvicorn",
        "app.main:app",
        "--reload",
        "--host", "0.0.0.0",
        "--port", "8000",
        "--reload-dir", "app"
    ])
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
🔧 FastAPI Dev Server
💻 Local: http://127.0.0.1:8000
🌐 Network: http://192.168.68.60:8000
🔄 Hot reload enabled
📍 Project root: C:\Users\kbsim\PycharmProjects\MyBackend
🖥️ OS: Windows

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
| ❌ Other devices can't connect | Check Windows firewall rule exists |
| ❌ Connection times out | Verify network profile is "Private" |
| ❌ `curl` shows security warning | Always use `-UseBasicParsing` flag |
| ❌ IP address changes after restart | Set static IP via router (Method B) |
| ❌ Server not starting | Check for port conflicts (another app using 8000) |
| ❌ Hot reload not working | Ensure `--reload-dir app` points to correct folder |

### **Quick Diagnostic Commands:**
```powershell
# Check if server is listening on all interfaces
netstat -ano | findstr ":8000"

# Check firewall rules for port 8000
Get-NetFirewallRule -DisplayName "FastAPI Dev" | Get-NetFirewallAddressFilter

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
   - iOS: Use "Pythonista" or Safari browser

3. **When done developing**:
   - Set network profile back to "Public" on public networks
   - Or disable the firewall rule: `Remove-NetFirewallRule -DisplayName "FastAPI Dev"`

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