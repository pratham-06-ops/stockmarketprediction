#!/usr/bin/env python3
"""
Stock Market Prediction Dynamic Web Frontend
Run this script to start the Flask web application with dynamic frontend
"""

import os
import sys
import webbrowser
import time
from threading import Timer

# Add backend directory to Python path
backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_dir)

# Change to backend directory
os.chdir(backend_dir)

def open_browser():
    """Open browser after a short delay"""
    webbrowser.open('http://localhost:5001')

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = [
        'flask', 'pandas', 'numpy', 'plotly', 'requests'
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

if __name__ == '__main__':
    print("🌐 Starting Dynamic Web Frontend...")
    print("🎨 Modern, responsive web interface with real-time features")
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    try:
        # Import and run the web app
        from web_app import app, init_db
        
        print("📊 Initializing database...")
        init_db()
        
        print("✅ Database initialized successfully!")
        print("🚀 Starting web server...")
        print("📱 Features: Dynamic charts, real-time updates, responsive design")
        print("🔗 Web interface will be available at: http://localhost:5001")
        print("🛑 Press Ctrl+C to stop the server")
        print("-" * 60)
        
        # Open browser after 2 seconds
        Timer(2.0, open_browser).start()
        
        # Run the Flask app
        app.run(debug=True, host='0.0.0.0', port=5001, use_reloader=False)
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure all dependencies are installed: pip install -r requirements.txt")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n🛑 Web server stopped by user")
    except Exception as e:
        print(f"❌ Error starting web application: {e}")
        sys.exit(1)