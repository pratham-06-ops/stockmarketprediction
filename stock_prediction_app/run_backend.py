#!/usr/bin/env python3
"""
Stock Market Prediction Backend Server
Run this script to start the Flask backend server
"""

import os
import sys

# Add backend directory to Python path
backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_dir)

# Change to backend directory
os.chdir(backend_dir)

# Import and run the Flask app
from app import app, init_db

if __name__ == '__main__':
    print("🚀 Starting Stock Market Prediction Backend Server...")
    print("📊 Initializing database...")
    
    # Initialize database
    init_db()
    
    print("✅ Database initialized successfully!")
    print("🌐 Server starting on http://localhost:5000")
    print("🔗 Frontend should connect to this URL")
    print("🛑 Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        # Run the Flask app
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)