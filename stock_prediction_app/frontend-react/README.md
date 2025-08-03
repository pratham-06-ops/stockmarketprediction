# Stock Prediction Frontend

A modern React frontend for the Stock Prediction Application built with React 18, Tailwind CSS, and Recharts.

## Features

- 🎨 **Modern UI/UX** - Clean, responsive design with Tailwind CSS
- 📊 **Interactive Charts** - Real-time stock data visualization with Recharts
- 🔮 **AI Predictions** - Advanced machine learning-based stock predictions
- 📱 **Mobile Responsive** - Optimized for all device sizes
- 🌙 **Dark Mode Support** - Light and dark theme options
- 📈 **Portfolio Tracking** - Comprehensive portfolio management
- 🔔 **Real-time Notifications** - Customizable alert system
- 🛡️ **Security Features** - Two-factor authentication support

## Project Structure

```
frontend-react/
├── public/                 # Static files
│   └── index.html         # Main HTML template
├── src/
│   ├── components/        # Reusable components
│   │   └── Layout/        # Layout components
│   │       ├── Layout.js  # Main layout wrapper
│   │       ├── Header.js  # Top navigation bar
│   │       └── Sidebar.js # Side navigation menu
│   ├── pages/             # Page components
│   │   ├── Home/          # Landing page
│   │   ├── Dashboard/     # Main dashboard
│   │   ├── Analysis/      # Stock analysis tools
│   │   ├── Portfolio/     # Portfolio management
│   │   └── Settings/      # User settings
│   ├── App.js             # Main app component
│   ├── index.js           # App entry point
│   └── index.css          # Global styles
├── package.json           # Dependencies and scripts
├── tailwind.config.js     # Tailwind CSS configuration
└── postcss.config.js      # PostCSS configuration
```

## Technologies Used

- **React 18** - Modern React with hooks and functional components
- **React Router** - Client-side routing
- **Tailwind CSS** - Utility-first CSS framework
- **Recharts** - Composable charting library
- **Lucide React** - Beautiful & consistent icon toolkit
- **Axios** - HTTP client for API requests

## Getting Started

### Prerequisites

- Node.js (version 16 or higher)
- npm or yarn package manager

### Installation

1. **Navigate to the frontend directory:**
   ```bash
   cd stock_prediction_app/frontend-react
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start the development server:**
   ```bash
   npm start
   ```

4. **Open your browser and visit:**
   ```
   http://localhost:3000
   ```

### Available Scripts

- `npm start` - Runs the app in development mode
- `npm build` - Builds the app for production
- `npm test` - Launches the test runner
- `npm eject` - Ejects from Create React App (one-way operation)

## Pages Overview

### 🏠 Home Page
- Hero section with call-to-action
- Feature highlights
- Platform statistics
- Getting started guide

### 📊 Dashboard
- Portfolio overview with key metrics
- Interactive charts (portfolio performance, trading volume)
- Watchlist with real-time price updates
- Quick action buttons

### 🔍 Analysis
- AI-powered stock predictions
- Technical analysis indicators
- Market sentiment analysis
- Support and resistance levels
- Interactive prediction charts

### 💼 Portfolio
- Holdings overview with allocation charts
- Performance tracking over time
- Transaction history
- Buy/sell actions
- Portfolio analytics

### ⚙️ Settings
- Account information management
- Notification preferences
- Security settings (2FA, password)
- App preferences (theme, language, currency)
- Data export and privacy controls

## Styling

The application uses **Tailwind CSS** for styling with a custom color scheme:

- Primary: Blue (`#3b82f6`)
- Success: Green (`#10b981`)
- Danger: Red (`#ef4444`)
- Warning: Yellow (`#f59e0b`)

### Custom Classes
- Responsive design with mobile-first approach
- Custom color palette defined in `tailwind.config.js`
- Consistent spacing and typography

## Component Architecture

### Layout Components
- **Layout**: Main wrapper with header and sidebar
- **Header**: Top navigation with search and user menu
- **Sidebar**: Side navigation with responsive design

### Page Components
- Organized by feature in separate directories
- Each page is a functional component with hooks
- Consistent styling and structure across pages

## State Management

- React built-in state management with `useState` and `useEffect`
- Local state for component-specific data
- Future: Redux/Context API for global state

## Charts and Visualization

Uses **Recharts** library for all data visualization:
- Line charts for stock price trends
- Area charts for portfolio performance
- Pie charts for portfolio allocation
- Bar charts for trading volume
- Composed charts for prediction data

## Responsive Design

- Mobile-first approach
- Breakpoints: `sm`, `md`, `lg`, `xl`
- Responsive navigation with mobile sidebar
- Optimized layouts for different screen sizes

## Development Notes

### Code Style
- Functional components with React Hooks
- Consistent naming conventions
- Clean and maintainable code structure
- Proper component separation

### Performance
- Lazy loading for large components (future enhancement)
- Optimized re-renders with proper dependency arrays
- Efficient chart rendering with ResponsiveContainer

## Future Enhancements

- [ ] Real-time WebSocket connections
- [ ] Advanced filtering and search
- [ ] More chart types and indicators
- [ ] Dark mode implementation
- [ ] PWA capabilities
- [ ] Unit and integration tests
- [ ] Performance optimizations
- [ ] Accessibility improvements

## Contributing

1. Follow the existing code style and structure
2. Create feature branches for new functionality
3. Ensure responsive design for all new components
4. Test across different browsers and devices
5. Update documentation for new features

## API Integration

The frontend is designed to integrate with the backend API:
- Base URL configuration in environment variables
- Axios for HTTP requests
- Error handling and loading states
- Authentication token management

---

Built with ❤️ using React and modern web technologies.