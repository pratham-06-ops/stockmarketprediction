# 🚀 Stock Prediction Full Stack Application

A complete full-stack stock prediction application with React frontend and Flask backend.

## 🎯 Quick Start Guide

### Option 1: Automated Startup (Recommended)
```bash
# Navigate to project directory
cd stock_prediction_app

# Run the automated setup script
python run_full_stack.py
```

### Option 2: Manual Setup
```bash
# Terminal 1: Start Backend
cd stock_prediction_app/backend
pip install -r ../requirements.txt
python app.py

# Terminal 2: Start Frontend
cd stock_prediction_app/frontend-react
npm install
npm start
```

### Option 3: Test Connection Only
```bash
# Test if frontend and backend can communicate
python test_connection.py
```

## 🔗 How to Check Frontend-Backend Connection

### 1. **Visual Indicator**
- Open http://localhost:3000
- Look for connection status in the top header
- Green "Connected" = ✅ Working
- Red "Disconnected" = ❌ Issues

### 2. **Browser Developer Tools**
```javascript
// Open console (F12) and run:
fetch('http://localhost:5000/api/companies')
  .then(r => r.json())
  .then(d => console.log('✅ Connected:', d))
  .catch(e => console.log('❌ Failed:', e))
```

### 3. **Direct API Testing**
```bash
# Test backend endpoints directly
curl http://localhost:5000/api/companies
curl http://localhost:5000/api/stock-data/AAPL
```

### 4. **Network Monitoring**
- Open DevTools (F12) → Network tab
- Navigate pages in React app
- Look for API calls to localhost:5000
- Check for 200 status codes

## 📊 Application URLs

| Service | URL | Description |
|---------|-----|-------------|
| **Frontend** | http://localhost:3000 | React application |
| **Dashboard** | http://localhost:3000/dashboard | Main dashboard |
| **Analysis** | http://localhost:3000/analysis | Stock analysis tools |
| **Backend API** | http://localhost:5000 | Flask API server |
| **Companies API** | http://localhost:5000/api/companies | Available stocks |

## ✅ Success Indicators

When everything is working correctly, you should see:

- ✅ Flask backend running on port 5000
- ✅ React frontend running on port 3000  
- ✅ Green "Connected" status in header
- ✅ Charts and data loading properly
- ✅ No CORS errors in console
- ✅ API calls showing in Network tab

## 🐛 Common Issues & Solutions

### Issue: Connection Status Shows "Disconnected"
```bash
# Check if backend is running
curl http://localhost:5000/api/companies

# If not running, start it:
cd backend && python app.py
```

### Issue: "Port already in use"
```bash
# Kill processes on occupied ports
npx kill-port 3000
npx kill-port 5000

# Or manually:
lsof -ti:3000 | xargs kill -9
lsof -ti:5000 | xargs kill -9
```

### Issue: CORS Errors
The backend already has CORS enabled, but if you see CORS errors:
```python
# This is already in backend/app.py:
from flask_cors import CORS
CORS(app)
```

### Issue: Missing Dependencies
```bash
# Python dependencies
pip install -r requirements.txt

# Node.js dependencies
cd frontend-react && npm install
```

## 🔧 Project Architecture

```
Frontend (React) ←→ Backend (Flask) ←→ Database (SQLite)
Port 3000            Port 5000          stock_app.db

┌─────────────────┐  HTTP/JSON API  ┌──────────────────┐
│   React App     │ ←────────────→  │   Flask Server   │
│                 │                 │                  │
│ • Dashboard     │                 │ • Stock Data API │
│ • Analysis      │                 │ • ML Predictions │
│ • Portfolio     │                 │ • User Auth      │
│ • Settings      │                 │ • Database ORM   │
└─────────────────┘                 └──────────────────┘
```

## 📁 Key Files for Connection

- **API Service**: `frontend-react/src/services/api.js`
- **Connection Check**: `frontend-react/src/components/ConnectionStatus/`
- **Backend API**: `backend/app.py`
- **Environment**: `frontend-react/.env`

## 📋 Development Workflow

1. **Start Backend**: `cd backend && python app.py`
2. **Start Frontend**: `cd frontend-react && npm start`
3. **Check Connection**: Look for green status in header
4. **Monitor Logs**: Watch both terminal windows
5. **Test Features**: Navigate through all pages

## 🔍 Debugging Tips

- **Backend Logs**: Check terminal where Flask is running
- **Frontend Logs**: Check browser console (F12)
- **Network Requests**: Monitor DevTools Network tab
- **Connection Test**: Run `python test_connection.py`

---

## 🎉 Success!

If you see:
- Backend running on port 5000 ✅
- Frontend running on port 3000 ✅  
- Green connection status ✅
- Data loading in charts ✅

**Congratulations!** Your full-stack stock prediction app is running perfectly! 🚀

---

For detailed troubleshooting, see: `FULL_STACK_GUIDE.md`