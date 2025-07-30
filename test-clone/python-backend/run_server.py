#!/usr/bin/env python3
"""
Simple script to run the conversational voice agent
"""
import subprocess
import sys
import os

def main():
    print("🚀 Starting Conversational Voice Agent...")
    print("📍 Working directory:", os.getcwd())
    
    # Change to the script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # Activate virtual environment and run server
    try:
        print("🔧 Activating virtual environment...")
        subprocess.run([
            "/bin/bash", "-c", 
            "source venv/bin/activate && python3 working_server.py"
        ], check=True)
    except KeyboardInterrupt:
        print("\n⏹️  Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        print("💡 Make sure you're in the python-backend directory")
        sys.exit(1)

if __name__ == "__main__":
    main()