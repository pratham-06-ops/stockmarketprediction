from flask import Flask, request, jsonify, session
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from ml_models import StockPredictor

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'
CORS(app)

# Database initialization
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

# Authentication routes
@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    if not username or not email or not password:
        return jsonify({'error': 'Missing required fields'}), 400
    
    conn = sqlite3.connect('stock_app.db')
    cursor = conn.cursor()
    
    # Check if user exists
    cursor.execute('SELECT id FROM users WHERE username = ? OR email = ?', (username, email))
    if cursor.fetchone():
        conn.close()
        return jsonify({'error': 'User already exists'}), 400
    
    # Create user
    password_hash = generate_password_hash(password)
    cursor.execute('''
        INSERT INTO users (username, email, password_hash)
        VALUES (?, ?, ?)
    ''', (username, email, password_hash))
    
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    is_admin = data.get('is_admin', False)
    
    conn = sqlite3.connect('stock_app.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT id, username, password_hash, is_admin FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()
    
    if user and check_password_hash(user[2], password):
        if is_admin and not user[3]:
            return jsonify({'error': 'Access denied: Not an admin'}), 403
        
        session['user_id'] = user[0]
        session['username'] = user[1]
        session['is_admin'] = user[3]
        
        return jsonify({
            'message': 'Login successful',
            'user': {
                'id': user[0],
                'username': user[1],
                'is_admin': user[3]
            }
        }), 200
    
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/api/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'message': 'Logout successful'}), 200

@app.route('/api/change-password', methods=['POST'])
def change_password():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    data = request.get_json()
    current_password = data.get('current_password')
    new_password = data.get('new_password')
    
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
        return jsonify({'message': 'Password changed successfully'}), 200
    
    conn.close()
    return jsonify({'error': 'Invalid current password'}), 400

# Stock data routes
@app.route('/api/companies', methods=['GET'])
def get_companies():
    return jsonify(['TCS', 'WIPRO', 'INFOSYS'])

@app.route('/api/stock-data/<company>', methods=['GET'])
def get_stock_data(company):
    try:
        filename = f'../data/{company.lower()}_stock_data.csv'
        df = pd.read_csv(filename)
        df['Date'] = pd.to_datetime(df['Date'])
        
        # Calculate daily returns and RSI
        df['Daily_Return'] = df['Close'].pct_change()
        df['RSI'] = calculate_rsi(df['Close'])
        
        return jsonify({
            'data': df.to_dict('records'),
            'statistics': {
                'avg_close': float(df['Close'].mean()),
                'avg_volume': float(df['Volume'].mean()),
                'volatility': float(df['Daily_Return'].std()),
                'latest_price': float(df['Close'].iloc[-1])
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def calculate_rsi(prices, window=14):
    delta = prices.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

# Prediction routes
@app.route('/api/predict', methods=['POST'])
def predict_stock():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    data = request.get_json()
    company = data.get('company')
    model_type = data.get('model_type', 'LSTM')
    days_ahead = data.get('days_ahead', 5)
    
    try:
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
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/predictions/history', methods=['GET'])
def get_prediction_history():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    conn = sqlite3.connect('stock_app.db')
    cursor = conn.cursor()
    
    if session.get('is_admin'):
        # Admin can see all predictions
        cursor.execute('''
            SELECT p.*, u.username 
            FROM predictions p 
            JOIN users u ON p.user_id = u.id 
            ORDER BY p.prediction_date DESC
        ''')
        columns = ['id', 'user_id', 'company', 'predicted_price', 'actual_price', 
                  'prediction_date', 'target_date', 'model_used', 'rmse', 'username']
    else:
        # Regular users see only their predictions
        cursor.execute('''
            SELECT * FROM predictions 
            WHERE user_id = ? 
            ORDER BY prediction_date DESC
        ''', (session['user_id'],))
        columns = ['id', 'user_id', 'company', 'predicted_price', 'actual_price', 
                  'prediction_date', 'target_date', 'model_used', 'rmse']
    
    predictions = cursor.fetchall()
    conn.close()
    
    result = []
    for pred in predictions:
        pred_dict = dict(zip(columns, pred))
        result.append(pred_dict)
    
    return jsonify(result)

# Admin routes
@app.route('/api/admin/users', methods=['GET'])
def get_all_users():
    if not session.get('is_admin'):
        return jsonify({'error': 'Admin access required'}), 403
    
    conn = sqlite3.connect('stock_app.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT id, username, email, is_admin, created_at FROM users')
    users = cursor.fetchall()
    conn.close()
    
    result = []
    for user in users:
        result.append({
            'id': user[0],
            'username': user[1],
            'email': user[2],
            'is_admin': user[3],
            'created_at': user[4]
        })
    
    return jsonify(result)

@app.route('/api/admin/statistics', methods=['GET'])
def get_admin_statistics():
    if not session.get('is_admin'):
        return jsonify({'error': 'Admin access required'}), 403
    
    conn = sqlite3.connect('stock_app.db')
    cursor = conn.cursor()
    
    # Get user count
    cursor.execute('SELECT COUNT(*) FROM users WHERE is_admin = FALSE')
    user_count = cursor.fetchone()[0]
    
    # Get prediction count
    cursor.execute('SELECT COUNT(*) FROM predictions')
    prediction_count = cursor.fetchone()[0]
    
    # Get predictions by company
    cursor.execute('SELECT company, COUNT(*) FROM predictions GROUP BY company')
    company_predictions = dict(cursor.fetchall())
    
    conn.close()
    
    return jsonify({
        'total_users': user_count,
        'total_predictions': prediction_count,
        'predictions_by_company': company_predictions
    })

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)