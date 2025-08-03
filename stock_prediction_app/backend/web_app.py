from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
import sys
import json
import plotly
import plotly.graph_objs as go
import plotly.express as px
from plotly.utils import PlotlyJSONEncoder

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from ml_models import StockPredictor

app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.secret_key = 'your-dynamic-secret-key-here'
CORS(app)

# Database initialization (reuse from app.py)
def init_db():
    conn = sqlite3.connect('stock_app.db')
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            is_admin BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Predictions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            company TEXT NOT NULL,
            predicted_price REAL NOT NULL,
            actual_price REAL,
            prediction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            target_date DATE NOT NULL,
            model_used TEXT NOT NULL,
            rmse REAL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Create default admin user
    admin_password = generate_password_hash('admin123')
    cursor.execute('''
        INSERT OR IGNORE INTO users (username, email, password_hash, is_admin)
        VALUES (?, ?, ?, ?)
    ''', ('admin', 'admin@stockapp.com', admin_password, True))
    
    conn.commit()
    conn.close()

def login_required(f):
    """Decorator to require login for routes"""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Decorator to require admin access"""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or not session.get('is_admin'):
            flash('Admin access required', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Public Routes
@app.route('/')
def index():
    """Home page with market overview"""
    try:
        # Get market data for overview
        companies = ['TCS', 'WIPRO', 'INFOSYS']
        market_data = []
        
        for company in companies:
            try:
                filename = f'../data/{company.lower()}_stock_data.csv'
                df = pd.read_csv(filename)
                latest_price = float(df['Close'].iloc[-1])
                avg_price = float(df['Close'].mean())
                change = ((latest_price - df['Close'].iloc[-2]) / df['Close'].iloc[-2]) * 100
                
                market_data.append({
                    'company': company,
                    'price': latest_price,
                    'average': avg_price,
                    'change': change,
                    'trend': 'up' if change > 0 else 'down'
                })
            except:
                market_data.append({
                    'company': company,
                    'price': 0,
                    'average': 0,
                    'change': 0,
                    'trend': 'neutral'
                })
        
        return render_template('index.html', market_data=market_data)
    except Exception as e:
        return render_template('index.html', market_data=[], error=str(e))

@app.route('/about')
def about():
    """About page"""
    return render_template('about.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        is_admin = request.form.get('is_admin') == 'true'
        
        if not username or not password:
            flash('Please enter both username and password', 'error')
            return render_template('login.html')
        
        conn = sqlite3.connect('stock_app.db')
        cursor = conn.cursor()
        
        cursor.execute('SELECT id, username, password_hash, is_admin FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        conn.close()
        
        if user and check_password_hash(user[2], password):
            if is_admin and not user[3]:
                flash('Access denied: Not an admin', 'error')
                return render_template('login.html')
            
            session['user_id'] = user[0]
            session['username'] = user[1]
            session['is_admin'] = user[3]
            
            flash('Login successful!', 'success')
            
            if user[3]:  # Admin
                return redirect(url_for('admin_dashboard'))
            else:  # Regular user
                return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Registration page"""
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if not all([username, email, password, confirm_password]):
            flash('Please fill all fields', 'error')
            return render_template('register.html')
        
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return render_template('register.html')
        
        conn = sqlite3.connect('stock_app.db')
        cursor = conn.cursor()
        
        # Check if user exists
        cursor.execute('SELECT id FROM users WHERE username = ? OR email = ?', (username, email))
        if cursor.fetchone():
            conn.close()
            flash('User already exists', 'error')
            return render_template('register.html')
        
        # Create user
        password_hash = generate_password_hash(password)
        cursor.execute('''
            INSERT INTO users (username, email, password_hash)
            VALUES (?, ?, ?)
        ''', (username, email, password_hash))
        
        conn.commit()
        conn.close()
        
        flash('Registration successful! You can now login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    """Logout route"""
    session.clear()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('index'))

# User Dashboard Routes
@app.route('/dashboard')
@login_required
def dashboard():
    """User dashboard"""
    return render_template('dashboard.html', username=session['username'])

@app.route('/predictions')
@login_required
def predictions():
    """Predictions page"""
    return render_template('predictions.html')

@app.route('/api/predict', methods=['POST'])
@login_required
def predict():
    """Make prediction API"""
    try:
        data = request.get_json()
        company = data.get('company')
        model_type = data.get('model_type', 'LSTM')
        days_ahead = data.get('days_ahead', 5)
        
        predictor = StockPredictor()
        result = predictor.predict(company, model_type, days_ahead)
        
        # Save prediction to database
        conn = sqlite3.connect('stock_app.db')
        cursor = conn.cursor()
        
        target_date = datetime.now() + timedelta(days=days_ahead)
        cursor.execute('''
            INSERT INTO predictions (user_id, company, predicted_price, target_date, model_used, rmse)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (session['user_id'], company, result['predicted_price'], target_date.date(), 
              model_type, result.get('rmse')))
        
        conn.commit()
        conn.close()
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/chart-data/<company>')
@login_required
def get_chart_data(company):
    """Get chart data for visualization"""
    try:
        filename = f'../data/{company.lower()}_stock_data.csv'
        df = pd.read_csv(filename)
        df['Date'] = pd.to_datetime(df['Date'])
        
        # Create interactive chart with Plotly
        fig = go.Figure()
        
        # Candlestick chart
        fig.add_trace(go.Candlestick(
            x=df['Date'],
            open=df['Open'],
            high=df['High'],
            low=df['Low'],
            close=df['Close'],
            name='OHLC'
        ))
        
        # Add moving averages
        df['MA_5'] = df['Close'].rolling(window=5).mean()
        df['MA_10'] = df['Close'].rolling(window=10).mean()
        
        fig.add_trace(go.Scatter(
            x=df['Date'],
            y=df['MA_5'],
            mode='lines',
            name='MA 5',
            line=dict(color='orange', width=1)
        ))
        
        fig.add_trace(go.Scatter(
            x=df['Date'],
            y=df['MA_10'],
            mode='lines',
            name='MA 10',
            line=dict(color='blue', width=1)
        ))
        
        fig.update_layout(
            title=f'{company} Stock Price Analysis',
            xaxis_title='Date',
            yaxis_title='Price (₹)',
            template='plotly_white',
            height=500
        )
        
        # Convert to JSON
        graphJSON = json.dumps(fig, cls=PlotlyJSONEncoder)
        return jsonify({'chart': graphJSON})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/history')
@login_required
def history():
    """Prediction history page"""
    conn = sqlite3.connect('stock_app.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT * FROM predictions 
        WHERE user_id = ? 
        ORDER BY prediction_date DESC
        LIMIT 50
    ''', (session['user_id'],))
    
    predictions = cursor.fetchall()
    conn.close()
    
    # Convert to list of dictionaries
    columns = ['id', 'user_id', 'company', 'predicted_price', 'actual_price', 
               'prediction_date', 'target_date', 'model_used', 'rmse']
    
    history_data = []
    for pred in predictions:
        pred_dict = dict(zip(columns, pred))
        pred_dict['prediction_date'] = pred_dict['prediction_date'][:10]  # Format date
        history_data.append(pred_dict)
    
    return render_template('history.html', predictions=history_data)

@app.route('/profile')
@login_required
def profile():
    """User profile page"""
    return render_template('profile.html')

@app.route('/change-password', methods=['POST'])
@login_required
def change_password():
    """Change password route"""
    current_password = request.form.get('current_password')
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')
    
    if not all([current_password, new_password, confirm_password]):
        flash('Please fill all fields', 'error')
        return redirect(url_for('profile'))
    
    if new_password != confirm_password:
        flash('New passwords do not match', 'error')
        return redirect(url_for('profile'))
    
    conn = sqlite3.connect('stock_app.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT password_hash FROM users WHERE id = ?', (session['user_id'],))
    user = cursor.fetchone()
    
    if user and check_password_hash(user[0], current_password):
        new_password_hash = generate_password_hash(new_password)
        cursor.execute('UPDATE users SET password_hash = ? WHERE id = ?', 
                      (new_password_hash, session['user_id']))
        conn.commit()
        conn.close()
        flash('Password changed successfully!', 'success')
    else:
        conn.close()
        flash('Invalid current password', 'error')
    
    return redirect(url_for('profile'))

# Admin Dashboard Routes
@app.route('/admin')
@admin_required
def admin_dashboard():
    """Admin dashboard"""
    conn = sqlite3.connect('stock_app.db')
    cursor = conn.cursor()
    
    # Get statistics
    cursor.execute('SELECT COUNT(*) FROM users WHERE is_admin = FALSE')
    user_count = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM predictions')
    prediction_count = cursor.fetchone()[0]
    
    cursor.execute('SELECT company, COUNT(*) FROM predictions GROUP BY company')
    company_predictions = dict(cursor.fetchall())
    
    conn.close()
    
    stats = {
        'total_users': user_count,
        'total_predictions': prediction_count,
        'predictions_by_company': company_predictions
    }
    
    return render_template('admin/dashboard.html', stats=stats)

@app.route('/admin/users')
@admin_required
def admin_users():
    """Admin users management"""
    conn = sqlite3.connect('stock_app.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT id, username, email, is_admin, created_at FROM users ORDER BY created_at DESC')
    users = cursor.fetchall()
    conn.close()
    
    columns = ['id', 'username', 'email', 'is_admin', 'created_at']
    users_data = [dict(zip(columns, user)) for user in users]
    
    return render_template('admin/users.html', users=users_data)

@app.route('/admin/predictions')
@admin_required
def admin_predictions():
    """Admin predictions view"""
    conn = sqlite3.connect('stock_app.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT p.*, u.username 
        FROM predictions p 
        JOIN users u ON p.user_id = u.id 
        ORDER BY p.prediction_date DESC
        LIMIT 100
    ''')
    predictions = cursor.fetchall()
    conn.close()
    
    columns = ['id', 'user_id', 'company', 'predicted_price', 'actual_price', 
               'prediction_date', 'target_date', 'model_used', 'rmse', 'username']
    
    predictions_data = [dict(zip(columns, pred)) for pred in predictions]
    
    return render_template('admin/predictions.html', predictions=predictions_data)

# API Routes for dynamic content
@app.route('/api/market-overview')
def api_market_overview():
    """API endpoint for market overview data"""
    companies = ['TCS', 'WIPRO', 'INFOSYS']
    data = []
    
    for company in companies:
        try:
            filename = f'../data/{company.lower()}_stock_data.csv'
            df = pd.read_csv(filename)
            
            latest_price = float(df['Close'].iloc[-1])
            prev_price = float(df['Close'].iloc[-2])
            change = ((latest_price - prev_price) / prev_price) * 100
            
            data.append({
                'company': company,
                'price': latest_price,
                'change': round(change, 2),
                'trend': 'up' if change > 0 else 'down'
            })
        except:
            data.append({
                'company': company,
                'price': 0,
                'change': 0,
                'trend': 'neutral'
            })
    
    return jsonify(data)

@app.route('/api/companies')
def api_companies():
    """Get supported companies"""
    return jsonify(['TCS', 'WIPRO', 'INFOSYS'])

if __name__ == '__main__':
    init_db()
    print("🌐 Starting Dynamic Web Frontend...")
    print("📊 Access the web interface at: http://localhost:5001")
    print("🎨 Features: Dynamic charts, real-time updates, responsive design")
    app.run(debug=True, host='0.0.0.0', port=5001)