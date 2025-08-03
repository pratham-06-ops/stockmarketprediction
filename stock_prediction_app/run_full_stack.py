#!/usr/bin/env python3
"""
Full Stack Stock Prediction App Runner
This script starts both the Flask backend and React frontend
"""

import os
import sys
import time
import subprocess
import platform
import signal
import json
from threading import Thread
from pathlib import Path

# Colors for terminal output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_colored(message, color=Colors.OKGREEN):
    """Print colored message"""
    print(f"{color}{message}{Colors.ENDC}")

def print_banner():
    """Print application banner"""
    banner = f"""
{Colors.HEADER}╔══════════════════════════════════════════════════════════════╗
║              📈 STOCK PREDICTION FULL STACK APP 📊           ║
║                                                              ║
║  🔧 Backend: Flask + SQLite + ML Models                     ║
║  🎨 Frontend: React + Tailwind + Charts                     ║
║  🔗 API Integration & Real-time Updates                     ║
║  📊 Interactive Dashboard & Analytics                       ║
╚══════════════════════════════════════════════════════════════╝{Colors.ENDC}
    """
    print(banner)

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 7):
        print_colored("❌ Python 3.7 or higher is required!", Colors.FAIL)
        return False
    print_colored(f"✅ Python {sys.version.split()[0]} detected", Colors.OKGREEN)
    return True

def check_node_version():
    """Check if Node.js is installed"""
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            version = result.stdout.strip()
            print_colored(f"✅ Node.js {version} detected", Colors.OKGREEN)
            return True
    except FileNotFoundError:
        pass
    
    print_colored("❌ Node.js is not installed or not in PATH", Colors.FAIL)
    print_colored("💡 Please install Node.js from https://nodejs.org/", Colors.WARNING)
    return False

def check_backend_dependencies():
    """Check if backend dependencies are installed"""
    required_packages = [
        'flask', 'flask_cors', 'pandas', 'numpy', 'scikit-learn', 
        'tensorflow', 'matplotlib', 'yfinance', 'requests'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print_colored(f"❌ Missing Python packages: {', '.join(missing_packages)}", Colors.FAIL)
        print_colored("💡 Install with: pip install -r requirements.txt", Colors.WARNING)
        return False
    
    print_colored("✅ All Python dependencies are installed!", Colors.OKGREEN)
    return True

def setup_backend():
    """Setup and start the Flask backend"""
    print_colored("\n🔧 Setting up Backend (Flask)...", Colors.OKBLUE)
    
    backend_dir = Path(__file__).parent / "backend"
    
    if not backend_dir.exists():
        print_colored("❌ Backend directory not found!", Colors.FAIL)
        return None
    
    # Change to backend directory
    os.chdir(backend_dir)
    
    # Set environment variables
    env = os.environ.copy()
    env['FLASK_APP'] = 'app.py'
    env['FLASK_ENV'] = 'development'
    env['FLASK_DEBUG'] = '1'
    
    try:
        print_colored("🚀 Starting Flask backend on http://localhost:5000", Colors.OKGREEN)
        process = subprocess.Popen(
            [sys.executable, 'app.py'],
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )
        return process
    except Exception as e:
        print_colored(f"❌ Failed to start backend: {e}", Colors.FAIL)
        return None

def setup_frontend():
    """Setup and start the React frontend"""
    print_colored("\n🎨 Setting up Frontend (React)...", Colors.OKBLUE)
    
    frontend_dir = Path(__file__).parent / "frontend-react"
    
    if not frontend_dir.exists():
        print_colored("❌ Frontend directory not found!", Colors.FAIL)
        return None
    
    # Change to frontend directory
    os.chdir(frontend_dir)
    
    # Check if node_modules exists
    if not (frontend_dir / "node_modules").exists():
        print_colored("📦 Installing npm dependencies...", Colors.WARNING)
        try:
            subprocess.run(['npm', 'install'], check=True)
            print_colored("✅ NPM dependencies installed!", Colors.OKGREEN)
        except subprocess.CalledProcessError:
            print_colored("❌ Failed to install npm dependencies", Colors.FAIL)
            return None
    
    try:
        print_colored("🚀 Starting React frontend on http://localhost:3000", Colors.OKGREEN)
        
        # Set environment variable to suppress browser opening
        env = os.environ.copy()
        env['BROWSER'] = 'none'
        
        process = subprocess.Popen(
            ['npm', 'start'],
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )
        return process
    except Exception as e:
        print_colored(f"❌ Failed to start frontend: {e}", Colors.FAIL)
        return None

def wait_for_backend(timeout=30):
    """Wait for backend to be ready"""
    import requests
    
    print_colored("⏳ Waiting for backend to be ready...", Colors.WARNING)
    
    for i in range(timeout):
        try:
            response = requests.get('http://localhost:5000/api/companies', timeout=2)
            if response.status_code == 200:
                print_colored("✅ Backend is ready!", Colors.OKGREEN)
                return True
        except requests.exceptions.RequestException:
            pass
        
        time.sleep(1)
        print(f"\rWaiting... ({i+1}/{timeout})", end='', flush=True)
    
    print_colored(f"\n❌ Backend failed to start within {timeout} seconds", Colors.FAIL)
    return False

def wait_for_frontend(timeout=60):
    """Wait for frontend to be ready"""
    import requests
    
    print_colored("⏳ Waiting for frontend to be ready...", Colors.WARNING)
    
    for i in range(timeout):
        try:
            response = requests.get('http://localhost:3000', timeout=2)
            if response.status_code == 200:
                print_colored("✅ Frontend is ready!", Colors.OKGREEN)
                return True
        except requests.exceptions.RequestException:
            pass
        
        time.sleep(1)
        print(f"\rWaiting... ({i+1}/{timeout})", end='', flush=True)
    
    print_colored(f"\n❌ Frontend failed to start within {timeout} seconds", Colors.FAIL)
    return False

def print_status():
    """Print application status and URLs"""
    status_info = f"""
{Colors.OKGREEN}🎉 APPLICATION IS RUNNING SUCCESSFULLY! 🎉{Colors.ENDC}

{Colors.BOLD}📱 Frontend (React):{Colors.ENDC}
   🌐 URL: http://localhost:3000
   📊 Dashboard: http://localhost:3000/dashboard
   📈 Analysis: http://localhost:3000/analysis

{Colors.BOLD}🔧 Backend (Flask API):{Colors.ENDC}
   🌐 URL: http://localhost:5000
   📋 Companies: http://localhost:5000/api/companies
   📊 Stock Data: http://localhost:5000/api/stock-data/AAPL

{Colors.BOLD}🔧 How to test the connection:{Colors.ENDC}
   1. Open http://localhost:3000 in your browser
   2. Check the connection status indicator in the header
   3. Try navigating to different pages
   4. Monitor the console for any errors

{Colors.WARNING}💡 Tips:{Colors.ENDC}
   • The React app will automatically connect to the Flask backend
   • Check the connection status in the top header
   • Backend logs will show API requests
   • Press Ctrl+C to stop both servers

{Colors.BOLD}🐛 Troubleshooting:{Colors.ENDC}
   • If frontend can't connect: Check if backend is running on port 5000
   • If port conflicts: Change ports in the configuration files
   • If CORS errors: Make sure CORS is enabled in Flask backend
"""
    print(status_info)

def cleanup_processes(backend_process, frontend_process):
    """Clean up processes on exit"""
    print_colored("\n🛑 Shutting down applications...", Colors.WARNING)
    
    if backend_process:
        backend_process.terminate()
        print_colored("✅ Backend stopped", Colors.OKGREEN)
    
    if frontend_process:
        frontend_process.terminate()
        print_colored("✅ Frontend stopped", Colors.OKGREEN)

def main():
    """Main function to run the full stack application"""
    # Change to the script directory
    os.chdir(Path(__file__).parent)
    
    print_banner()
    
    # Check system requirements
    print_colored("🔍 Checking system requirements...", Colors.OKBLUE)
    
    if not check_python_version():
        return 1
    
    if not check_node_version():
        return 1
    
    if not check_backend_dependencies():
        print_colored("💡 Run: pip install -r requirements.txt", Colors.WARNING)
        return 1
    
    print_colored("\n✅ All system requirements met!", Colors.OKGREEN)
    
    # Start backend
    backend_process = setup_backend()
    if not backend_process:
        return 1
    
    # Wait for backend to be ready
    if not wait_for_backend():
        cleanup_processes(backend_process, None)
        return 1
    
    # Start frontend
    frontend_process = setup_frontend()
    if not frontend_process:
        cleanup_processes(backend_process, None)
        return 1
    
    # Wait for frontend to be ready
    if not wait_for_frontend():
        cleanup_processes(backend_process, frontend_process)
        return 1
    
    # Print status
    print_status()
    
    # Set up signal handlers for graceful shutdown
    def signal_handler(sig, frame):
        cleanup_processes(backend_process, frontend_process)
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Keep the script running
    try:
        while True:
            # Check if processes are still running
            if backend_process.poll() is not None:
                print_colored("❌ Backend process stopped unexpectedly", Colors.FAIL)
                break
            
            if frontend_process.poll() is not None:
                print_colored("❌ Frontend process stopped unexpectedly", Colors.FAIL)
                break
            
            time.sleep(1)
    
    except KeyboardInterrupt:
        pass
    finally:
        cleanup_processes(backend_process, frontend_process)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())