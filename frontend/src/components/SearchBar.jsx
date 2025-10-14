import React, { useState } from 'react';

function SearchBar({ onSearch, loading }) {
  const [input, setInput] = useState('');
  const [budget, setBudget] = useState('');
  const [showBudget, setShowBudget] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    const budgetValue = budget && !isNaN(budget) ? parseFloat(budget) : null;
    onSearch(input, budgetValue);
  };

  // Detect if query is for Indian market (NSE/BSE)
  const isIndianMarket = () => {
    const query = input.toLowerCase();
    // Check for .NS or .BO suffix (NSE/BSE)
    if (query.includes('.ns') || query.includes('.bo')) return true;
    // Check for Indian company keywords
    const indianKeywords = ['reliance', 'tcs', 'infosys', 'hdfc', 'icici', 'tata', 'wipro', 
                            'sbi', 'airtel', 'bajaj', 'kotak', 'larsen', 'asian paints', 
                            'maruti', 'sunpharma', 'titan', 'axis', 'adani', 'nse', 'bse', 'indian'];
    return indianKeywords.some(keyword => query.includes(keyword));
  };

  const getCurrencyInfo = () => {
    if (isIndianMarket()) {
      return { symbol: '₹', name: 'INR', placeholder: '50000' };
    }
    return { symbol: '$', name: 'USD', placeholder: '5000' };
  };

  const currency = getCurrencyInfo();

  const exampleQueries = [
    "Can I invest in Apple today?",
    "Should I buy Tesla stock?",
    "Is Reliance a good investment?",
    "AAPL",
    "RELIANCE.NS"
  ];

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <div className="mb-4">
        <h2 className="text-lg font-semibold text-gray-800 mb-2">
          🤖 Ask in Plain English or Use Stock Symbol
        </h2>
        <p className="text-sm text-gray-600">
          Try asking: "Should I invest in Apple?" or simply enter "AAPL"
        </p>
      </div>
      
      <form onSubmit={handleSubmit} className="space-y-3">
        <div className="flex flex-col sm:flex-row gap-4">
          <div className="flex-1">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask: 'Can I invest in Apple today?' or enter 'AAPL'"
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent text-base"
              disabled={loading}
            />
          </div>
          <button
            type="submit"
            disabled={loading}
            className="px-8 py-3 bg-gradient-to-r from-blue-600 to-indigo-600 text-white font-medium rounded-lg hover:from-blue-700 hover:to-indigo-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition transform hover:scale-105"
          >
            {loading ? (
              <span className="flex items-center">
                <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Analyzing...
              </span>
            ) : (
              '🔍 Analyze'
            )}
          </button>
        </div>
        
        {/* Budget Input Toggle */}
        <div className="flex items-center gap-2">
          <button
            type="button"
            onClick={() => setShowBudget(!showBudget)}
            className="text-sm text-blue-600 hover:text-blue-700 font-medium"
          >
            {showBudget ? '− Hide' : '+ Add'} Budget (Get Trading Plan)
          </button>
        </div>
        
        {/* Budget Input Field */}
        {showBudget && (
          <div className="flex items-center gap-3 bg-blue-50 p-3 rounded-lg">
            <label className="text-sm font-medium text-gray-700">Budget ({currency.symbol}):</label>
            <div className="relative">
              <span className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-500 font-medium">
                {currency.symbol}
              </span>
              <input
                type="number"
                value={budget}
                onChange={(e) => setBudget(e.target.value)}
                placeholder={currency.placeholder}
                min="0"
                step="100"
                className="pl-8 pr-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 w-40"
                disabled={loading}
              />
            </div>
            <span className="text-xs text-gray-500 bg-white px-2 py-1 rounded border border-gray-200">
              {isIndianMarket() ? '🇮🇳 Indian Market' : '🇺🇸 US Market'}
            </span>
            <span className="text-sm text-gray-600">
              💡 Enter your budget to get position sizing, entry/exit prices, and timing
            </span>
          </div>
        )}
      </form>
      
      <div className="mt-4 flex flex-wrap gap-2">
        <span className="text-xs text-gray-500 self-center">Quick try:</span>
        {exampleQueries.map((query, idx) => (
          <button
            key={idx}
            onClick={() => setInput(query)}
            className="px-3 py-1 text-xs bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-full transition"
            disabled={loading}
          >
            {query}
          </button>
        ))}
      </div>
    </div>
  );
}

export default SearchBar;
