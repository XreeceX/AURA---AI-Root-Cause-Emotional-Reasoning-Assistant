#!/usr/bin/env python3
"""
Cross-platform runner for AURA.
Usage: python run.py
"""
import os
import sys
import subprocess
import platform
import webbrowser
from pathlib import Path

ROOT = Path(__file__).parent
VENV_DIR = ROOT / ".venv"
BACKEND_DIR = ROOT / "backend"
REQUIREMENTS = BACKEND_DIR / "requirements.txt"
FRONTEND_HTML = ROOT / "frontend" / "index.html"

def is_windows():
    return platform.system() == "Windows"

def get_python():
    if is_windows():
        return sys.executable
    return "python3"

def get_venv_python():
    if is_windows():
        return VENV_DIR / "Scripts" / "python.exe"
    return VENV_DIR / "bin" / "python"

def get_venv_pip():
    if is_windows():
        return VENV_DIR / "Scripts" / "pip.exe"
    return VENV_DIR / "bin" / "pip"

def get_venv_uvicorn():
    if is_windows():
        return VENV_DIR / "Scripts" / "uvicorn.exe"
    return VENV_DIR / "bin" / "uvicorn"

def check_python():
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 10):
        print("❌ Python 3.10+ required. Found:", sys.version)
        sys.exit(1)
    print(f"✅ Python {version.major}.{version.minor}.{version.micro}")

def setup_venv():
    if VENV_DIR.exists():
        print("✅ Virtual environment exists")
        return
    
    print("📦 Creating virtual environment...")
    subprocess.run([get_python(), "-m", "venv", str(VENV_DIR)], check=True)
    print("✅ Virtual environment created")

def install_deps():
    pip = get_venv_pip()
    if not pip.exists():
        print("❌ pip not found in venv")
        sys.exit(1)
    
    print("📦 Installing dependencies (this may take a few minutes)...")
    subprocess.run([str(pip), "install", "-q", "-r", str(REQUIREMENTS)], check=True)
    print("✅ Dependencies installed")

def open_browser():
    url = f"file://{FRONTEND_HTML.absolute()}"
    print(f"🌐 Opening browser at {url}")
    try:
        webbrowser.open(url)
    except Exception as e:
        print(f"⚠️  Could not open browser automatically: {e}")
        print(f"   Please open: {FRONTEND_HTML.absolute()}")

def run_server():
    uvicorn = get_venv_uvicorn()
    if not uvicorn.exists():
        print("❌ uvicorn not found")
        sys.exit(1)
    
    print("🚀 Starting AURA server on http://localhost:8000")
    print("   Press Ctrl+C to stop")
    print()
    
    os.chdir(BACKEND_DIR)
    try:
        subprocess.run([
            str(uvicorn),
            "app.main:app",
            "--host", "0.0.0.0",
            "--port", "8000",
            "--reload",
            "--reload-dir", "app"
        ], check=True)
    except KeyboardInterrupt:
        print("\n👋 Server stopped")

def main():
    print("=" * 50)
    print("AURA - AI Root-Cause & Emotional Reasoning Assistant")
    print("=" * 50)
    print()
    
    check_python()
    setup_venv()
    install_deps()
    
    print()
    print("=" * 50)
    print("Starting AURA...")
    print("=" * 50)
    print()
    
    # Open browser after a short delay
    import threading
    def delayed_open():
        import time
        time.sleep(2)
        open_browser()
    
    threading.Thread(target=delayed_open, daemon=True).start()
    
    run_server()

if __name__ == "__main__":
    main()

