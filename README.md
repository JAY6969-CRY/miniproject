# Stock Market Forecast - Full Stack MVP

A full-stack web application for predicting next-day stock prices for NSE, BSE, and NASDAQ tickers using machine learning.

![Tech Stack](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-61DAFB?style=flat&logo=react&logoColor=black)
![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/Tailwind-38B2AC?style=flat&logo=tailwind-css&logoColor=white)

## 🚀 Features

- **Real-time Stock Quotes**: Fetches current prices from Alpha Vantage API with yfinance fallback
- **Next-Day Price Prediction**: Uses Linear Regression with technical indicators (SMA, RSI)
- **Trading Signals**: Buy/Sell/Hold recommendations with reasoning and timing
- **Portfolio Strategies**: Aggressive, Balanced, and Long-term investment approaches
- **Interactive Charts**: Visual price trends with Chart.js
- **Smart Caching**: SQLite-based caching for improved performance
- **Multi-Market Support**: NSE (India), BSE (India), and NASDAQ (US)

## 📋 Prerequisites

- Python 3.8+
- Node.js 16+
- Alpha Vantage API Key (free tier available at https://www.alphavantage.co/support/#api-key)

## 🛠️ Installation

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create and activate virtual environment:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
# Copy example env file
copy .env.example .env

# Edit .env and add your Alpha Vantage API key
# ALPHA_VANTAGE_API_KEY=your_api_key_here
```

5. Start the backend server:
```bash
python main.py
```

The API will be available at http://localhost:8000

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Configure environment:
```bash
# Copy example env file
copy .env.example .env

# Default API URL is http://localhost:8000
```

4. Start the development server:
```bash
npm run dev
```

The frontend will be available at http://localhost:3000

## 📊 API Endpoints

### `GET /quote?symbol=RELIANCE.NS`
Get current stock quote with price, change, volume

### `GET /predict?symbol=RELIANCE.NS`
Predict next-day closing price

### `GET /signal?symbol=RELIANCE.NS`
Get buy/sell/hold recommendation

### `GET /chart?symbol=RELIANCE.NS`
Get historical + prediction data for charting

### `GET /portfolio?symbol=RELIANCE.NS&type=aggressive`
Get personalized signal based on portfolio type (aggressive/balanced/long_term)

### `POST /train?symbol=RELIANCE.NS`
Manually train or retrain model for a symbol

## 🎯 Usage Examples

### NSE Stocks (India)
- RELIANCE.NS
- TCS.NS
- INFY.NS
- HDFCBANK.NS

### BSE Stocks (India)
- RELIANCE.BO
- TCS.BO
- INFY.BO

### NASDAQ Stocks (US)
- AAPL
- GOOGL
- MSFT
- TSLA

## 🧠 How It Works

1. **Data Fetching**: Retrieves historical price data using Alpha Vantage API or yfinance
2. **Feature Engineering**: Calculates technical indicators:
   - Simple Moving Average (SMA 5 & 10)
   - Relative Strength Index (RSI 14)
3. **Model Training**: Trains Linear Regression model on 90 days of historical data
4. **Prediction**: Generates next-day price forecast
5. **Signal Generation**: Produces buy/sell/hold recommendation based on:
   - Predicted price movement
   - RSI overbought/oversold conditions
   - Portfolio risk tolerance

## 📁 Project Structure

```
miniproject/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration settings
│   ├── data_fetcher.py      # Data retrieval & caching
│   ├── model_trainer.py     # ML model training
│   ├── predictor.py         # Prediction & signal logic
│   ├── requirements.txt     # Python dependencies
│   ├── .env.example         # Environment template
│   └── models/              # Trained model storage
│
└── frontend/
    ├── src/
    │   ├── App.jsx          # Main application
    │   ├── api.js           # API client
    │   ├── components/
    │   │   ├── SearchBar.jsx
    │   │   ├── PriceCard.jsx
    │   │   ├── SignalCard.jsx
    │   │   ├── StockChart.jsx
    │   │   └── Footer.jsx
    │   └── index.css        # Tailwind styles
    ├── package.json
    └── vite.config.js
```

## 🚢 Deployment

### Deploy to Railway

1. Create new project on Railway
2. Connect your GitHub repository
3. Add environment variables:
   - `ALPHA_VANTAGE_API_KEY`
4. Deploy backend and frontend separately

### Deploy to Render

1. Create new Web Service
2. Connect repository
3. Set build command: `pip install -r requirements.txt` (backend) or `npm install && npm run build` (frontend)
4. Set start command: `python main.py` (backend) or `npm run preview` (frontend)
5. Add environment variables

## ⚠️ Disclaimer

This tool provides market forecasts based on historical data and technical analysis. All predictions are for **informational purposes only** and should not be considered as financial advice. Past performance does not guarantee future results. Please consult with a qualified financial advisor before making any investment decisions.

## 🔧 Technologies Used

**Backend:**
- FastAPI - Modern Python web framework
- scikit-learn - Machine learning
- pandas & numpy - Data processing
- yfinance - Stock data
- SQLite - Caching

**Frontend:**
- React - UI framework
- Vite - Build tool
- Tailwind CSS - Styling
- Chart.js - Data visualization
- Axios - HTTP client

## 📝 License

This project is for educational purposes only.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Support

For issues or questions, please open an issue on GitHub.
