import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import requests
import json
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import threading

class StockPredictionApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Stock Market Prediction System")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f0f0')
        
        # Backend URL
        self.backend_url = "http://localhost:5000"
        
        # Session variables
        self.current_user = None
        self.is_admin = False
        
        # Style configuration
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Create main container
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Initialize UI
        self.create_public_pages()
        
    def create_public_pages(self):
        """Create public pages (home, about, login)"""
        self.clear_main_frame()
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Home tab
        self.home_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.home_frame, text="Home")
        self.create_home_page()
        
        # About tab
        self.about_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.about_frame, text="About Us")
        self.create_about_page()
        
        # User Login tab
        self.user_login_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.user_login_frame, text="User Login")
        self.create_user_login_page()
        
        # Admin Login tab
        self.admin_login_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.admin_login_frame, text="Admin Login")
        self.create_admin_login_page()
        
        # User Registration tab
        self.register_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.register_frame, text="Register")
        self.create_register_page()
    
    def clear_main_frame(self):
        """Clear all widgets from main frame"""
        for widget in self.main_frame.winfo_children():
            widget.destroy()
    
    def create_home_page(self):
        """Create home page with overview"""
        title = tk.Label(self.home_frame, text="Stock Market Prediction System", 
                        font=("Arial", 24, "bold"), bg='#f0f0f0', fg='#2c3e50')
        title.pack(pady=20)
        
        subtitle = tk.Label(self.home_frame, 
                           text="Advanced ML-powered stock price prediction for TCS, WIPRO, and INFOSYS",
                           font=("Arial", 14), bg='#f0f0f0', fg='#34495e')
        subtitle.pack(pady=10)
        
        # Features frame
        features_frame = ttk.LabelFrame(self.home_frame, text="Features", padding=20)
        features_frame.pack(pady=20, padx=20, fill=tk.X)
        
        features = [
            "🤖 LSTM and Linear Regression Models",
            "📊 Interactive Charts and Visualizations",
            "📈 Technical Indicators (RSI, Moving Averages, Bollinger Bands)",
            "🔍 Historical Data Analysis",
            "👥 User Management System",
            "📱 Admin Dashboard"
        ]
        
        for feature in features:
            feature_label = tk.Label(features_frame, text=feature, font=("Arial", 12),
                                   bg='#f0f0f0', fg='#2c3e50', anchor='w')
            feature_label.pack(anchor='w', pady=5)
        
        # Quick stats frame
        stats_frame = ttk.LabelFrame(self.home_frame, text="Market Overview", padding=20)
        stats_frame.pack(pady=20, padx=20, fill=tk.X)
        
        try:
            # Try to get stock data for quick overview
            self.load_market_overview(stats_frame)
        except:
            overview_label = tk.Label(stats_frame, text="Connect to backend to view market data",
                                    font=("Arial", 12), bg='#f0f0f0', fg='#e74c3c')
            overview_label.pack()
    
    def load_market_overview(self, parent):
        """Load quick market overview"""
        companies = ['TCS', 'WIPRO', 'INFOSYS']
        
        for i, company in enumerate(companies):
            try:
                response = requests.get(f"{self.backend_url}/api/stock-data/{company}")
                if response.status_code == 200:
                    data = response.json()
                    stats = data['statistics']
                    
                    company_frame = ttk.Frame(parent)
                    company_frame.pack(fill=tk.X, pady=5)
                    
                    company_label = tk.Label(company_frame, text=f"{company}:", 
                                           font=("Arial", 12, "bold"), width=10, anchor='w')
                    company_label.pack(side=tk.LEFT)
                    
                    price_label = tk.Label(company_frame, 
                                         text=f"Latest: ₹{stats['latest_price']:.2f} | Avg: ₹{stats['avg_close']:.2f}",
                                         font=("Arial", 11), anchor='w')
                    price_label.pack(side=tk.LEFT, padx=10)
            except:
                pass
    
    def create_about_page(self):
        """Create about page"""
        title = tk.Label(self.about_frame, text="About Our Stock Prediction System", 
                        font=("Arial", 20, "bold"), bg='#f0f0f0', fg='#2c3e50')
        title.pack(pady=20)
        
        about_text = """
        Our Stock Market Prediction System is a comprehensive application that combines
        advanced machine learning techniques with user-friendly interfaces to provide
        accurate stock price predictions.
        
        🎯 Mission:
        To democratize financial market analysis by providing accessible, accurate,
        and reliable stock prediction tools for retail and institutional investors.
        
        🔬 Technology Stack:
        • Backend: Flask (Python) with ML models
        • Frontend: Tkinter for desktop interface
        • Machine Learning: LSTM Neural Networks, Linear Regression
        • Data Processing: Pandas, NumPy, Scikit-learn
        • Visualization: Matplotlib with interactive charts
        
        📊 Supported Companies:
        • Tata Consultancy Services (TCS)
        • Wipro Limited (WIPRO)
        • Infosys Limited (INFOSYS)
        
        🎓 Team:
        Developed by experts in financial technology and machine learning,
        committed to providing cutting-edge solutions for market analysis.
        """
        
        about_label = tk.Label(self.about_frame, text=about_text, 
                              font=("Arial", 11), bg='#f0f0f0', fg='#2c3e50',
                              justify=tk.LEFT, wraplength=800)
        about_label.pack(pady=20, padx=40)
    
    def create_user_login_page(self):
        """Create user login page"""
        login_frame = ttk.LabelFrame(self.user_login_frame, text="User Login", padding=40)
        login_frame.pack(expand=True)
        
        # Username
        ttk.Label(login_frame, text="Username:", font=("Arial", 12)).grid(row=0, column=0, sticky=tk.W, pady=5)
        self.user_username_entry = ttk.Entry(login_frame, font=("Arial", 12), width=25)
        self.user_username_entry.grid(row=0, column=1, pady=5, padx=10)
        
        # Password
        ttk.Label(login_frame, text="Password:", font=("Arial", 12)).grid(row=1, column=0, sticky=tk.W, pady=5)
        self.user_password_entry = ttk.Entry(login_frame, font=("Arial", 12), width=25, show="*")
        self.user_password_entry.grid(row=1, column=1, pady=5, padx=10)
        
        # Login button
        login_btn = ttk.Button(login_frame, text="Login", command=self.user_login)
        login_btn.grid(row=2, column=0, columnspan=2, pady=20)
        
        # Bind Enter key
        self.user_password_entry.bind('<Return>', lambda e: self.user_login())
    
    def create_admin_login_page(self):
        """Create admin login page"""
        login_frame = ttk.LabelFrame(self.admin_login_frame, text="Admin Login", padding=40)
        login_frame.pack(expand=True)
        
        # Username
        ttk.Label(login_frame, text="Username:", font=("Arial", 12)).grid(row=0, column=0, sticky=tk.W, pady=5)
        self.admin_username_entry = ttk.Entry(login_frame, font=("Arial", 12), width=25)
        self.admin_username_entry.grid(row=0, column=1, pady=5, padx=10)
        
        # Password
        ttk.Label(login_frame, text="Password:", font=("Arial", 12)).grid(row=1, column=0, sticky=tk.W, pady=5)
        self.admin_password_entry = ttk.Entry(login_frame, font=("Arial", 12), width=25, show="*")
        self.admin_password_entry.grid(row=1, column=1, pady=5, padx=10)
        
        # Login button
        login_btn = ttk.Button(login_frame, text="Admin Login", command=self.admin_login)
        login_btn.grid(row=2, column=0, columnspan=2, pady=20)
        
        # Default admin credentials hint
        hint_label = tk.Label(login_frame, text="Default: admin / admin123", 
                             font=("Arial", 10), fg='#7f8c8d')
        hint_label.grid(row=3, column=0, columnspan=2, pady=5)
        
        # Bind Enter key
        self.admin_password_entry.bind('<Return>', lambda e: self.admin_login())
    
    def create_register_page(self):
        """Create user registration page"""
        register_frame = ttk.LabelFrame(self.register_frame, text="User Registration", padding=40)
        register_frame.pack(expand=True)
        
        # Username
        ttk.Label(register_frame, text="Username:", font=("Arial", 12)).grid(row=0, column=0, sticky=tk.W, pady=5)
        self.reg_username_entry = ttk.Entry(register_frame, font=("Arial", 12), width=25)
        self.reg_username_entry.grid(row=0, column=1, pady=5, padx=10)
        
        # Email
        ttk.Label(register_frame, text="Email:", font=("Arial", 12)).grid(row=1, column=0, sticky=tk.W, pady=5)
        self.reg_email_entry = ttk.Entry(register_frame, font=("Arial", 12), width=25)
        self.reg_email_entry.grid(row=1, column=1, pady=5, padx=10)
        
        # Password
        ttk.Label(register_frame, text="Password:", font=("Arial", 12)).grid(row=2, column=0, sticky=tk.W, pady=5)
        self.reg_password_entry = ttk.Entry(register_frame, font=("Arial", 12), width=25, show="*")
        self.reg_password_entry.grid(row=2, column=1, pady=5, padx=10)
        
        # Confirm Password
        ttk.Label(register_frame, text="Confirm Password:", font=("Arial", 12)).grid(row=3, column=0, sticky=tk.W, pady=5)
        self.reg_confirm_entry = ttk.Entry(register_frame, font=("Arial", 12), width=25, show="*")
        self.reg_confirm_entry.grid(row=3, column=1, pady=5, padx=10)
        
        # Register button
        register_btn = ttk.Button(register_frame, text="Register", command=self.register_user)
        register_btn.grid(row=4, column=0, columnspan=2, pady=20)
    
    def user_login(self):
        """Handle user login"""
        username = self.user_username_entry.get()
        password = self.user_password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password")
            return
        
        try:
            response = requests.post(f"{self.backend_url}/api/login", 
                                   json={"username": username, "password": password})
            
            if response.status_code == 200:
                data = response.json()
                self.current_user = data['user']
                self.is_admin = data['user']['is_admin']
                messagebox.showinfo("Success", "Login successful!")
                self.create_user_dashboard()
            else:
                error_msg = response.json().get('error', 'Login failed')
                messagebox.showerror("Error", error_msg)
        except requests.exceptions.RequestException:
            messagebox.showerror("Error", "Cannot connect to server. Please ensure backend is running.")
    
    def admin_login(self):
        """Handle admin login"""
        username = self.admin_username_entry.get()
        password = self.admin_password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password")
            return
        
        try:
            response = requests.post(f"{self.backend_url}/api/login", 
                                   json={"username": username, "password": password, "is_admin": True})
            
            if response.status_code == 200:
                data = response.json()
                self.current_user = data['user']
                self.is_admin = True
                messagebox.showinfo("Success", "Admin login successful!")
                self.create_admin_dashboard()
            else:
                error_msg = response.json().get('error', 'Login failed')
                messagebox.showerror("Error", error_msg)
        except requests.exceptions.RequestException:
            messagebox.showerror("Error", "Cannot connect to server. Please ensure backend is running.")
    
    def register_user(self):
        """Handle user registration"""
        username = self.reg_username_entry.get()
        email = self.reg_email_entry.get()
        password = self.reg_password_entry.get()
        confirm = self.reg_confirm_entry.get()
        
        if not all([username, email, password, confirm]):
            messagebox.showerror("Error", "Please fill all fields")
            return
        
        if password != confirm:
            messagebox.showerror("Error", "Passwords do not match")
            return
        
        try:
            response = requests.post(f"{self.backend_url}/api/register", 
                                   json={"username": username, "email": email, "password": password})
            
            if response.status_code == 201:
                messagebox.showinfo("Success", "Registration successful! You can now login.")
                # Clear form
                self.reg_username_entry.delete(0, tk.END)
                self.reg_email_entry.delete(0, tk.END)
                self.reg_password_entry.delete(0, tk.END)
                self.reg_confirm_entry.delete(0, tk.END)
            else:
                error_msg = response.json().get('error', 'Registration failed')
                messagebox.showerror("Error", error_msg)
        except requests.exceptions.RequestException:
            messagebox.showerror("Error", "Cannot connect to server. Please ensure backend is running.")
    
    def create_user_dashboard(self):
        """Create user dashboard"""
        self.clear_main_frame()
        
        # Create notebook for user dashboard
        self.dashboard_notebook = ttk.Notebook(self.main_frame)
        self.dashboard_notebook.pack(fill=tk.BOTH, expand=True)
        
        # Welcome message
        welcome_frame = ttk.Frame(self.main_frame)
        welcome_frame.pack(fill=tk.X, pady=5)
        
        welcome_label = tk.Label(welcome_frame, 
                                text=f"Welcome, {self.current_user['username']}!", 
                                font=("Arial", 16, "bold"), fg='#27ae60')
        welcome_label.pack(side=tk.LEFT)
        
        logout_btn = ttk.Button(welcome_frame, text="Logout", command=self.logout)
        logout_btn.pack(side=tk.RIGHT)
        
        # Dashboard tabs
        self.dash_home_frame = ttk.Frame(self.dashboard_notebook)
        self.dashboard_notebook.add(self.dash_home_frame, text="Home")
        self.create_dash_home()
        
        self.prediction_frame = ttk.Frame(self.dashboard_notebook)
        self.dashboard_notebook.add(self.prediction_frame, text="Predictions")
        self.create_prediction_page()
        
        self.history_frame = ttk.Frame(self.dashboard_notebook)
        self.dashboard_notebook.add(self.history_frame, text="History")
        self.create_history_page()
        
        self.change_pwd_frame = ttk.Frame(self.dashboard_notebook)
        self.dashboard_notebook.add(self.change_pwd_frame, text="Change Password")
        self.create_change_password_page()
    
    def create_dash_home(self):
        """Create dashboard home page"""
        title = tk.Label(self.dash_home_frame, text="Stock Market Dashboard", 
                        font=("Arial", 20, "bold"), fg='#2c3e50')
        title.pack(pady=20)
        
        # Quick stats frame
        stats_frame = ttk.LabelFrame(self.dash_home_frame, text="Quick Statistics", padding=20)
        stats_frame.pack(pady=20, padx=20, fill=tk.X)
        
        try:
            self.load_dashboard_stats(stats_frame)
        except:
            error_label = tk.Label(stats_frame, text="Unable to load statistics", 
                                 font=("Arial", 12), fg='#e74c3c')
            error_label.pack()
        
        # Quick actions frame
        actions_frame = ttk.LabelFrame(self.dash_home_frame, text="Quick Actions", padding=20)
        actions_frame.pack(pady=20, padx=20, fill=tk.X)
        
        actions = [
            ("Make Prediction", self.go_to_predictions),
            ("View History", self.go_to_history),
            ("Change Password", self.go_to_change_password)
        ]
        
        for i, (text, command) in enumerate(actions):
            btn = ttk.Button(actions_frame, text=text, command=command, width=20)
            btn.grid(row=0, column=i, padx=10)
    
    def load_dashboard_stats(self, parent):
        """Load dashboard statistics"""
        companies = ['TCS', 'WIPRO', 'INFOSYS']
        
        for i, company in enumerate(companies):
            try:
                response = requests.get(f"{self.backend_url}/api/stock-data/{company}")
                if response.status_code == 200:
                    data = response.json()
                    stats = data['statistics']
                    
                    company_frame = ttk.Frame(parent)
                    company_frame.pack(fill=tk.X, pady=5)
                    
                    company_label = tk.Label(company_frame, text=f"{company}:", 
                                           font=("Arial", 12, "bold"), width=10, anchor='w')
                    company_label.pack(side=tk.LEFT)
                    
                    details = (f"Current: ₹{stats['latest_price']:.2f} | "
                             f"Avg: ₹{stats['avg_close']:.2f} | "
                             f"Volatility: {stats['volatility']:.4f}")
                    
                    details_label = tk.Label(company_frame, text=details, 
                                           font=("Arial", 11), anchor='w')
                    details_label.pack(side=tk.LEFT, padx=10)
            except:
                pass
    
    def create_prediction_page(self):
        """Create prediction page with charts"""
        # Control frame
        control_frame = ttk.LabelFrame(self.prediction_frame, text="Prediction Controls", padding=10)
        control_frame.pack(fill=tk.X, pady=5, padx=10)
        
        # Company selection
        ttk.Label(control_frame, text="Company:").grid(row=0, column=0, sticky=tk.W, padx=5)
        self.company_var = tk.StringVar(value="TCS")
        company_combo = ttk.Combobox(control_frame, textvariable=self.company_var, 
                                   values=["TCS", "WIPRO", "INFOSYS"], state="readonly")
        company_combo.grid(row=0, column=1, padx=5)
        
        # Model selection
        ttk.Label(control_frame, text="Model:").grid(row=0, column=2, sticky=tk.W, padx=5)
        self.model_var = tk.StringVar(value="LSTM")
        model_combo = ttk.Combobox(control_frame, textvariable=self.model_var, 
                                 values=["LSTM", "Linear_Regression"], state="readonly")
        model_combo.grid(row=0, column=3, padx=5)
        
        # Days ahead
        ttk.Label(control_frame, text="Days Ahead:").grid(row=0, column=4, sticky=tk.W, padx=5)
        self.days_var = tk.StringVar(value="5")
        days_combo = ttk.Combobox(control_frame, textvariable=self.days_var, 
                                values=["1", "3", "5", "7", "10"], state="readonly", width=5)
        days_combo.grid(row=0, column=5, padx=5)
        
        # Predict button
        predict_btn = ttk.Button(control_frame, text="Predict", command=self.make_prediction)
        predict_btn.grid(row=0, column=6, padx=10)
        
        # Results frame
        self.results_frame = ttk.LabelFrame(self.prediction_frame, text="Prediction Results", padding=10)
        self.results_frame.pack(fill=tk.BOTH, expand=True, pady=5, padx=10)
        
        # Chart frame
        self.chart_frame = ttk.Frame(self.results_frame)
        self.chart_frame.pack(fill=tk.BOTH, expand=True)
    
    def make_prediction(self):
        """Make stock prediction"""
        company = self.company_var.get()
        model = self.model_var.get()
        days = int(self.days_var.get())
        
        # Show loading message
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        
        loading_label = tk.Label(self.results_frame, text="Making prediction... Please wait", 
                               font=("Arial", 14), fg='#3498db')
        loading_label.pack(pady=50)
        
        # Make prediction in separate thread
        threading.Thread(target=self._predict_thread, args=(company, model, days)).start()
    
    def _predict_thread(self, company, model, days):
        """Prediction thread"""
        try:
            response = requests.post(f"{self.backend_url}/api/predict", 
                                   json={"company": company, "model_type": model, "days_ahead": days})
            
            if response.status_code == 200:
                result = response.json()
                self.root.after(0, self.display_prediction_result, result)
            else:
                error_msg = response.json().get('error', 'Prediction failed')
                self.root.after(0, self.show_prediction_error, error_msg)
        except requests.exceptions.RequestException:
            self.root.after(0, self.show_prediction_error, "Cannot connect to server")
    
    def display_prediction_result(self, result):
        """Display prediction results with charts"""
        # Clear results frame
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        
        # Results summary
        summary_frame = ttk.Frame(self.results_frame)
        summary_frame.pack(fill=tk.X, pady=10)
        
        # Current price
        current_label = tk.Label(summary_frame, 
                               text=f"Current Price: ₹{result['current_price']:.2f}", 
                               font=("Arial", 12, "bold"))
        current_label.pack(side=tk.LEFT, padx=10)
        
        # Predicted price
        color = '#27ae60' if result['price_change_percent'] > 0 else '#e74c3c'
        predicted_label = tk.Label(summary_frame, 
                                 text=f"Predicted Price: ₹{result['predicted_price']:.2f}", 
                                 font=("Arial", 12, "bold"), fg=color)
        predicted_label.pack(side=tk.LEFT, padx=10)
        
        # Price change
        change_text = f"Change: {result['price_change_percent']:.2f}%"
        change_label = tk.Label(summary_frame, text=change_text, 
                              font=("Arial", 12, "bold"), fg=color)
        change_label.pack(side=tk.LEFT, padx=10)
        
        # RMSE
        rmse_label = tk.Label(summary_frame, 
                            text=f"Model RMSE: {result['rmse']:.4f}", 
                            font=("Arial", 10))
        rmse_label.pack(side=tk.RIGHT, padx=10)
        
        # Create chart
        self.create_prediction_chart(result)
    
    def create_prediction_chart(self, result):
        """Create prediction chart"""
        # Get historical data
        try:
            response = requests.get(f"{self.backend_url}/api/stock-data/{result['company']}")
            if response.status_code == 200:
                data = response.json()['data']
                df = pd.DataFrame(data)
                df['Date'] = pd.to_datetime(df['Date'])
                
                # Create figure
                fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 8))
                fig.suptitle(f"{result['company']} - Stock Analysis & Prediction", fontsize=16)
                
                # Historical prices with prediction
                ax1.plot(df['Date'], df['Close'], label='Historical', color='blue', alpha=0.7)
                
                # Add prediction points
                last_date = df['Date'].iloc[-1]
                pred_dates = [last_date + timedelta(days=i+1) for i in range(len(result['predictions']))]
                ax1.plot(pred_dates, result['predictions'], 'ro-', label='Predicted', markersize=6)
                
                ax1.set_title('Price Prediction')
                ax1.set_ylabel('Price (₹)')
                ax1.legend()
                ax1.grid(True, alpha=0.3)
                
                # Candlestick-style chart (simplified)
                ax2.plot(df['Date'], df['High'], label='High', color='green', alpha=0.6)
                ax2.plot(df['Date'], df['Low'], label='Low', color='red', alpha=0.6)
                ax2.plot(df['Date'], df['Close'], label='Close', color='blue', linewidth=2)
                ax2.set_title('OHLC Data')
                ax2.set_ylabel('Price (₹)')
                ax2.legend()
                ax2.grid(True, alpha=0.3)
                
                # Volume chart
                ax3.bar(df['Date'], df['Volume'], alpha=0.7, color='orange')
                ax3.set_title('Trading Volume')
                ax3.set_ylabel('Volume')
                ax3.grid(True, alpha=0.3)
                
                # RSI if available
                if 'RSI' in df.columns:
                    ax4.plot(df['Date'], df['RSI'], color='purple', linewidth=2)
                    ax4.axhline(y=70, color='r', linestyle='--', alpha=0.7, label='Overbought')
                    ax4.axhline(y=30, color='g', linestyle='--', alpha=0.7, label='Oversold')
                    ax4.set_title('RSI Indicator')
                    ax4.set_ylabel('RSI')
                    ax4.legend()
                else:
                    ax4.plot(df['Date'], df['Close'].pct_change(), color='brown')
                    ax4.set_title('Daily Returns')
                    ax4.set_ylabel('Return %')
                
                ax4.grid(True, alpha=0.3)
                
                plt.tight_layout()
                
                # Add chart to frame
                chart_frame = ttk.Frame(self.results_frame)
                chart_frame.pack(fill=tk.BOTH, expand=True)
                
                canvas = FigureCanvasTkAgg(fig, chart_frame)
                canvas.draw()
                canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
                
        except Exception as e:
            error_label = tk.Label(self.results_frame, text=f"Chart error: {str(e)}", 
                                 font=("Arial", 12), fg='#e74c3c')
            error_label.pack(pady=20)
    
    def show_prediction_error(self, error_msg):
        """Show prediction error"""
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        
        error_label = tk.Label(self.results_frame, text=f"Error: {error_msg}", 
                             font=("Arial", 14), fg='#e74c3c')
        error_label.pack(pady=50)
    
    def create_history_page(self):
        """Create prediction history page"""
        # Refresh button
        refresh_btn = ttk.Button(self.history_frame, text="Refresh", command=self.load_history)
        refresh_btn.pack(anchor=tk.NE, pady=5, padx=10)
        
        # History tree
        columns = ('Date', 'Company', 'Model', 'Predicted', 'Target Date', 'RMSE')
        self.history_tree = ttk.Treeview(self.history_frame, columns=columns, show='headings', height=20)
        
        for col in columns:
            self.history_tree.heading(col, text=col)
            self.history_tree.column(col, width=120)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.history_frame, orient=tk.VERTICAL, command=self.history_tree.yview)
        self.history_tree.configure(yscrollcommand=scrollbar.set)
        
        self.history_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=10)
        
        # Load initial data
        self.load_history()
    
    def load_history(self):
        """Load prediction history"""
        try:
            response = requests.get(f"{self.backend_url}/api/predictions/history")
            if response.status_code == 200:
                predictions = response.json()
                
                # Clear existing data
                for item in self.history_tree.get_children():
                    self.history_tree.delete(item)
                
                # Add new data
                for pred in predictions:
                    values = (
                        pred['prediction_date'][:10],
                        pred['company'],
                        pred['model_used'],
                        f"₹{pred['predicted_price']:.2f}",
                        pred['target_date'],
                        f"{pred['rmse']:.4f}" if pred['rmse'] else 'N/A'
                    )
                    self.history_tree.insert('', tk.END, values=values)
            else:
                messagebox.showerror("Error", "Failed to load history")
        except requests.exceptions.RequestException:
            messagebox.showerror("Error", "Cannot connect to server")
    
    def create_change_password_page(self):
        """Create change password page"""
        pwd_frame = ttk.LabelFrame(self.change_pwd_frame, text="Change Password", padding=40)
        pwd_frame.pack(expand=True)
        
        # Current password
        ttk.Label(pwd_frame, text="Current Password:", font=("Arial", 12)).grid(row=0, column=0, sticky=tk.W, pady=5)
        self.current_pwd_entry = ttk.Entry(pwd_frame, font=("Arial", 12), width=25, show="*")
        self.current_pwd_entry.grid(row=0, column=1, pady=5, padx=10)
        
        # New password
        ttk.Label(pwd_frame, text="New Password:", font=("Arial", 12)).grid(row=1, column=0, sticky=tk.W, pady=5)
        self.new_pwd_entry = ttk.Entry(pwd_frame, font=("Arial", 12), width=25, show="*")
        self.new_pwd_entry.grid(row=1, column=1, pady=5, padx=10)
        
        # Confirm new password
        ttk.Label(pwd_frame, text="Confirm New Password:", font=("Arial", 12)).grid(row=2, column=0, sticky=tk.W, pady=5)
        self.confirm_pwd_entry = ttk.Entry(pwd_frame, font=("Arial", 12), width=25, show="*")
        self.confirm_pwd_entry.grid(row=2, column=1, pady=5, padx=10)
        
        # Change button
        change_btn = ttk.Button(pwd_frame, text="Change Password", command=self.change_password)
        change_btn.grid(row=3, column=0, columnspan=2, pady=20)
    
    def change_password(self):
        """Change user password"""
        current = self.current_pwd_entry.get()
        new = self.new_pwd_entry.get()
        confirm = self.confirm_pwd_entry.get()
        
        if not all([current, new, confirm]):
            messagebox.showerror("Error", "Please fill all fields")
            return
        
        if new != confirm:
            messagebox.showerror("Error", "New passwords do not match")
            return
        
        try:
            response = requests.post(f"{self.backend_url}/api/change-password", 
                                   json={"current_password": current, "new_password": new})
            
            if response.status_code == 200:
                messagebox.showinfo("Success", "Password changed successfully!")
                # Clear form
                self.current_pwd_entry.delete(0, tk.END)
                self.new_pwd_entry.delete(0, tk.END)
                self.confirm_pwd_entry.delete(0, tk.END)
            else:
                error_msg = response.json().get('error', 'Password change failed')
                messagebox.showerror("Error", error_msg)
        except requests.exceptions.RequestException:
            messagebox.showerror("Error", "Cannot connect to server")
    
    def create_admin_dashboard(self):
        """Create admin dashboard"""
        self.clear_main_frame()
        
        # Create notebook for admin dashboard
        self.admin_notebook = ttk.Notebook(self.main_frame)
        self.admin_notebook.pack(fill=tk.BOTH, expand=True)
        
        # Welcome message
        welcome_frame = ttk.Frame(self.main_frame)
        welcome_frame.pack(fill=tk.X, pady=5)
        
        welcome_label = tk.Label(welcome_frame, 
                                text=f"Admin Dashboard - Welcome, {self.current_user['username']}!", 
                                font=("Arial", 16, "bold"), fg='#e74c3c')
        welcome_label.pack(side=tk.LEFT)
        
        logout_btn = ttk.Button(welcome_frame, text="Logout", command=self.logout)
        logout_btn.pack(side=tk.RIGHT)
        
        # Admin tabs
        self.admin_home_frame = ttk.Frame(self.admin_notebook)
        self.admin_notebook.add(self.admin_home_frame, text="Dashboard")
        self.create_admin_home()
        
        self.admin_users_frame = ttk.Frame(self.admin_notebook)
        self.admin_notebook.add(self.admin_users_frame, text="User Management")
        self.create_admin_users_page()
        
        self.admin_results_frame = ttk.Frame(self.admin_notebook)
        self.admin_notebook.add(self.admin_results_frame, text="All Results")
        self.create_admin_results_page()
        
        self.admin_pwd_frame = ttk.Frame(self.admin_notebook)
        self.admin_notebook.add(self.admin_pwd_frame, text="Change Password")
        self.create_admin_change_password_page()
    
    def create_admin_home(self):
        """Create admin home page"""
        title = tk.Label(self.admin_home_frame, text="System Statistics", 
                        font=("Arial", 20, "bold"), fg='#2c3e50')
        title.pack(pady=20)
        
        # Stats frame
        stats_frame = ttk.LabelFrame(self.admin_home_frame, text="Overview", padding=20)
        stats_frame.pack(pady=20, padx=20, fill=tk.X)
        
        try:
            self.load_admin_stats(stats_frame)
        except:
            error_label = tk.Label(stats_frame, text="Unable to load statistics", 
                                 font=("Arial", 12), fg='#e74c3c')
            error_label.pack()
    
    def load_admin_stats(self, parent):
        """Load admin statistics"""
        try:
            response = requests.get(f"{self.backend_url}/api/admin/statistics")
            if response.status_code == 200:
                stats = response.json()
                
                # Total users
                users_label = tk.Label(parent, 
                                     text=f"Total Users: {stats['total_users']}", 
                                     font=("Arial", 14))
                users_label.pack(anchor='w', pady=5)
                
                # Total predictions
                pred_label = tk.Label(parent, 
                                    text=f"Total Predictions: {stats['total_predictions']}", 
                                    font=("Arial", 14))
                pred_label.pack(anchor='w', pady=5)
                
                # Predictions by company
                company_label = tk.Label(parent, text="Predictions by Company:", 
                                       font=("Arial", 14, "bold"))
                company_label.pack(anchor='w', pady=(10, 5))
                
                for company, count in stats['predictions_by_company'].items():
                    comp_label = tk.Label(parent, text=f"  {company}: {count}", 
                                        font=("Arial", 12))
                    comp_label.pack(anchor='w', pady=2)
            else:
                error_label = tk.Label(parent, text="Failed to load statistics", 
                                     font=("Arial", 12), fg='#e74c3c')
                error_label.pack()
        except:
            error_label = tk.Label(parent, text="Cannot connect to server", 
                                 font=("Arial", 12), fg='#e74c3c')
            error_label.pack()
    
    def create_admin_users_page(self):
        """Create admin users management page"""
        # Refresh button
        refresh_btn = ttk.Button(self.admin_users_frame, text="Refresh", command=self.load_users)
        refresh_btn.pack(anchor=tk.NE, pady=5, padx=10)
        
        # Users tree
        columns = ('ID', 'Username', 'Email', 'Admin', 'Created')
        self.users_tree = ttk.Treeview(self.admin_users_frame, columns=columns, show='headings', height=20)
        
        for col in columns:
            self.users_tree.heading(col, text=col)
            self.users_tree.column(col, width=150)
        
        # Scrollbar
        users_scrollbar = ttk.Scrollbar(self.admin_users_frame, orient=tk.VERTICAL, command=self.users_tree.yview)
        self.users_tree.configure(yscrollcommand=users_scrollbar.set)
        
        self.users_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        users_scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=10)
        
        # Load initial data
        self.load_users()
    
    def load_users(self):
        """Load all users"""
        try:
            response = requests.get(f"{self.backend_url}/api/admin/users")
            if response.status_code == 200:
                users = response.json()
                
                # Clear existing data
                for item in self.users_tree.get_children():
                    self.users_tree.delete(item)
                
                # Add new data
                for user in users:
                    values = (
                        user['id'],
                        user['username'],
                        user['email'],
                        'Yes' if user['is_admin'] else 'No',
                        user['created_at'][:10]
                    )
                    self.users_tree.insert('', tk.END, values=values)
            else:
                messagebox.showerror("Error", "Failed to load users")
        except requests.exceptions.RequestException:
            messagebox.showerror("Error", "Cannot connect to server")
    
    def create_admin_results_page(self):
        """Create admin results page - same as history but for all users"""
        # Refresh button
        refresh_btn = ttk.Button(self.admin_results_frame, text="Refresh", command=self.load_all_results)
        refresh_btn.pack(anchor=tk.NE, pady=5, padx=10)
        
        # Results tree
        columns = ('User', 'Date', 'Company', 'Model', 'Predicted', 'Target Date', 'RMSE')
        self.results_tree = ttk.Treeview(self.admin_results_frame, columns=columns, show='headings', height=20)
        
        for col in columns:
            self.results_tree.heading(col, text=col)
            self.results_tree.column(col, width=100)
        
        # Scrollbar
        results_scrollbar = ttk.Scrollbar(self.admin_results_frame, orient=tk.VERTICAL, command=self.results_tree.yview)
        self.results_tree.configure(yscrollcommand=results_scrollbar.set)
        
        self.results_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        results_scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=10)
        
        # Load initial data
        self.load_all_results()
    
    def load_all_results(self):
        """Load all prediction results"""
        try:
            response = requests.get(f"{self.backend_url}/api/predictions/history")
            if response.status_code == 200:
                predictions = response.json()
                
                # Clear existing data
                for item in self.results_tree.get_children():
                    self.results_tree.delete(item)
                
                # Add new data
                for pred in predictions:
                    values = (
                        pred.get('username', 'Unknown'),
                        pred['prediction_date'][:10],
                        pred['company'],
                        pred['model_used'],
                        f"₹{pred['predicted_price']:.2f}",
                        pred['target_date'],
                        f"{pred['rmse']:.4f}" if pred['rmse'] else 'N/A'
                    )
                    self.results_tree.insert('', tk.END, values=values)
            else:
                messagebox.showerror("Error", "Failed to load results")
        except requests.exceptions.RequestException:
            messagebox.showerror("Error", "Cannot connect to server")
    
    def create_admin_change_password_page(self):
        """Create admin change password page"""
        pwd_frame = ttk.LabelFrame(self.admin_pwd_frame, text="Change Admin Password", padding=40)
        pwd_frame.pack(expand=True)
        
        # Current password
        ttk.Label(pwd_frame, text="Current Password:", font=("Arial", 12)).grid(row=0, column=0, sticky=tk.W, pady=5)
        self.admin_current_pwd_entry = ttk.Entry(pwd_frame, font=("Arial", 12), width=25, show="*")
        self.admin_current_pwd_entry.grid(row=0, column=1, pady=5, padx=10)
        
        # New password
        ttk.Label(pwd_frame, text="New Password:", font=("Arial", 12)).grid(row=1, column=0, sticky=tk.W, pady=5)
        self.admin_new_pwd_entry = ttk.Entry(pwd_frame, font=("Arial", 12), width=25, show="*")
        self.admin_new_pwd_entry.grid(row=1, column=1, pady=5, padx=10)
        
        # Confirm new password
        ttk.Label(pwd_frame, text="Confirm New Password:", font=("Arial", 12)).grid(row=2, column=0, sticky=tk.W, pady=5)
        self.admin_confirm_pwd_entry = ttk.Entry(pwd_frame, font=("Arial", 12), width=25, show="*")
        self.admin_confirm_pwd_entry.grid(row=2, column=1, pady=5, padx=10)
        
        # Change button
        change_btn = ttk.Button(pwd_frame, text="Change Password", command=self.admin_change_password)
        change_btn.grid(row=3, column=0, columnspan=2, pady=20)
    
    def admin_change_password(self):
        """Change admin password"""
        current = self.admin_current_pwd_entry.get()
        new = self.admin_new_pwd_entry.get()
        confirm = self.admin_confirm_pwd_entry.get()
        
        if not all([current, new, confirm]):
            messagebox.showerror("Error", "Please fill all fields")
            return
        
        if new != confirm:
            messagebox.showerror("Error", "New passwords do not match")
            return
        
        try:
            response = requests.post(f"{self.backend_url}/api/change-password", 
                                   json={"current_password": current, "new_password": new})
            
            if response.status_code == 200:
                messagebox.showinfo("Success", "Admin password changed successfully!")
                # Clear form
                self.admin_current_pwd_entry.delete(0, tk.END)
                self.admin_new_pwd_entry.delete(0, tk.END)
                self.admin_confirm_pwd_entry.delete(0, tk.END)
            else:
                error_msg = response.json().get('error', 'Password change failed')
                messagebox.showerror("Error", error_msg)
        except requests.exceptions.RequestException:
            messagebox.showerror("Error", "Cannot connect to server")
    
    def logout(self):
        """Logout user"""
        try:
            requests.post(f"{self.backend_url}/api/logout")
        except:
            pass
        
        self.current_user = None
        self.is_admin = False
        self.create_public_pages()
        messagebox.showinfo("Success", "Logged out successfully!")
    
    # Navigation helper methods
    def go_to_predictions(self):
        self.dashboard_notebook.select(1)
    
    def go_to_history(self):
        self.dashboard_notebook.select(2)
    
    def go_to_change_password(self):
        self.dashboard_notebook.select(3)
    
    def run(self):
        """Run the application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = StockPredictionApp()
    app.run()