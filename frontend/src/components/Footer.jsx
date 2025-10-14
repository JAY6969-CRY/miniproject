import React from 'react';

function Footer() {
  return (
    <footer className="bg-white border-t border-gray-200 mt-16">
      <div className="max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
        <div className="bg-yellow-50 border-l-4 border-yellow-400 p-4 mb-6">
          <div className="flex">
            <div className="flex-shrink-0">
              <svg className="h-5 w-5 text-yellow-400" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
              </svg>
            </div>
            <div className="ml-3">
              <h3 className="text-sm font-medium text-yellow-800">
                Important Disclaimer
              </h3>
              <div className="mt-2 text-sm text-yellow-700">
                <p>
                  This tool provides market forecasts based on historical data and technical analysis. 
                  All predictions are for <strong>informational purposes only</strong> and should not be 
                  considered as financial advice. Past performance does not guarantee future results. 
                  Please consult with a qualified financial advisor before making any investment decisions.
                </p>
              </div>
            </div>
          </div>
        </div>

        <div className="text-center text-sm text-gray-600">
          <p>
            © {new Date().getFullYear()} Stock Market Forecast. Built with FastAPI & React.
          </p>
          <p className="mt-2">
            Data sources: Alpha Vantage API & Yahoo Finance
          </p>
        </div>
      </div>
    </footer>
  );
}

export default Footer;
