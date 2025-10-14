import React, { useState } from 'react';
import { analyzeQueryGemini, analyzeQuery } from '../api';
import SearchBar from '../components/SearchBar';
import AnalysisCard from '../components/AnalysisCard';
import TopStocksChart from '../components/TopStocksChart';

function AggressivePage() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [analysisData, setAnalysisData] = useState(null);
  const [symbol, setSymbol] = useState('');

  const handleSearch = async (searchQuery, budget = null) => {
    if (!searchQuery.trim()) {
      setError('Please enter a stock symbol or question');
      return;
    }

    setLoading(true);
    setError(null);
    
    try {
      // Try Gemini AI first, fall back to standard analyzer
      let analysis;
      try {
        analysis = await analyzeQueryGemini(searchQuery, 'aggressive', budget);
      } catch (geminiError) {
        console.log('Gemini not available, using standard analyzer');
        analysis = await analyzeQuery(searchQuery, 'aggressive', budget);
      }
      
      setAnalysisData(analysis);
      
      if (analysis.success) {
        setSymbol(analysis.symbol);
      }
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to fetch stock data. Please check your input and try again.');
      setAnalysisData(null);
    } finally {
      setLoading(false);
    }
  };

  const handleStockSelect = (stockSymbol) => {
    handleSearch(stockSymbol);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-red-50 via-orange-50 to-red-100">
      {/* Header */}
      <header className="bg-gradient-to-r from-red-600 to-orange-600 shadow-lg">
        <div className="max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-4xl font-bold text-white flex items-center gap-3">
                <span className="text-5xl">⚡</span>
                Aggressive Trading (Intraday)
              </h1>
              <p className="mt-2 text-lg text-red-100">
                Quick profits · 1-2 day holds · Tight risk management
              </p>
            </div>
            <a
              href="/"
              className="px-6 py-3 bg-white text-red-600 rounded-lg font-semibold hover:bg-red-50 transition shadow-md"
            >
              ← Back to Home
            </a>
          </div>
        </div>
      </header>

      {/* Strategy Info Banner */}
      <div className="bg-white border-b-4 border-red-500 shadow-md">
        <div className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 text-center">
            <div className="p-4 bg-red-50 rounded-lg">
              <div className="text-2xl font-bold text-red-600">1.5%</div>
              <div className="text-sm text-gray-600">Stop Loss</div>
            </div>
            <div className="p-4 bg-orange-50 rounded-lg">
              <div className="text-2xl font-bold text-orange-600">4%</div>
              <div className="text-sm text-gray-600">Target Profit</div>
            </div>
            <div className="p-4 bg-red-50 rounded-lg">
              <div className="text-2xl font-bold text-red-600">1-2 Days</div>
              <div className="text-sm text-gray-600">Holding Period</div>
            </div>
            <div className="p-4 bg-orange-50 rounded-lg">
              <div className="text-2xl font-bold text-orange-600">30%</div>
              <div className="text-sm text-gray-600">Max Position Size</div>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
        {/* Search Bar */}
        <div className="mb-8">
          <SearchBar onSearch={handleSearch} loading={loading} />
        </div>

        {/* Top Stocks Chart */}
        {!symbol && !loading && (
          <div className="mb-8">
            <TopStocksChart region="US" onSelectStock={handleStockSelect} />
          </div>
        )}

        {/* Strategy Description */}
        {!symbol && !loading && (
          <div className="mb-8 bg-white rounded-xl shadow-lg p-8">
            <h2 className="text-2xl font-bold text-gray-800 mb-4 flex items-center gap-2">
              <span className="text-3xl">🎯</span>
              About Aggressive Trading
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <h3 className="font-semibold text-red-600 mb-2">✅ Best For:</h3>
                <ul className="space-y-2 text-gray-700">
                  <li>• Active day traders</li>
                  <li>• Quick profit opportunities</li>
                  <li>• High market volatility</li>
                  <li>• Full-time trading focus</li>
                  <li>• Technical analysis experts</li>
                </ul>
              </div>
              <div>
                <h3 className="font-semibold text-red-600 mb-2">⚠️ Risk Factors:</h3>
                <ul className="space-y-2 text-gray-700">
                  <li>• <strong>High risk</strong> - tight stops</li>
                  <li>• Requires constant monitoring</li>
                  <li>• Higher transaction costs</li>
                  <li>• Quick decision making needed</li>
                  <li>• Emotional discipline required</li>
                </ul>
              </div>
            </div>
            <div className="mt-6 p-4 bg-red-50 rounded-lg border-l-4 border-red-500">
              <p className="text-sm text-gray-700">
                <strong>💡 Pro Tip:</strong> Set alerts at your entry price and monitor RSI closely. 
                Exit by end of day or when target is hit. Never hold overnight unless strong uptrend confirmed.
              </p>
            </div>
          </div>
        )}

        {/* Error Message */}
        {error && (
          <div className="mb-6 bg-red-50 border-l-4 border-red-400 p-4 rounded">
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
          <div className="flex justify-center py-12">
            <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-red-600"></div>
          </div>
        )}

        {/* Analysis Results */}
        {!loading && analysisData && (
          <div className="animate-fade-in">
            <AnalysisCard data={analysisData} />
          </div>
        )}

        {/* Example Queries */}
        {!symbol && !loading && (
          <div className="bg-white rounded-xl shadow-lg p-8">
            <h2 className="text-xl font-semibold text-gray-800 mb-4">
              🚀 Try these intraday opportunities:
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              <button
                onClick={() => handleSearch('Should I day trade Apple stock?')}
                className="p-4 text-left bg-red-50 hover:bg-red-100 rounded-lg transition border-2 border-transparent hover:border-red-300"
              >
                <div className="font-semibold text-gray-800">Apple (AAPL)</div>
                <div className="text-sm text-gray-600">Should I day trade Apple?</div>
              </button>
              <button
                onClick={() => handleSearch('Is Tesla good for intraday trading?')}
                className="p-4 text-left bg-orange-50 hover:bg-orange-100 rounded-lg transition border-2 border-transparent hover:border-orange-300"
              >
                <div className="font-semibold text-gray-800">Tesla (TSLA)</div>
                <div className="text-sm text-gray-600">Intraday trading opportunity?</div>
              </button>
              <button
                onClick={() => handleSearch('Can I buy Microsoft for day trading?')}
                className="p-4 text-left bg-red-50 hover:bg-red-100 rounded-lg transition border-2 border-transparent hover:border-red-300"
              >
                <div className="font-semibold text-gray-800">Microsoft (MSFT)</div>
                <div className="text-sm text-gray-600">Day trading potential?</div>
              </button>
              <button
                onClick={() => handleSearch('Should I day trade Reliance?')}
                className="p-4 text-left bg-orange-50 hover:bg-orange-100 rounded-lg transition border-2 border-transparent hover:border-orange-300"
              >
                <div className="font-semibold text-gray-800">Reliance (RELIANCE.NS)</div>
                <div className="text-sm text-gray-600">NSE intraday trade?</div>
              </button>
              <button
                onClick={() => handleSearch('Is TCS good for quick trading?')}
                className="p-4 text-left bg-red-50 hover:bg-red-100 rounded-lg transition border-2 border-transparent hover:border-red-300"
              >
                <div className="font-semibold text-gray-800">TCS (TCS.NS)</div>
                <div className="text-sm text-gray-600">Quick profit opportunity?</div>
              </button>
              <button
                onClick={() => handleSearch('Should I scalp trade Google?')}
                className="p-4 text-left bg-orange-50 hover:bg-orange-100 rounded-lg transition border-2 border-transparent hover:border-orange-300"
              >
                <div className="font-semibold text-gray-800">Google (GOOGL)</div>
                <div className="text-sm text-gray-600">Scalping potential?</div>
              </button>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default AggressivePage;
