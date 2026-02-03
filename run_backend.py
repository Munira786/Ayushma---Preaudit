"""
Simple backend server runner.
Run this to start the Ayushma backend on port 8000.
"""

from backend.app import app
import uvicorn
import signal
import sys

def signal_handler(sig, frame):
    print("\n\n🛑 Backend server shutting down...")
    sys.exit(0)

if __name__ == "__main__":
    # Handle Ctrl+C gracefully
    signal.signal(signal.SIGINT, signal_handler)
    
    print("🚀 Starting Ayushma Backend Server...")
    print("📡 API running on http://127.0.0.1:8000")
    print("📚 API docs available at http://127.0.0.1:8000/docs")
    print("\nPress Ctrl+C to stop the server.\n")
    
    try:
        uvicorn.run(
            app, 
            host="127.0.0.1", 
            port=8000,
            log_level="info",
            access_log=True
        )
    except KeyboardInterrupt:
        print("\n\n🛑 Backend server shutting down...")
        sys.exit(0)
