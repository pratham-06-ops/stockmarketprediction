#!/usr/bin/env python3
"""
Stock Market Prediction Frontend Application
Run this script to start the Tkinter GUI application
"""

import os
import sys
import tkinter as tk
from tkinter import messagebox

# Add frontend directory to Python path
frontend_dir = os.path.join(os.path.dirname(__file__), 'frontend')
sys.path.insert(0, frontend_dir)

def check_backend_connection():
    """Check if backend server is running"""
    import requests
    try:
        response = requests.get("http://localhost:5000/api/companies", timeout=5)
        return response.status_code == 200
    except:
        return False

def show_backend_warning():
    """Show warning if backend is not running"""
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    
    result = messagebox.askyesno(
        "Backend Server Not Running",
        "The backend server doesn't seem to be running on localhost:5000.\n\n"
        "The application may not work properly without the backend.\n\n"
        "Do you want to continue anyway?\n\n"
        "To start the backend, run: python run_backend.py"
    )
    
    root.destroy()
    return result

if __name__ == '__main__':
    print("🎨 Starting Stock Market Prediction Frontend...")
    print("🔗 Checking backend connection...")
    
    # Check backend connection
    if not check_backend_connection():
        print("⚠️  Warning: Backend server not detected on localhost:5000")
        print("💡 Make sure to run 'python run_backend.py' first")
        
        if not show_backend_warning():
            print("🛑 Application startup cancelled by user")
            sys.exit(0)
    else:
        print("✅ Backend connection successful!")
    
    print("🖥️  Launching GUI application...")
    print("🎯 Features: User/Admin dashboards, ML predictions, real-time charts")
    print("-" * 60)
    
    try:
        # Import and run the main application
        from main import StockPredictionApp
        
        app = StockPredictionApp()
        app.run()
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure all dependencies are installed: pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        sys.exit(1)
    
    print("👋 Application closed successfully!")