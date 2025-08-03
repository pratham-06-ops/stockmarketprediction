#!/usr/bin/env python3
"""
Stock Market Prediction System - Quick Start
This script helps you start both backend and frontend components
"""

import os
import sys
import time
import subprocess
import platform
from threading import Thread

def print_banner():
    """Print application banner"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║              📈 STOCK MARKET PREDICTION SYSTEM 📊             ║
    ║                                                              ║
    ║  🎯 Features: LSTM & Linear Regression ML Models            ║
    ║  📊 Interactive Charts & Technical Indicators               ║
    ║  👥 User Management & Admin Dashboard                       ║
    ║  🔐 Secure Authentication System                            ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = [
        'flask', 'pandas', 'numpy', 'scikit-learn', 
        'tensorflow', 'matplotlib', 'requests'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required packages:", ', '.join(missing_packages))
        print("💡 Please install them with: pip install -r requirements.txt")
        return False
    
    print("✅ All required packages are installed!")
    return True

def start_backend():
    """Start the backend server"""
    print("🚀 Starting backend server...")
    try:
        if platform.system() == "Windows":
            subprocess.run([sys.executable, "run_backend.py"], check=True)
        else:
            subprocess.run([sys.executable, "run_backend.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Backend startup failed: {e}")
    except KeyboardInterrupt:
        print("🛑 Backend stopped by user")

def start_frontend():
    """Start the frontend application"""
    print("🎨 Starting frontend application...")
    try:
        subprocess.run([sys.executable, "run_frontend.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Frontend startup failed: {e}")
    except KeyboardInterrupt:
        print("🛑 Frontend stopped by user")

def show_menu():
    """Show startup menu"""
    print("\n🎛️  Choose startup option:")
    print("1. 🚀 Start Backend Only")
    print("2. 🎨 Start Tkinter Frontend Only") 
    print("3. 🔄 Start Both (Backend + Tkinter)")
    print("4. 🌐 Start Dynamic Web Frontend")
    print("5. 📋 View System Information")
    print("6. 🛠️  Install Dependencies")
    print("7. ❌ Exit")
    
    choice = input("\nEnter your choice (1-7): ").strip()
    return choice

def show_system_info():
    """Show system information"""
    print("\n📋 System Information:")
    print(f"🐍 Python Version: {sys.version}")
    print(f"💻 Platform: {platform.system()} {platform.release()}")
    print(f"📁 Current Directory: {os.getcwd()}")
    print(f"🎯 Project Structure:")
    
    # Show project structure
    for root, dirs, files in os.walk('.'):
        level = root.replace('.', '').count(os.sep)
        indent = ' ' * 2 * level
        print(f"{indent}📁 {os.path.basename(root)}/")
        subindent = ' ' * 2 * (level + 1)
        for file in files[:5]:  # Show first 5 files
            print(f"{subindent}📄 {file}")
        if len(files) > 5:
            print(f"{subindent}... and {len(files) - 5} more files")

def install_dependencies():
    """Install project dependencies"""
    print("🛠️  Installing project dependencies...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        print("✅ Dependencies installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        print("💡 Try running manually: pip install -r requirements.txt")

def main():
    """Main function"""
    print_banner()
    
    print("🔍 Checking system requirements...")
    
    # Check if we're in the right directory
    if not os.path.exists('requirements.txt'):
        print("❌ requirements.txt not found!")
        print("💡 Please run this script from the stock_prediction_app directory")
        return
    
    while True:
        choice = show_menu()
        
        if choice == '1':
            if check_dependencies():
                start_backend()
            break
            
        elif choice == '2':
            if check_dependencies():
                start_frontend()
            break
            
        elif choice == '3':
            if check_dependencies():
                print("🔄 Starting both backend and frontend...")
                print("📝 Note: Backend will start first, then frontend")
                print("⏳ Please wait for backend to initialize completely...")
                
                # Start backend in background thread
                backend_thread = Thread(target=start_backend, daemon=True)
                backend_thread.start()
                
                # Wait a bit for backend to start
                print("⏳ Waiting for backend to initialize...")
                time.sleep(3)
                
                # Start frontend
                start_frontend()
            break
            
        elif choice == '4':
            if check_dependencies():
                print("🌐 Starting Dynamic Web Frontend...")
                print("📊 This will start the modern web interface with real-time features")
                print("🔗 Web interface will open at http://localhost:5001")
                subprocess.run([sys.executable, "run_web_frontend.py"], check=True)
            break
            
        elif choice == '5':
            show_system_info()
            
        elif choice == '6':
            install_dependencies()
            
        elif choice == '7':
            print("👋 Goodbye!")
            break
            
        else:
            print("❌ Invalid choice. Please enter 1-7.")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n🛑 Application stopped by user")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)