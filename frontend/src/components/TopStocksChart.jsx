import React, { useState, useEffect } from 'react';
import { getTopStocks } from '../api';

function TopStocksChart({ region = 'US', onSelectStock }) {
  const [stocks, setStocks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedRegion, setSelectedRegion] = useState(region);

  useEffect(() => {
    fetchTopStocks();
  }, [selectedRegion]);

  const fetchTopStocks = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await getTopStocks(10, selectedRegion);
      if (data.success) {
        setStocks(data.stocks);
      }
    } catch (err) {
      setError('Failed to load top stocks');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const getSignalColor = (signal) => {
    switch (signal) {
      case 'STRONG BUY':
        return 'text-green-600 bg-green-100';
      case 'BUY':
        return 'text-green-600 bg-green-50';
      case 'STRONG SELL':
        return 'text-red-600 bg-red-100';
      case 'SELL':
        return 'text-red-600 bg-red-50';
      default:
        return 'text-gray-600 bg-gray-50';
    }
  };

  const getChangeColor = (change) => {
    if (change > 0) return 'text-green-600';
    if (change < 0) return 'text-red-600';
    return 'text-gray-600';
  };

  if (loading) {
    return (
      <div className="bg-white rounded-xl shadow-lg p-6">
        <div className="flex justify-center items-center py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-red-600"></div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-white rounded-xl shadow-lg p-6">
        <div className="text-center text-red-600 py-8">{error}</div>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-xl shadow-lg p-6">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <h2 className="text-2xl font-bold text-gray-800 flex items-center gap-2">
            <span className="text-3xl">🔥</span>
            Top Intraday Stocks
          </h2>
          <p className="text-sm text-gray-600 mt-1">
            High volume · High volatility · Best for day trading
          </p>
        </div>
        
        {/* Region Selector */}
        <div className="flex gap-2">
          <button
            onClick={() => setSelectedRegion('US')}
            className={`px-4 py-2 rounded-lg font-medium transition ${
              selectedRegion === 'US'
                ? 'bg-red-600 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            🇺🇸 US
          </button>
          <button
            onClick={() => setSelectedRegion('INDIA')}
            className={`px-4 py-2 rounded-lg font-medium transition ${
              selectedRegion === 'INDIA'
                ? 'bg-red-600 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            🇮🇳 India
          </button>
        </div>
      </div>

      {/* Stocks Table */}
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead>
            <tr className="border-b-2 border-gray-200">
              <th className="text-left py-3 px-2 font-semibold text-gray-700">Rank</th>
              <th className="text-left py-3 px-4 font-semibold text-gray-700">Stock</th>
              <th className="text-right py-3 px-4 font-semibold text-gray-700">Price</th>
              <th className="text-right py-3 px-4 font-semibold text-gray-700">Change</th>
              <th className="text-right py-3 px-4 font-semibold text-gray-700">Volume</th>
              <th className="text-right py-3 px-4 font-semibold text-gray-700">Volatility</th>
              <th className="text-center py-3 px-4 font-semibold text-gray-700">Signal</th>
              <th className="text-right py-3 px-4 font-semibold text-gray-700">Score</th>
              <th className="text-center py-3 px-2 font-semibold text-gray-700">Action</th>
            </tr>
          </thead>
          <tbody>
            {stocks.map((stock, index) => (
              <tr
                key={stock.symbol}
                className="border-b border-gray-100 hover:bg-red-50 transition cursor-pointer"
                onClick={() => onSelectStock && onSelectStock(stock.symbol)}
              >
                {/* Rank */}
                <td className="py-4 px-2">
                  <div className="flex items-center justify-center w-8 h-8 rounded-full bg-gradient-to-br from-red-500 to-orange-500 text-white font-bold text-sm">
                    {index + 1}
                  </div>
                </td>

                {/* Stock Name */}
                <td className="py-4 px-4">
                  <div>
                    <div className="font-semibold text-gray-800">{stock.symbol}</div>
                    <div className="text-xs text-gray-500 truncate max-w-[150px]">
                      {stock.company_name}
                    </div>
                  </div>
                </td>

                {/* Price */}
                <td className="py-4 px-4 text-right">
                  <div className="font-semibold text-gray-800">
                    {stock.symbol.includes('.NS') || stock.symbol.includes('.BO') ? '₹' : '$'}
                    {stock.current_price.toLocaleString()}
                  </div>
                </td>

                {/* Change */}
                <td className="py-4 px-4 text-right">
                  <div className={`font-semibold ${getChangeColor(stock.change_percent)}`}>
                    {stock.change_percent > 0 ? '+' : ''}
                    {stock.change_percent}%
                  </div>
                  <div className="text-xs text-gray-500">
                    {stock.momentum > 0 ? '↗' : '↘'} {Math.abs(stock.momentum).toFixed(1)}% 3d
                  </div>
                </td>

                {/* Volume */}
                <td className="py-4 px-4 text-right">
                  <div className="text-gray-800">
                    {(stock.volume / 1000000).toFixed(1)}M
                  </div>
                  <div className="text-xs text-gray-500">
                    {stock.volume_surge > 0 ? '+' : ''}
                    {stock.volume_surge.toFixed(0)}%
                  </div>
                </td>

                {/* Volatility */}
                <td className="py-4 px-4 text-right">
                  <div className="font-semibold text-orange-600">
                    {stock.volatility.toFixed(1)}%
                  </div>
                </td>

                {/* Signal */}
                <td className="py-4 px-4">
                  <div className="flex justify-center">
                    <span className={`px-3 py-1 rounded-full text-xs font-semibold ${getSignalColor(stock.signal)}`}>
                      {stock.signal}
                    </span>
                  </div>
                </td>

                {/* Trading Score */}
                <td className="py-4 px-4 text-right">
                  <div className="font-bold text-red-600 text-lg">
                    {stock.trading_score.toFixed(0)}
                  </div>
                </td>

                {/* Action */}
                <td className="py-4 px-2">
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      onSelectStock && onSelectStock(stock.symbol);
                    }}
                    className="px-3 py-1 bg-red-600 text-white rounded-lg hover:bg-red-700 transition text-sm font-medium"
                  >
                    Trade
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Legend */}
      <div className="mt-6 pt-4 border-t border-gray-200">
        <div className="flex flex-wrap gap-6 text-xs text-gray-600">
          <div>
            <span className="font-semibold">Score:</span> Trading suitability (higher = better)
          </div>
          <div>
            <span className="font-semibold">Volatility:</span> Average daily price range
          </div>
          <div>
            <span className="font-semibold">Volume Surge:</span> Today vs average
          </div>
          <div>
            <span className="font-semibold">3d:</span> 3-day momentum
          </div>
        </div>
      </div>

      {/* Last Updated */}
      {stocks.length > 0 && (
        <div className="mt-4 text-center text-xs text-gray-500">
          Last updated: {new Date(stocks[0].last_updated).toLocaleTimeString()}
          <button
            onClick={fetchTopStocks}
            className="ml-4 text-red-600 hover:text-red-700 font-medium"
          >
            🔄 Refresh
          </button>
        </div>
      )}
    </div>
  );
}

export default TopStocksChart;
