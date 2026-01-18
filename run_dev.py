# run_dev.py
import socket
import subprocess
import sys
import os


def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip


if __name__ == "__main__":
    # Get the project root directory (where this script is located)
    project_root = os.path.dirname(os.path.abspath(__file__))

    local_ip = get_local_ip()
    print(f"\n🔧 FastAPI Dev Server")
    print(f"💻 Local: http://127.0.0.1:8000")
    print(f"🌐 Network: http://{local_ip}:8000")
    print(f"🔄 Hot reload enabled\n")

    # Change to project root directory to ensure proper imports
    os.chdir(project_root)

    subprocess.run([
        sys.executable, "-m", "uvicorn",
        "app.main:app",  # Changed from "main:app" to "app.main:app"
        "--reload",
        "--host", "0.0.0.0",
        "--port", "8000"
    ])