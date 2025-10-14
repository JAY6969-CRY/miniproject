import React from 'react';

function PriceCard({ title, price, symbol, quote, change, changePercent }) {
  const isPositive = change >= 0;
  const isPrediction = title.includes('Predicted');
  
  // Detect if it's an Indian stock (NSE or BSE)
  const isIndianStock = symbol && (symbol.includes('.NS') || symbol.includes('.BO'));
  const currencySymbol = isIndianStock ? '₹' : '$';

  return (
    <div className={`bg-white rounded-lg shadow-md p-6 card-shadow ${isPrediction ? 'border-2 border-blue-200' : ''}`}>
      <div className="flex items-center justify-between mb-2">
        <h3 className="text-sm font-medium text-gray-600">{title}</h3>
        {isPrediction && (
          <span className="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded-full font-medium">
            Next Day
          </span>
        )}
      </div>
      
      <div className="flex items-baseline justify-between">
        <div>
          <p className="text-3xl font-bold text-gray-900">
            {currencySymbol}{price.toFixed(2)}
          </p>
          {symbol && (
            <p className="text-sm text-gray-500 mt-1">{symbol}</p>
          )}
        </div>
        
        {changePercent !== undefined && (
          <div className={`text-right ${isPositive ? 'text-green-600' : 'text-red-600'}`}>
            <div className="flex items-center">
              {isPositive ? (
                <svg className="w-5 h-5 mr-1" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M5.293 9.707a1 1 0 010-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 01-1.414 1.414L11 7.414V15a1 1 0 11-2 0V7.414L6.707 9.707a1 1 0 01-1.414 0z" clipRule="evenodd" />
                </svg>
              ) : (
                <svg className="w-5 h-5 mr-1" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M14.707 10.293a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 111.414-1.414L9 12.586V5a1 1 0 012 0v7.586l2.293-2.293a1 1 0 011.414 0z" clipRule="evenodd" />
                </svg>
              )}
              <span className="font-semibold">
                {isPositive ? '+' : ''}{changePercent.toFixed(2)}%
              </span>
            </div>
            <p className="text-sm">
              {isPositive ? '+' : ''}{currencySymbol}{Math.abs(change).toFixed(2)}
            </p>
          </div>
        )}
      </div>
      
      {quote && (
        <div className="mt-4 pt-4 border-t border-gray-200">
          <div className="flex justify-between text-sm">
            <span className="text-gray-600">Volume:</span>
            <span className="font-medium text-gray-900">
              {quote.volume.toLocaleString()}
            </span>
          </div>
          <div className="flex justify-between text-sm mt-1">
            <span className="text-gray-600">Last Updated:</span>
            <span className="font-medium text-gray-900">
              {quote.latest_trading_day}
            </span>
          </div>
        </div>
      )}
    </div>
  );
}

export default PriceCard;
