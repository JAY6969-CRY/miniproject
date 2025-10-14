import React, { useState } from 'react';
import { getQuote, getPrediction, getSignal, getChartData, getPortfolioSignal } from './api';
import StockChart from './components/StockChart';
import SignalCard from './components/SignalCard';
import PriceCard from './components/PriceCard';
import SearchBar from './components/SearchBar';
import Footer from './components/Footer';

function App() {
  const [symbol, setSymbol] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [portfolioType, setPortfolioType] = useState('balanced');
  
  const [quoteData, setQuoteData] = useState(null);
  const [predictionData, setPredictionData] = useState(null);
  const [signalData, setSignalData] = useState(null);
  const [chartData, setChartData] = useState(null);

  const handleSearch = async (searchSymbol) => {
    if (!searchSymbol.trim()) {
      setError('Please enter a stock symbol');
      return;
    }

    setLoading(true);
    setError(null);
    setSymbol(searchSymbol.toUpperCase());

    try {
      // Fetch all data in parallel
      const [quote, prediction, signal, chart] = await Promise.all([
        getQuote(searchSymbol),
        getPrediction(searchSymbol),
        getPortfolioSignal(searchSymbol, portfolioType),
        getChartData(searchSymbol),
      ]);

      setQuoteData(quote);
      setPredictionData(prediction);
      setSignalData(signal);
      setChartData(chart);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to fetch stock data. Please check the symbol and try again.');
      setQuoteData(null);
      setPredictionData(null);
      setSignalData(null);
      setChartData(null);
    } finally {
      setLoading(false);
    }
  };

  const handlePortfolioTypeChange = async (newType) => {
    setPortfolioType(newType);
    
    if (symbol) {
      try {
        const signal = await getPortfolioSignal(symbol, newType);
        setSignalData(signal);
      } catch (err) {
        console.error('Failed to update signal:', err);
      }
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8">
          <h1 className="text-3xl font-bold text-gray-900">
            📈 Stock Market Forecast
          </h1>
          <p className="mt-1 text-sm text-gray-600">
            Next-day price predictions for NSE, BSE & NASDAQ
          </p>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
        {/* Search Bar */}
        <SearchBar onSearch={handleSearch} loading={loading} />

        {/* Portfolio Type Selector */}
        {symbol && (
          <div className="mt-6 flex justify-center space-x-4">
            <button
              onClick={() => handlePortfolioTypeChange('aggressive')}
              className={`px-4 py-2 rounded-lg font-medium transition ${
                portfolioType === 'aggressive'
                  ? 'bg-red-600 text-white'
                  : 'bg-white text-gray-700 hover:bg-gray-50'
              }`}
            >
              Aggressive
            </button>
            <button
              onClick={() => handlePortfolioTypeChange('balanced')}
              className={`px-4 py-2 rounded-lg font-medium transition ${
                portfolioType === 'balanced'
                  ? 'bg-blue-600 text-white'
                  : 'bg-white text-gray-700 hover:bg-gray-50'
              }`}
            >
              Balanced
            </button>
            <button
              onClick={() => handlePortfolioTypeChange('long_term')}
              className={`px-4 py-2 rounded-lg font-medium transition ${
                portfolioType === 'long_term'
                  ? 'bg-green-600 text-white'
                  : 'bg-white text-gray-700 hover:bg-gray-50'
              }`}
            >
              Long Term
            </button>
          </div>
        )}

        {/* Error Message */}
        {error && (
          <div className="mt-6 bg-red-50 border-l-4 border-red-400 p-4 rounded">
            <div className="flex">
              <div className="flex-shrink-0">
                <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                </svg>
              </div>
              <div className="ml-3">
                <p className="text-sm text-red-700">{error}</p>
              </div>
            </div>
          </div>
        )}

        {/* Loading Spinner */}
        {loading && (
          <div className="mt-8 flex justify-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
          </div>
        )}

        {/* Results */}
        {!loading && predictionData && (
          <div className="mt-8 space-y-6">
            {/* Price Cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <PriceCard
                title="Current Price"
                price={predictionData.current_price}
                symbol={symbol}
                quote={quoteData}
              />
              <PriceCard
                title="Predicted Price"
                price={predictionData.predicted_price}
                symbol={symbol}
                change={predictionData.prediction_change}
                changePercent={predictionData.prediction_change_percent}
              />
            </div>

            {/* Signal Card */}
            {signalData && (
              <SignalCard signal={signalData} />
            )}

            {/* Chart */}
            {chartData && (
              <div className="bg-white rounded-lg shadow-md p-6">
                <h2 className="text-xl font-semibold text-gray-800 mb-4">
                  Price Trend & Forecast
                </h2>
                <StockChart data={chartData} />
              </div>
            )}
          </div>
        )}

        {/* Examples */}
        {!symbol && !loading && (
          <div className="mt-12 bg-white rounded-lg shadow-md p-6">
            <h2 className="text-lg font-semibold text-gray-800 mb-4">
              Try these examples:
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <h3 className="font-medium text-gray-700 mb-2">NSE (India)</h3>
                <ul className="space-y-1 text-sm text-gray-600">
                  <li className="cursor-pointer hover:text-blue-600" onClick={() => handleSearch('RELIANCE.NS')}>
                    • RELIANCE.NS
                  </li>
                  <li className="cursor-pointer hover:text-blue-600" onClick={() => handleSearch('TCS.NS')}>
                    • TCS.NS
                  </li>
                  <li className="cursor-pointer hover:text-blue-600" onClick={() => handleSearch('INFY.NS')}>
                    • INFY.NS
                  </li>
                </ul>
              </div>
              <div>
                <h3 className="font-medium text-gray-700 mb-2">BSE (India)</h3>
                <ul className="space-y-1 text-sm text-gray-600">
                  <li className="cursor-pointer hover:text-blue-600" onClick={() => handleSearch('RELIANCE.BO')}>
                    • RELIANCE.BO
                  </li>
                  <li className="cursor-pointer hover:text-blue-600" onClick={() => handleSearch('TCS.BO')}>
                    • TCS.BO
                  </li>
                  <li className="cursor-pointer hover:text-blue-600" onClick={() => handleSearch('INFY.BO')}>
                    • INFY.BO
                  </li>
                </ul>
              </div>
              <div>
                <h3 className="font-medium text-gray-700 mb-2">NASDAQ (US)</h3>
                <ul className="space-y-1 text-sm text-gray-600">
                  <li className="cursor-pointer hover:text-blue-600" onClick={() => handleSearch('AAPL')}>
                    • AAPL
                  </li>
                  <li className="cursor-pointer hover:text-blue-600" onClick={() => handleSearch('GOOGL')}>
                    • GOOGL
                  </li>
                  <li className="cursor-pointer hover:text-blue-600" onClick={() => handleSearch('MSFT')}>
                    • MSFT
                  </li>
                </ul>
              </div>
            </div>
          </div>
        )}
      </main>

      {/* Footer */}
      <Footer />
    </div>
  );
}

export default App;
