# Stock Market Prediction System

A comprehensive stock market prediction application that combines advanced machine learning techniques with user-friendly interfaces to provide accurate stock price predictions for TCS, WIPRO, and INFOSYS.

## 🎯 Features

### 🖥 Frontend (Tkinter)
- **Public Pages**
  - Home: Application overview with market statistics
  - About Us: Information about the project and technology
  - User Login: Authentication for regular users
  - Admin Login: Authentication for administrators
  - User Registration: New user account creation

### 👤 User Dashboard
- **Home**: Welcome screen with quick statistics and actions
- **Predictions**: Interactive prediction interface with real-time charts
- **History**: Personal prediction history with detailed records
- **Change Password**: Secure password update functionality

### 🔧 Admin Dashboard
- **Dashboard**: System statistics and overview
- **User Management**: Complete user database management
- **All Results**: System-wide prediction results
- **Change Password**: Admin password management

### 🧠 Backend (Flask)
- **Machine Learning Models**
  - LSTM (Long Short-Term Memory): Advanced neural network for time series prediction
  - Linear Regression: Baseline model for comparison
  - RMSE (Root Mean Square Error): Model performance evaluation
- **Authentication System**: Secure user and admin authentication
- **Database Management**: SQLite database with user and prediction data
- **RESTful API**: Complete API for frontend-backend communication

### 📊 Data Visualization
- **Line Charts**: Historical prices with prediction overlay
- **Candlestick Charts**: OHLC (Open, High, Low, Close) data visualization
- **Volume Charts**: Trading volume analysis
- **Technical Indicators**:
  - RSI (Relative Strength Index)
  - Moving Averages (5, 10, 20 day)
  - Bollinger Bands
  - Daily Returns Analysis

## 🔧 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Step 1: Clone/Download the Project
```bash
cd stock_prediction_app
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Set Up the Backend
```bash
cd backend
python app.py
```
The backend will start on `http://localhost:5000`

### Step 4: Launch the Frontend
Open a new terminal and run:
```bash
cd frontend
python main.py
```

## 📱 Usage Guide

### For Users

1. **Registration**
   - Click on "Register" tab
   - Fill in username, email, and password
   - Click "Register" to create account

2. **Login**
   - Use "User Login" tab
   - Enter your credentials
   - Access your personal dashboard

3. **Making Predictions**
   - Go to "Predictions" tab in dashboard
   - Select company (TCS, WIPRO, INFOSYS)
   - Choose model (LSTM or Linear Regression)
   - Set prediction days (1-10 days ahead)
   - Click "Predict" and view results with charts

4. **Viewing History**
   - Check "History" tab for all past predictions
   - View prediction accuracy and model performance

### For Administrators

1. **Admin Login**
   - Use "Admin Login" tab
   - Default credentials: `admin` / `admin123`
   - Access admin dashboard

2. **System Management**
   - Monitor user statistics
   - View all user predictions
   - Manage user accounts
   - System performance analytics

## 📊 Sample Data

The application includes sample historical data for:
- **TCS (Tata Consultancy Services)**: 30 days of OHLCV data
- **WIPRO**: 30 days of OHLCV data  
- **INFOSYS**: 30 days of OHLCV data

Data includes:
- Date, Open, High, Low, Close, Volume
- Calculated technical indicators
- Daily returns and volatility metrics

## 🔬 Technical Architecture

### Backend Structure
```
backend/
├── app.py              # Main Flask application
├── ml_models.py        # Machine learning models
└── stock_app.db        # SQLite database (auto-created)
```

### Frontend Structure
```
frontend/
└── main.py             # Tkinter GUI application
```

### Data Structure
```
data/
├── tcs_stock_data.csv
├── wipro_stock_data.csv
└── infosys_stock_data.csv
```

### API Endpoints

#### Authentication
- `POST /api/register` - User registration
- `POST /api/login` - User/Admin login
- `POST /api/logout` - Logout
- `POST /api/change-password` - Change password

#### Stock Data
- `GET /api/companies` - Get supported companies
- `GET /api/stock-data/<company>` - Get historical data

#### Predictions
- `POST /api/predict` - Make prediction
- `GET /api/predictions/history` - Get prediction history

#### Admin
- `GET /api/admin/users` - Get all users
- `GET /api/admin/statistics` - Get system statistics

## 🤖 Machine Learning Models

### LSTM Model
- **Architecture**: 3-layer LSTM with dropout
- **Features**: 60-day lookback window
- **Training**: 80/20 train-test split
- **Epochs**: 20 (optimized for speed)
- **Performance**: Measured by RMSE

### Linear Regression Model
- **Features**: Technical indicators, moving averages, volume
- **Training**: Scikit-learn implementation
- **Performance**: Baseline comparison model

### Model Evaluation
- **RMSE**: Root Mean Square Error for accuracy
- **Visualization**: Prediction vs actual price charts
- **Comparison**: Side-by-side model performance

## 🎨 User Interface

### Design Principles
- **Modern**: Clean, professional interface
- **User-Friendly**: Intuitive navigation and controls
- **Responsive**: Adaptive layouts and real-time updates
- **Informative**: Rich data visualization and feedback

### Color Scheme
- **Primary**: Professional blues and grays
- **Success**: Green for positive changes
- **Warning**: Red for negative changes
- **Info**: Blue for neutral information

## 🔒 Security Features

- **Password Hashing**: Werkzeug secure password hashing
- **Session Management**: Flask session handling
- **Authentication**: Role-based access control
- **Input Validation**: Form data validation and sanitization

## 📈 Performance Optimization

- **Async Predictions**: Threading for non-blocking UI
- **Efficient Data Loading**: Pandas optimization
- **Model Caching**: Reduced training time
- **Database Indexing**: Optimized queries

## 🔧 Configuration

### Backend Configuration
- **Host**: `0.0.0.0` (configurable)
- **Port**: `5000` (configurable)
- **Debug Mode**: Enabled for development
- **Database**: SQLite (easily replaceable)

### Frontend Configuration
- **Backend URL**: `http://localhost:5000`
- **Window Size**: 1200x800 (resizable)
- **Theme**: Professional dark/light theme

## 🚀 Future Enhancements

- **Real-time Data**: Integration with live stock APIs
- **More Companies**: Extended stock universe
- **Advanced Models**: Deep learning improvements
- **Mobile App**: Cross-platform mobile version
- **Cloud Deployment**: Scalable cloud infrastructure
- **Portfolio Management**: Multi-stock portfolio tracking

## 🛠 Troubleshooting

### Common Issues

1. **Backend Connection Error**
   - Ensure backend is running on port 5000
   - Check firewall settings
   - Verify Python dependencies

2. **Prediction Errors**
   - Check TensorFlow installation
   - Verify CSV data files exist
   - Ensure sufficient data for training

3. **Chart Display Issues**
   - Install matplotlib backend dependencies
   - Check display settings
   - Verify tkinter installation

### System Requirements
- **RAM**: Minimum 4GB (8GB recommended)
- **Storage**: 1GB free space
- **Python**: 3.8+ with tkinter support
- **OS**: Windows, macOS, Linux

## 📞 Support

For issues and questions:
1. Check this README for common solutions
2. Verify all dependencies are installed
3. Ensure backend and frontend are properly configured
4. Check console output for error messages

## 📄 License

This project is developed for educational and demonstration purposes. Please ensure compliance with financial data usage regulations in your jurisdiction.

---

**Built with ❤️ using Python, Flask, Tkinter, TensorFlow, and modern ML techniques**