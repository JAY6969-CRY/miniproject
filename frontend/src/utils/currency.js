/**
 * Utility functions for currency detection and formatting
 */

/**
 * Detect if a stock symbol is from Indian exchanges (NSE/BSE)
 * @param {string} symbol - Stock symbol (e.g., "RELIANCE.NS", "AAPL")
 * @returns {boolean} - True if Indian stock, false otherwise
 */
export const isIndianStock = (symbol) => {
  if (!symbol) return false;
  return symbol.includes('.NS') || symbol.includes('.BO');
};

/**
 * Get currency symbol based on stock exchange
 * @param {string} symbol - Stock symbol
 * @returns {string} - Currency symbol (₹ or $)
 */
export const getCurrencySymbol = (symbol) => {
  return isIndianStock(symbol) ? '₹' : '$';
};

/**
 * Format price with appropriate currency symbol
 * @param {number} price - Price value
 * @param {string} symbol - Stock symbol
 * @param {number} decimals - Number of decimal places (default: 2)
 * @returns {string} - Formatted price string
 */
export const formatPrice = (price, symbol, decimals = 2) => {
  const currencySymbol = getCurrencySymbol(symbol);
  return `${currencySymbol}${price.toFixed(decimals)}`;
};

/**
 * Get exchange name from symbol
 * @param {string} symbol - Stock symbol
 * @returns {string} - Exchange name
 */
export const getExchangeName = (symbol) => {
  if (!symbol) return 'Unknown';
  if (symbol.includes('.NS')) return 'NSE (India)';
  if (symbol.includes('.BO')) return 'BSE (India)';
  return 'NASDAQ/NYSE (US)';
};

/**
 * Get currency code based on symbol
 * @param {string} symbol - Stock symbol
 * @returns {string} - Currency code (INR or USD)
 */
export const getCurrencyCode = (symbol) => {
  return isIndianStock(symbol) ? 'INR' : 'USD';
};
