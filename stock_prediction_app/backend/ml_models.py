import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
import warnings
warnings.filterwarnings('ignore')

class StockPredictor:
    def __init__(self):
        self.scaler = MinMaxScaler()
        self.lstm_model = None
        self.lr_model = None
        
    def load_data(self, company):
        """Load stock data for the specified company"""
        filename = f'../data/{company.lower()}_stock_data.csv'
        df = pd.read_csv(filename)
        df['Date'] = pd.to_datetime(df['Date'])
        df = df.sort_values('Date')
        return df
    
    def prepare_data(self, df, lookback_period=None):
        """Prepare data for machine learning models"""
        # Use closing prices for prediction
        data = df['Close'].values.reshape(-1, 1)
        
        # Adjust lookback period based on data size
        if lookback_period is None:
            lookback_period = min(10, len(data) // 3)  # Use smaller lookback for small datasets
        
        lookback_period = max(5, min(lookback_period, len(data) - 5))  # Ensure reasonable bounds
        
        # Scale the data
        scaled_data = self.scaler.fit_transform(data)
        
        # Create sequences for LSTM
        X, y = [], []
        for i in range(lookback_period, len(scaled_data)):
            X.append(scaled_data[i-lookback_period:i, 0])
            y.append(scaled_data[i, 0])
        
        X, y = np.array(X), np.array(y)
        
        # Reshape X for LSTM [samples, time steps, features]
        X = np.reshape(X, (X.shape[0], X.shape[1], 1))
        
        return X, y, scaled_data
    
    def create_lstm_model(self, input_shape):
        """Create LSTM model for time series prediction"""
        model = Sequential([
            LSTM(50, return_sequences=True, input_shape=input_shape),
            Dropout(0.2),
            LSTM(50, return_sequences=True),
            Dropout(0.2),
            LSTM(50),
            Dropout(0.2),
            Dense(1)
        ])
        
        model.compile(optimizer='adam', loss='mean_squared_error')
        return model
    
    def train_lstm(self, X, y):
        """Train LSTM model"""
        # Split data for training
        train_size = int(len(X) * 0.8)
        X_train, X_test = X[:train_size], X[train_size:]
        y_train, y_test = y[:train_size], y[train_size:]
        
        # Create and train model
        self.lstm_model = self.create_lstm_model((X.shape[1], 1))
        
        # Train with reduced epochs for faster execution
        self.lstm_model.fit(X_train, y_train, 
                           batch_size=32, 
                           epochs=20, 
                           verbose=0,
                           validation_split=0.1)
        
        # Calculate RMSE
        predictions = self.lstm_model.predict(X_test, verbose=0)
        rmse = np.sqrt(mean_squared_error(y_test, predictions))
        
        return rmse
    
    def train_linear_regression(self, df):
        """Train Linear Regression model"""
        # Create features
        df = df.copy()
        df['Day'] = range(len(df))
        df['MA_5'] = df['Close'].rolling(window=5).mean()
        df['MA_10'] = df['Close'].rolling(window=10).mean()
        df['Volume_MA'] = df['Volume'].rolling(window=5).mean()
        
        # Drop NaN values
        df = df.dropna()
        
        # Features and target
        features = ['Day', 'Open', 'High', 'Low', 'Volume', 'MA_5', 'MA_10', 'Volume_MA']
        X = df[features].values
        y = df['Close'].values
        
        # Split data
        train_size = int(len(X) * 0.8)
        X_train, X_test = X[:train_size], X[train_size:]
        y_train, y_test = y[:train_size], y[train_size:]
        
        # Train model
        self.lr_model = LinearRegression()
        self.lr_model.fit(X_train, y_train)
        
        # Calculate RMSE
        predictions = self.lr_model.predict(X_test)
        rmse = np.sqrt(mean_squared_error(y_test, predictions))
        
        return rmse, df
    
    def predict_lstm(self, scaled_data, days_ahead=5):
        """Make predictions using LSTM model"""
        # Use appropriate number of days based on available data
        lookback_days = min(10, len(scaled_data) // 2)
        lookback_days = max(5, lookback_days)
        
        last_days = scaled_data[-lookback_days:]
        
        predictions = []
        current_sequence = last_days.reshape(1, lookback_days, 1)
        
        for _ in range(days_ahead):
            pred = self.lstm_model.predict(current_sequence, verbose=0)
            predictions.append(pred[0, 0])
            
            # Update sequence for next prediction
            current_sequence = np.append(current_sequence[:, 1:, :], 
                                       pred.reshape(1, 1, 1), axis=1)
        
        # Inverse transform predictions
        predictions = np.array(predictions).reshape(-1, 1)
        predictions = self.scaler.inverse_transform(predictions)
        
        return predictions.flatten()
    
    def predict_linear_regression(self, df, days_ahead=5):
        """Make predictions using Linear Regression model"""
        last_row = df.iloc[-1].copy()
        predictions = []
        
        for i in range(days_ahead):
            # Create features for prediction
            features = [
                last_row['Day'] + i + 1,
                last_row['Close'],  # Use previous close as open
                last_row['Close'] * 1.02,  # Estimate high
                last_row['Close'] * 0.98,  # Estimate low
                last_row['Volume'],  # Use average volume
                last_row['MA_5'],
                last_row['MA_10'],
                last_row['Volume_MA']
            ]
            
            pred = self.lr_model.predict([features])[0]
            predictions.append(pred)
            
            # Update for next prediction
            last_row['Close'] = pred
            last_row['Day'] += 1
        
        return np.array(predictions)
    
    def predict(self, company, model_type='LSTM', days_ahead=5):
        """Main prediction function"""
        try:
            # Load data
            df = self.load_data(company)
            
            if model_type == 'LSTM':
                # Prepare data for LSTM
                X, y, scaled_data = self.prepare_data(df)
                
                # Train model
                rmse = self.train_lstm(X, y)
                
                # Make predictions
                predictions = self.predict_lstm(scaled_data, days_ahead)
                
                # Get current price and calculate change
                current_price = df['Close'].iloc[-1]
                predicted_price = predictions[-1]
                price_change = ((predicted_price - current_price) / current_price) * 100
                
                return {
                    'company': company,
                    'model_used': 'LSTM',
                    'current_price': float(current_price),
                    'predicted_price': float(predicted_price),
                    'price_change_percent': float(price_change),
                    'predictions': predictions.tolist(),
                    'rmse': float(rmse),
                    'days_ahead': days_ahead
                }
                
            elif model_type == 'Linear_Regression':
                # Train Linear Regression model
                rmse, processed_df = self.train_linear_regression(df)
                
                # Make predictions
                predictions = self.predict_linear_regression(processed_df, days_ahead)
                
                # Get current price and calculate change
                current_price = df['Close'].iloc[-1]
                predicted_price = predictions[-1]
                price_change = ((predicted_price - current_price) / current_price) * 100
                
                return {
                    'company': company,
                    'model_used': 'Linear_Regression',
                    'current_price': float(current_price),
                    'predicted_price': float(predicted_price),
                    'price_change_percent': float(price_change),
                    'predictions': predictions.tolist(),
                    'rmse': float(rmse),
                    'days_ahead': days_ahead
                }
                
        except Exception as e:
            raise Exception(f"Prediction failed: {str(e)}")
    
    def get_technical_indicators(self, company):
        """Calculate technical indicators for visualization"""
        df = self.load_data(company)
        
        # Moving averages
        df['MA_5'] = df['Close'].rolling(window=5).mean()
        df['MA_10'] = df['Close'].rolling(window=10).mean()
        df['MA_20'] = df['Close'].rolling(window=20).mean()
        
        # RSI
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))
        
        # Bollinger Bands
        df['BB_Middle'] = df['Close'].rolling(window=20).mean()
        bb_std = df['Close'].rolling(window=20).std()
        df['BB_Upper'] = df['BB_Middle'] + (bb_std * 2)
        df['BB_Lower'] = df['BB_Middle'] - (bb_std * 2)
        
        # Daily returns
        df['Daily_Return'] = df['Close'].pct_change()
        
        return df.fillna(0).to_dict('records')