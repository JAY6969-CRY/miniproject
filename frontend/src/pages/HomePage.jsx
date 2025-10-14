import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { getQuote, getPrediction, getSignal, getChartData, getPortfolioSignal, analyzeQuery } from '../api';
import StockChart from '../components/StockChart';
import SignalCard from '../components/SignalCard';
import PriceCard from '../components/PriceCard';
import SearchBar from '../components/SearchBar';
import Footer from '../components/Footer';
import AnalysisCard from '../components/AnalysisCard';

function HomePage() {
  const [symbol, setSymbol] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [portfolioType, setPortfolioType] = useState('balanced');
  const [viewMode, setViewMode] = useState('simple'); // 'simple' or 'advanced'
  
  const [quoteData, setQuoteData] = useState(null);
  const [predictionData, setPredictionData] = useState(null);
  const [signalData, setSignalData] = useState(null);
  const [chartData, setChartData] = useState(null);
  const [analysisData, setAnalysisData] = useState(null);

  const handleSearch = async (searchSymbol, budget = null) => {
    if (!searchSymbol.trim()) {
      setError('Please enter a stock symbol or question');
      return;
    }

    setLoading(true);
    setError(null);
    
    // Check if it's a natural language query (contains spaces or question words)
    const isNaturalLanguage = searchSymbol.includes(' ') || 
                              /\b(can|should|is|how|what|buy|sell|invest|worth|good|bad)\b/i.test(searchSymbol);
    
    try {
      if (isNaturalLanguage) {
        // Use advanced NLP analysis
        setViewMode('advanced');
        const analysis = await analyzeQuery(searchSymbol, portfolioType, budget);
        setAnalysisData(analysis);
        
        if (analysis.success) {
          setSymbol(analysis.symbol);
          // Also set basic data for compatibility
          setQuoteData(analysis.quote);
          setPredictionData(analysis.prediction);
          setSignalData(analysis.signal);
        }
      } else {
        // Simple symbol search
        setViewMode('simple');
        setSymbol(searchSymbol.toUpperCase());
        setAnalysisData(null);
        
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
      }
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to fetch stock data. Please check your input and try again.');
      setQuoteData(null);
      setPredictionData(null);
      setSignalData(null);
      setChartData(null);
      setAnalysisData(null);
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
            AI-powered predictions & intelligent trading strategies
          </p>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
        {/* Trading Strategy Cards */}
        <div className="mb-8">
          <h2 className="text-2xl font-bold text-gray-800 mb-4 text-center">
            Choose Your Trading Style
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {/* Aggressive Card */}
            <Link
              to="/aggressive"
              className="group relative overflow-hidden bg-gradient-to-br from-red-500 to-orange-600 rounded-xl shadow-lg hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-2"
            >
              <div className="p-8 text-white">
                <div className="text-6xl mb-4">⚡</div>
                <h3 className="text-2xl font-bold mb-2">Aggressive</h3>
                <p className="text-lg mb-4 text-red-100">Intraday Trading</p>
                <div className="space-y-2 text-sm mb-6">
                  <div className="flex items-center gap-2">
                    <span className="text-xl">📊</span>
                    <span>1-2 day holds</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className="text-xl">🎯</span>
                    <span>4% target profit</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className="text-xl">🛡️</span>
                    <span>1.5% stop loss</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className="text-xl">⚠️</span>
                    <span>HIGH risk</span>
                  </div>
                </div>
                <div className="inline-flex items-center gap-2 bg-white/20 px-4 py-2 rounded-lg group-hover:bg-white/30 transition">
                  <span>Start Trading</span>
                  <span className="text-xl">→</span>
                </div>
              </div>
              <div className="absolute -right-4 -bottom-4 text-9xl opacity-10">⚡</div>
            </Link>

            {/* Balanced Card */}
            <div className="group relative overflow-hidden bg-gradient-to-br from-blue-500 to-indigo-600 rounded-xl shadow-lg hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-2 cursor-pointer">
              <div className="p-8 text-white">
                <div className="text-6xl mb-4">⚖️</div>
                <h3 className="text-2xl font-bold mb-2">Balanced</h3>
                <p className="text-lg mb-4 text-blue-100">Swing Trading</p>
                <div className="space-y-2 text-sm mb-6">
                  <div className="flex items-center gap-2">
                    <span className="text-xl">📊</span>
                    <span>1-4 week holds</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className="text-xl">🎯</span>
                    <span>10% target profit</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className="text-xl">🛡️</span>
                    <span>5% stop loss</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className="text-xl">⚖️</span>
                    <span>MEDIUM risk</span>
                  </div>
                </div>
                <div className="inline-flex items-center gap-2 bg-white/20 px-4 py-2 rounded-lg">
                  <span>Default View</span>
                  <span className="text-xl">✓</span>
                </div>
              </div>
              <div className="absolute -right-4 -bottom-4 text-9xl opacity-10">⚖️</div>
            </div>

            {/* Long-Term Card */}
            <Link
              to="/long-term"
              className="group relative overflow-hidden bg-gradient-to-br from-green-500 to-emerald-600 rounded-xl shadow-lg hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-2"
            >
              <div className="p-8 text-white">
                <div className="text-6xl mb-4">📈</div>
                <h3 className="text-2xl font-bold mb-2">Long-Term</h3>
                <p className="text-lg mb-4 text-green-100">Investment</p>
                <div className="space-y-2 text-sm mb-6">
                  <div className="flex items-center gap-2">
                    <span className="text-xl">📊</span>
                    <span>3-6 month holds</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className="text-xl">🎯</span>
                    <span>20% target profit</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className="text-xl">🛡️</span>
                    <span>8% stop loss</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className="text-xl">💎</span>
                    <span>LOWER risk</span>
                  </div>
                </div>
                <div className="inline-flex items-center gap-2 bg-white/20 px-4 py-2 rounded-lg group-hover:bg-white/30 transition">
                  <span>Start Investing</span>
                  <span className="text-xl">→</span>
                </div>
              </div>
              <div className="absolute -right-4 -bottom-4 text-9xl opacity-10">📈</div>
            </Link>
          </div>
        </div>

        {/* Search Bar */}
        <SearchBar onSearch={handleSearch} loading={loading} />

        {/* Portfolio Type Selector (for balanced mode) */}
        {symbol && (
          <div className="mt-6">
            <div className="max-w-4xl mx-auto">
              <p className="text-center text-sm text-gray-600 mb-3">Current strategy:</p>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <button
                  onClick={() => handlePortfolioTypeChange('aggressive')}
                  className={`p-4 rounded-lg font-medium transition border-2 ${
                    portfolioType === 'aggressive'
                      ? 'bg-red-600 text-white border-red-600'
                      : 'bg-white text-gray-700 hover:bg-red-50 border-gray-300'
                  }`}
                >
                  <div className="text-lg mb-1">⚡ Aggressive</div>
                  <div className="text-xs opacity-80">Intraday</div>
                </button>
                <button
                  onClick={() => handlePortfolioTypeChange('balanced')}
                  className={`p-4 rounded-lg font-medium transition border-2 ${
                    portfolioType === 'balanced'
                      ? 'bg-blue-600 text-white border-blue-600'
                      : 'bg-white text-gray-700 hover:bg-blue-50 border-gray-300'
                  }`}
                >
                  <div className="text-lg mb-1">⚖️ Balanced</div>
                  <div className="text-xs opacity-80">Swing</div>
                </button>
                <button
                  onClick={() => handlePortfolioTypeChange('long_term')}
                  className={`p-4 rounded-lg font-medium transition border-2 ${
                    portfolioType === 'long_term'
                      ? 'bg-green-600 text-white border-green-600'
                      : 'bg-white text-gray-700 hover:bg-green-50 border-gray-300'
                  }`}
                >
                  <div className="text-lg mb-1">📈 Long-Term</div>
                  <div className="text-xs opacity-80">Investment</div>
                </button>
              </div>
            </div>
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

        {/* Results - Advanced View (Natural Language Analysis) */}
        {!loading && viewMode === 'advanced' && analysisData && (
          <div className="mt-8">
            <AnalysisCard data={analysisData} />
          </div>
        )}

        {/* Results - Simple View (Traditional Symbol Search) */}
        {!loading && viewMode === 'simple' && predictionData && (
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

export default HomePage;
