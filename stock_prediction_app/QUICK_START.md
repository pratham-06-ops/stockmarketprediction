# 🚀 Quick Start Guide

## ⚡ Get Started in 3 Steps

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start the Application
```bash
python start_app.py
```
Choose option 3: "Start Both (Recommended)"

### 3. Access the Application
- **Frontend**: GUI application will open automatically
- **Backend**: Runs on http://localhost:5000

## 🎯 First Time Usage

### Default Admin Access
- **Username**: `admin`
- **Password**: `admin123`

### User Registration
1. Click "Register" tab in the GUI
2. Create your account
3. Login and start making predictions!

## 📊 Making Your First Prediction

1. **Login** to the application
2. Go to **"Predictions"** tab
3. Select a company: `TCS`, `WIPRO`, or `INFOSYS`
4. Choose model: `LSTM` or `Linear_Regression`
5. Set prediction days: `1-10`
6. Click **"Predict"** and view the results!

## 🎨 What You'll See

- **Interactive Charts**: Price predictions with historical data
- **Technical Indicators**: RSI, Moving Averages, Volume analysis
- **Model Performance**: RMSE scores and accuracy metrics
- **Prediction History**: Track all your past predictions

## 🔧 Alternative Startup Methods

### Manual Backend Start
```bash
python run_backend.py
```

### Manual Frontend Start  
```bash
python run_frontend.py
```

## 📱 User Interface Overview

### Public Pages
- **Home**: Application overview and market stats
- **About**: Technology and feature information
- **Login**: User/Admin authentication
- **Register**: New user account creation

### User Dashboard  
- **Home**: Personal dashboard with quick stats
- **Predictions**: ML-powered stock predictions
- **History**: Your prediction tracking
- **Settings**: Password management

### Admin Dashboard
- **Overview**: System statistics
- **Users**: User management interface  
- **Results**: All system predictions
- **Settings**: Admin configuration

## 🚨 Troubleshooting

### Backend Issues
- Ensure Python 3.8+ is installed
- Check that port 5000 is available
- Verify all dependencies are installed

### Frontend Issues  
- Ensure tkinter is available (`python -m tkinter`)
- Check backend connection
- Verify matplotlib backend support

### Dependencies Issues
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## 🎯 Key Features to Try

1. **LSTM Predictions**: Advanced neural network predictions
2. **Technical Analysis**: RSI, Bollinger Bands, Moving Averages
3. **Model Comparison**: Compare LSTM vs Linear Regression
4. **Historical Analysis**: View past prediction accuracy
5. **Admin Tools**: System management and user analytics

Ready to predict the market? Start with `python start_app.py`! 🚀