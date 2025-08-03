#!/usr/bin/env python3
"""
Connection Test Script
Quick script to test if frontend and backend can communicate
"""

import requests
import time
import json
from urllib.parse import urljoin

def test_backend_connection():
    """Test if backend is running and responsive"""
    backend_url = "http://localhost:5000"
    
    print("🔧 Testing Backend Connection...")
    
    try:
        # Test basic connection
        response = requests.get(f"{backend_url}/api/companies", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Backend is running on {backend_url}")
            print(f"   Available companies: {len(data) if isinstance(data, list) else 'N/A'}")
            return True
        else:
            print(f"❌ Backend responded with status code: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"❌ Cannot connect to backend at {backend_url}")
        print("   Make sure backend is running: cd backend && python app.py")
        return False
    except requests.exceptions.Timeout:
        print(f"❌ Backend connection timed out")
        return False
    except Exception as e:
        print(f"❌ Backend test failed: {str(e)}")
        return False

def test_frontend_connection():
    """Test if frontend is running"""
    frontend_url = "http://localhost:3000"
    
    print("\n🎨 Testing Frontend Connection...")
    
    try:
        response = requests.get(frontend_url, timeout=5)
        
        if response.status_code == 200:
            print(f"✅ Frontend is running on {frontend_url}")
            return True
        else:
            print(f"❌ Frontend responded with status code: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"❌ Cannot connect to frontend at {frontend_url}")
        print("   Make sure frontend is running: cd frontend-react && npm start")
        return False
    except requests.exceptions.Timeout:
        print(f"❌ Frontend connection timed out")
        return False
    except Exception as e:
        print(f"❌ Frontend test failed: {str(e)}")
        return False

def test_cors_connection():
    """Test CORS functionality"""
    print("\n🔗 Testing CORS Configuration...")
    
    try:
        # Simulate a preflight request
        headers = {
            'Origin': 'http://localhost:3000',
            'Access-Control-Request-Method': 'GET',
            'Access-Control-Request-Headers': 'Content-Type'
        }
        
        response = requests.options("http://localhost:5000/api/companies", headers=headers, timeout=5)
        
        if response.status_code in [200, 204]:
            print("✅ CORS is properly configured")
            return True
        else:
            print(f"❌ CORS preflight failed with status: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ CORS test failed: {str(e)}")
        return False

def test_api_endpoints():
    """Test specific API endpoints"""
    print("\n📊 Testing API Endpoints...")
    
    endpoints = [
        "/api/companies",
        "/api/stock-data/AAPL"
    ]
    
    base_url = "http://localhost:5000"
    results = []
    
    for endpoint in endpoints:
        try:
            url = f"{base_url}{endpoint}"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                print(f"✅ {endpoint} - OK")
                results.append(True)
            else:
                print(f"❌ {endpoint} - Status: {response.status_code}")
                results.append(False)
                
        except Exception as e:
            print(f"❌ {endpoint} - Error: {str(e)}")
            results.append(False)
    
    return all(results)

def main():
    """Main test function"""
    print("🧪 Stock Prediction App - Connection Test")
    print("=" * 50)
    
    # Test backend
    backend_ok = test_backend_connection()
    
    # Test frontend
    frontend_ok = test_frontend_connection()
    
    # Test CORS if backend is running
    cors_ok = test_cors_connection() if backend_ok else False
    
    # Test API endpoints if backend is running
    api_ok = test_api_endpoints() if backend_ok else False
    
    # Summary
    print("\n" + "=" * 50)
    print("📋 Connection Test Summary:")
    print("=" * 50)
    
    print(f"Backend (Flask):     {'✅ Connected' if backend_ok else '❌ Failed'}")
    print(f"Frontend (React):    {'✅ Connected' if frontend_ok else '❌ Failed'}")
    print(f"CORS Configuration:  {'✅ Working' if cors_ok else '❌ Failed'}")
    print(f"API Endpoints:       {'✅ Working' if api_ok else '❌ Failed'}")
    
    # Overall status
    if backend_ok and frontend_ok and cors_ok and api_ok:
        print(f"\n🎉 ALL TESTS PASSED! Your application is ready to use!")
        print(f"   Frontend: http://localhost:3000")
        print(f"   Backend:  http://localhost:5000")
    else:
        print(f"\n⚠️  Some tests failed. Please check the issues above.")
        print(f"\n💡 Quick fixes:")
        if not backend_ok:
            print(f"   • Start backend: cd backend && python app.py")
        if not frontend_ok:
            print(f"   • Start frontend: cd frontend-react && npm start")
        if not cors_ok:
            print(f"   • Check CORS configuration in backend/app.py")
        if not api_ok:
            print(f"   • Check backend logs for API errors")

if __name__ == "__main__":
    main()