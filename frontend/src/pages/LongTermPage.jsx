import React, { useState } from 'react';
import { analyzeQueryGemini, analyzeQuery } from '../api';
import SearchBar from '../components/SearchBar';
import AnalysisCard from '../components/AnalysisCard';

function LongTermPage() {
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
        analysis = await analyzeQueryGemini(searchQuery, 'long_term', budget);
      } catch (geminiError) {
        console.log('Gemini not available, using standard analyzer');
        analysis = await analyzeQuery(searchQuery, 'long_term', budget);
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

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 via-emerald-50 to-green-100">
      {/* Header */}
      <header className="bg-gradient-to-r from-green-600 to-emerald-600 shadow-lg">
        <div className="max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-4xl font-bold text-white flex items-center gap-3">
                <span className="text-5xl">📈</span>
                Long-Term Investment
              </h1>
              <p className="mt-2 text-lg text-green-100">
                Wealth building · 3-6 month holds · Growth focused
              </p>
            </div>
            <a
              href="/"
              className="px-6 py-3 bg-white text-green-600 rounded-lg font-semibold hover:bg-green-50 transition shadow-md"
            >
              ← Back to Home
            </a>
          </div>
        </div>
      </header>

      {/* Strategy Info Banner */}
      <div className="bg-white border-b-4 border-green-500 shadow-md">
        <div className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 text-center">
            <div className="p-4 bg-green-50 rounded-lg">
              <div className="text-2xl font-bold text-green-600">8%</div>
              <div className="text-sm text-gray-600">Stop Loss</div>
            </div>
            <div className="p-4 bg-emerald-50 rounded-lg">
              <div className="text-2xl font-bold text-emerald-600">20%</div>
              <div className="text-sm text-gray-600">Target Profit</div>
            </div>
            <div className="p-4 bg-green-50 rounded-lg">
              <div className="text-2xl font-bold text-green-600">3-6 Months</div>
              <div className="text-sm text-gray-600">Holding Period</div>
            </div>
            <div className="p-4 bg-emerald-50 rounded-lg">
              <div className="text-2xl font-bold text-emerald-600">25%</div>
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

        {/* Strategy Description */}
        {!symbol && !loading && (
          <div className="mb-8 bg-white rounded-xl shadow-lg p-8">
            <h2 className="text-2xl font-bold text-gray-800 mb-4 flex items-center gap-2">
              <span className="text-3xl">🎯</span>
              About Long-Term Investment
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <h3 className="font-semibold text-green-600 mb-2">✅ Best For:</h3>
                <ul className="space-y-2 text-gray-700">
                  <li>• Patient investors</li>
                  <li>• Retirement portfolios</li>
                  <li>• Wealth building goals</li>
                  <li>• Part-time investors</li>
                  <li>• Fundamental analysis lovers</li>
                </ul>
              </div>
              <div>
                <h3 className="font-semibold text-green-600 mb-2">💎 Advantages:</h3>
                <ul className="space-y-2 text-gray-700">
                  <li>• <strong>Lower risk</strong> - wider stops</li>
                  <li>• Less frequent monitoring needed</li>
                  <li>• Lower transaction costs</li>
                  <li>• Ride through volatility</li>
                  <li>• Capture major trends</li>
                </ul>
              </div>
            </div>
            <div className="mt-6 p-4 bg-green-50 rounded-lg border-l-4 border-green-500">
              <p className="text-sm text-gray-700">
                <strong>💡 Pro Tip:</strong> Focus on companies with strong fundamentals and growth potential. 
                Ignore daily volatility - check positions weekly. Add to winners on dips. 
                Target 20% gains but hold winners longer if trend continues.
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
            <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-green-600"></div>
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
              🌟 Try these investment opportunities:
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              <button
                onClick={() => handleSearch('Is Apple a good long-term investment?')}
                className="p-4 text-left bg-green-50 hover:bg-green-100 rounded-lg transition border-2 border-transparent hover:border-green-300"
              >
                <div className="font-semibold text-gray-800">Apple (AAPL)</div>
                <div className="text-sm text-gray-600">Long-term growth potential?</div>
              </button>
              <button
                onClick={() => handleSearch('Should I invest in Tesla for the long term?')}
                className="p-4 text-left bg-emerald-50 hover:bg-emerald-100 rounded-lg transition border-2 border-transparent hover:border-emerald-300"
              >
                <div className="font-semibold text-gray-800">Tesla (TSLA)</div>
                <div className="text-sm text-gray-600">EV sector investment?</div>
              </button>
              <button
                onClick={() => handleSearch('Can I hold Microsoft for 6 months?')}
                className="p-4 text-left bg-green-50 hover:bg-green-100 rounded-lg transition border-2 border-transparent hover:border-green-300"
              >
                <div className="font-semibold text-gray-800">Microsoft (MSFT)</div>
                <div className="text-sm text-gray-600">Tech sector hold?</div>
              </button>
              <button
                onClick={() => handleSearch('Is Reliance good for long term?')}
                className="p-4 text-left bg-emerald-50 hover:bg-emerald-100 rounded-lg transition border-2 border-transparent hover:border-emerald-300"
              >
                <div className="font-semibold text-gray-800">Reliance (RELIANCE.NS)</div>
                <div className="text-sm text-gray-600">Blue chip investment?</div>
              </button>
              <button
                onClick={() => handleSearch('Should I invest in TCS for 1 year?')}
                className="p-4 text-left bg-green-50 hover:bg-green-100 rounded-lg transition border-2 border-transparent hover:border-green-300"
              >
                <div className="font-semibold text-gray-800">TCS (TCS.NS)</div>
                <div className="text-sm text-gray-600">IT sector long-term?</div>
              </button>
              <button
                onClick={() => handleSearch('Is Google a buy and hold stock?')}
                className="p-4 text-left bg-emerald-50 hover:bg-emerald-100 rounded-lg transition border-2 border-transparent hover:border-emerald-300"
              >
                <div className="font-semibold text-gray-800">Google (GOOGL)</div>
                <div className="text-sm text-gray-600">Buy and hold potential?</div>
              </button>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default LongTermPage;
