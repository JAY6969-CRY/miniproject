import React from 'react';

function SignalCard({ signal }) {
  // Detect if it's an Indian stock (NSE or BSE)
  const isIndianStock = signal.symbol && (signal.symbol.includes('.NS') || signal.symbol.includes('.BO'));
  const currencySymbol = isIndianStock ? '₹' : '$';
  
  const getSignalColor = () => {
    switch (signal.signal) {
      case 'BUY':
        return 'bg-green-50 border-green-500';
      case 'SELL':
        return 'bg-red-50 border-red-500';
      default:
        return 'bg-yellow-50 border-yellow-500';
    }
  };

  const getSignalTextColor = () => {
    switch (signal.signal) {
      case 'BUY':
        return 'text-green-700';
      case 'SELL':
        return 'text-red-700';
      default:
        return 'text-yellow-700';
    }
  };

  const getSignalIcon = () => {
    switch (signal.signal) {
      case 'BUY':
        return '📈';
      case 'SELL':
        return '📉';
      default:
        return '⏸️';
    }
  };

  const getConfidenceBadge = () => {
    const colors = {
      HIGH: 'bg-green-100 text-green-800',
      MEDIUM: 'bg-yellow-100 text-yellow-800',
      LOW: 'bg-gray-100 text-gray-800'
    };
    return colors[signal.confidence] || colors.MEDIUM;
  };

  return (
    <div className={`rounded-lg border-l-4 shadow-md p-6 ${getSignalColor()}`}>
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <div className="flex items-center space-x-3">
            <span className="text-3xl">{getSignalIcon()}</span>
            <div>
              <h2 className={`text-2xl font-bold ${getSignalTextColor()}`}>
                {signal.signal}
              </h2>
              <p className="text-sm text-gray-600 mt-1">
                Market Recommendation
              </p>
            </div>
          </div>

          <div className="mt-4 space-y-3">
            <div className="flex items-start space-x-2">
              <svg className="w-5 h-5 text-gray-500 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <p className="text-gray-700 text-sm flex-1">
                {signal.reason}
              </p>
            </div>

            <div className="flex items-start space-x-2">
              <svg className="w-5 h-5 text-gray-500 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <p className="text-gray-700 text-sm flex-1">
                <span className="font-medium">Timing:</span> {signal.timing}
              </p>
            </div>
          </div>
        </div>

        <div className="ml-4">
          <span className={`inline-block px-3 py-1 rounded-full text-xs font-medium ${getConfidenceBadge()}`}>
            {signal.confidence} Confidence
          </span>
        </div>
      </div>

      <div className="mt-6 pt-4 border-t border-gray-300">
        <div className="grid grid-cols-3 gap-4 text-center">
          <div>
            <p className="text-xs text-gray-600 mb-1">RSI (14)</p>
            <p className="text-lg font-semibold text-gray-900">
              {signal.technical_indicators.rsi_14.toFixed(1)}
            </p>
          </div>
          <div>
            <p className="text-xs text-gray-600 mb-1">SMA (5)</p>
            <p className="text-lg font-semibold text-gray-900">
              {currencySymbol}{signal.technical_indicators.sma_5.toFixed(2)}
            </p>
          </div>
          <div>
            <p className="text-xs text-gray-600 mb-1">SMA (10)</p>
            <p className="text-lg font-semibold text-gray-900">
              {currencySymbol}{signal.technical_indicators.sma_10.toFixed(2)}
            </p>
          </div>
        </div>
      </div>

      <div className="mt-4 text-xs text-gray-500 italic">
        Strategy: {signal.portfolio_type.replace('_', ' ').toUpperCase()}
      </div>
    </div>
  );
}

export default SignalCard;
