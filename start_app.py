#!/usr/bin/env python
"""
Startup script to run both Ayushma Backend and Frontend servers.
Runs backend on port 8000 and frontend on port 8501.
"""

import subprocess
import time
import sys
import os

def start_backend():
    """Start the FastAPI backend server."""
    print("🚀 Starting Ayushma Backend on port 8000...")
    cmd = [
        sys.executable, 
        "-m", 
        "uvicorn", 
        "backend.app:app",
        "--host", "127.0.0.1",
        "--port", "8000",
        "--reload"
    ]
    backend_process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=os.path.dirname(os.path.abspath(__file__))
    )
    return backend_process

def start_frontend():
    """Start the Streamlit frontend server."""
    print("\n⏳ Waiting for backend to initialize (5 seconds)...")
    time.sleep(5)
    print("🎨 Starting Ayushma Frontend on port 8501...")
    cmd = [
        sys.executable,
        "-m",
        "streamlit",
        "run",
        "app.py",
        "--server.port=8501",
        "--server.address=localhost"
    ]
    frontend_process = subprocess.Popen(
        cmd,
        cwd=os.path.dirname(os.path.abspath(__file__))
    )
    return frontend_process

if __name__ == "__main__":
    print("=" * 60)
    print("  Ayushma AI Audit System - Startup Manager")
    print("=" * 60)
    
    try:
        # Start backend
        backend = start_backend()
        
        # Start frontend
        frontend = start_frontend()
        
        print("\n" + "=" * 60)
        print("✅ Both services are running!")
        print("   Backend API: http://127.0.0.1:8000")
        print("   Frontend UI: http://localhost:8501")
        print("=" * 60)
        print("\nPress Ctrl+C to stop all services...\n")
        
        # Keep running until interrupted
        backend.wait()
        frontend.wait()
        
    except KeyboardInterrupt:
        print("\n\n🛑 Shutting down services...")
        try:
            backend.terminate()
            frontend.terminate()
            time.sleep(1)
            backend.kill()
            frontend.kill()
        except:
            pass
        print("✅ All services stopped.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
