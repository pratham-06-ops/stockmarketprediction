# 🚀 Full Stack Stock Prediction App - Setup & Connection Guide

This guide explains how to run the complete stock prediction application with both the React frontend and Flask backend, and how to verify they're properly connected.

## 📋 Prerequisites

### System Requirements
- **Python 3.7+** (for backend)
- **Node.js 16+** (for frontend)
- **npm or yarn** (package manager)
- **Git** (for version control)

### Check Your System
```bash
# Check Python version
python --version

# Check Node.js version
node --version

# Check npm version
npm --version
```

## 🏗️ Project Structure

```
stock_prediction_app/
├── backend/                    # Flask API backend
│   ├── app.py                 # Main Flask application
│   ├── ml_models.py           # Machine learning models
│   └── stock_app.db           # SQLite database (auto-created)
├── frontend-react/            # React frontend
│   ├── src/                   # Source code
│   │   ├── components/        # Reusable components
│   │   ├── pages/            # Application pages
│   │   └── services/         # API services
│   ├── package.json          # NPM dependencies
│   └── .env                  # Environment variables
├── run_full_stack.py         # Automated startup script
├── requirements.txt          # Python dependencies
└── FULL_STACK_GUIDE.md      # This guide
```

## 🚀 Quick Start (Automated)

### Option 1: One-Command Startup
```bash
# Navigate to the project root
cd stock_prediction_app

# Run the automated startup script
python run_full_stack.py
```

This script will:
- ✅ Check system requirements
- ✅ Install missing dependencies
- ✅ Start the Flask backend (port 5000)
- ✅ Start the React frontend (port 3000)
- ✅ Verify connections
- ✅ Display status and URLs

## 🔧 Manual Setup (Step by Step)

### Step 1: Setup Backend (Flask)

```bash
# Navigate to project root
cd stock_prediction_app

# Install Python dependencies
pip install -r requirements.txt

# Navigate to backend directory
cd backend

# Start the Flask server
python app.py
```

The backend will start on: **http://localhost:5000**

### Step 2: Setup Frontend (React)

```bash
# Open a new terminal
# Navigate to frontend directory
cd stock_prediction_app/frontend-react

# Install npm dependencies (first time only)
npm install

# Start the React development server
npm start
```

The frontend will start on: **http://localhost:3000**

## 🔗 Verifying Frontend-Backend Connection

### 1. Visual Connection Status
- Open **http://localhost:3000** in your browser
- Look for the **connection status indicator** in the top header
- It should show "Connected" with a green WiFi icon

### 2. API Endpoints Testing

#### Test Backend Directly:
```bash
# Test companies endpoint
curl http://localhost:5000/api/companies

# Test specific stock data
curl http://localhost:5000/api/stock-data/AAPL
```

#### Test from Browser Console:
```javascript
// Open browser console on frontend (F12)
// Test API connection
fetch('http://localhost:5000/api/companies')
  .then(response => response.json())
  .then(data => console.log('Backend connected:', data))
  .catch(error => console.error('Connection failed:', error));
```

### 3. Network Tab Monitoring
1. Open **Developer Tools** (F12)
2. Go to **Network** tab
3. Navigate between pages in the React app
4. Look for API calls to `localhost:5000`
5. Check for successful **200** status codes

## 📊 Available Endpoints

### Backend API Endpoints (Flask)
```
GET  /api/companies              # List available companies
GET  /api/stock-data/<company>   # Get stock data for company
POST /api/predict               # Generate predictions
POST /api/register              # User registration
POST /api/login                 # User login
GET  /api/predictions/history   # Prediction history
```

### Frontend Routes (React)
```
/                    # Home page
/dashboard          # Main dashboard
/analysis           # Stock analysis
/portfolio          # Portfolio management
/settings           # User settings
```

## 🐛 Troubleshooting Connection Issues

### Issue 1: Frontend Can't Connect to Backend
**Symptoms:** Connection status shows "Disconnected"

**Solutions:**
```bash
# Check if backend is running
curl http://localhost:5000/api/companies

# If not running, start backend:
cd backend && python app.py

# Check for port conflicts
netstat -an | grep 5000
```

### Issue 2: CORS Errors
**Symptoms:** Console shows CORS policy errors

**Solution:** CORS is already enabled in `backend/app.py`:
```python
from flask_cors import CORS
CORS(app)  # This allows all origins
```

### Issue 3: Port Already in Use
**Symptoms:** "Port 3000/5000 already in use"

**Solutions:**
```bash
# Kill processes on port 3000
npx kill-port 3000

# Kill processes on port 5000
npx kill-port 5000

# Or find and kill manually
lsof -ti:3000 | xargs kill -9
lsof -ti:5000 | xargs kill -9
```

### Issue 4: Missing Dependencies
**Symptoms:** Import errors or module not found

**Solutions:**
```bash
# For Python dependencies
pip install -r requirements.txt

# For Node.js dependencies
cd frontend-react && npm install

# If issues persist, try clean install
rm -rf node_modules package-lock.json
npm install
```

## 📈 Testing Application Features

### 1. Dashboard Functionality
- Navigate to **http://localhost:3000/dashboard**
- Check if charts are loading
- Verify portfolio data displays
- Test responsive design on mobile

### 2. Stock Analysis
- Go to **http://localhost:3000/analysis**
- Try different analysis types (AI Predictions, Technical, Sentiment)
- Search for different stock symbols
- Verify charts render properly

### 3. API Integration
- Check browser console for any errors
- Monitor network requests in DevTools
- Test user registration/login functionality

## 🔧 Development Tips

### Backend Development
```bash
# Run backend in debug mode
cd backend
export FLASK_DEBUG=1
python app.py

# View logs
tail -f app.log  # if logging is enabled
```

### Frontend Development
```bash
# Run frontend with hot reload
cd frontend-react
npm start

# Build for production
npm run build

# Run tests
npm test
```

### Environment Variables
Create `.env` files for configuration:

**Backend (.env):**
```
FLASK_ENV=development
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///stock_app.db
```

**Frontend (.env):**
```
REACT_APP_API_BASE_URL=http://localhost:5000
REACT_APP_ENV=development
```

## 📊 Monitoring and Logs

### Backend Logs
- Flask logs appear in the terminal where you started the backend
- Look for API request logs showing frontend connections

### Frontend Logs
- React logs appear in the browser console (F12)
- Network tab shows API requests and responses

### Connection Health Check
The React app includes an automatic connection health checker that:
- Tests API connectivity every 30 seconds
- Shows connection status in the header
- Automatically retries failed connections

## 🎯 Success Indicators

✅ **Backend Running:** Flask server starts on port 5000  
✅ **Frontend Running:** React app starts on port 3000  
✅ **Connection Active:** Green "Connected" status in header  
✅ **API Calls Working:** Network tab shows successful requests  
✅ **Data Loading:** Charts and tables populate with data  
✅ **Navigation Working:** All pages load without errors  

## 🚨 Emergency Reset

If something goes wrong, here's how to completely reset:

```bash
# Stop all processes
pkill -f "python app.py"
pkill -f "npm start"

# Clean everything
cd stock_prediction_app/frontend-react
rm -rf node_modules package-lock.json
npm install

# Restart backend
cd ../backend
python app.py

# Restart frontend (new terminal)
cd ../frontend-react
npm start
```

## 📞 Getting Help

If you're still having issues:

1. **Check the logs** in both terminal windows
2. **Verify ports** are not blocked by firewall
3. **Test API directly** with curl or Postman
4. **Check browser console** for JavaScript errors
5. **Ensure dependencies** are properly installed

---

🎉 **Congratulations!** If everything is working, you now have a full-stack stock prediction application running with React frontend and Flask backend connected and communicating properly!