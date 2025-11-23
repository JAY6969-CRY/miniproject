import React from 'react';

function HiddenGemsCard({ data, onAnalyzeStock }) {
  if (!data || !data.stocks || data.stocks.length === 0) {
    return null;
  }

  const getRecommendationColor = (recommendation) => {
    switch (recommendation) {
      case 'STRONG BUY':
        return 'bg-green-100 text-green-800 border-green-300';
      case 'BUY':
        return 'bg-emerald-100 text-emerald-800 border-emerald-300';
      case 'ACCUMULATE':
        return 'bg-blue-100 text-blue-800 border-blue-300';
      case 'HOLD & WATCH':
        return 'bg-yellow-100 text-yellow-800 border-yellow-300';
      default:
        return 'bg-gray-100 text-gray-800 border-gray-300';
    }
  };

  const getScoreColor = (score) => {
    if (score >= 75) return 'text-green-600 font-bold';
    if (score >= 65) return 'text-emerald-600 font-semibold';
    if (score >= 55) return 'text-blue-600';
    return 'text-gray-600';
  };

  return (
    <div className="bg-white rounded-xl shadow-lg p-8 mb-8">
      {/* Header */}
      <div className="mb-6">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-3xl font-bold text-gray-800 flex items-center gap-3">
            <span className="text-4xl">💎</span>
            Hidden Gems - Quality Stocks
          </h2>
          <div className="px-4 py-2 bg-green-50 rounded-lg border-2 border-green-200">
            <span className="text-sm text-gray-600">Found: </span>
            <span className="text-xl font-bold text-green-600">{data.total_found}</span>
          </div>
        </div>
        <p className="text-gray-600 text-lg mb-4">{data.description}</p>
        
        {/* Screening Criteria */}
        <div className="bg-gradient-to-r from-green-50 to-emerald-50 rounded-lg p-4 border-l-4 border-green-500">
          <h3 className="font-semibold text-gray-800 mb-2 flex items-center gap-2">
            <span>🎯</span>
            Screening Criteria Applied:
          </h3>
          <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-7 gap-3 text-sm">
            <div className="bg-white px-3 py-2 rounded shadow-sm">
              <div className="text-gray-500 text-xs">ROCE</div>
              <div className="font-bold text-green-600">≥ {data.screening_criteria.min_roce}</div>
            </div>
            <div className="bg-white px-3 py-2 rounded shadow-sm">
              <div className="text-gray-500 text-xs">ROE</div>
              <div className="font-bold text-green-600">≥ {data.screening_criteria.min_roe}</div>
            </div>
            <div className="bg-white px-3 py-2 rounded shadow-sm">
              <div className="text-gray-500 text-xs">Sales Growth</div>
              <div className="font-bold text-green-600">≥ {data.screening_criteria.min_sales_growth_5y}</div>
            </div>
            <div className="bg-white px-3 py-2 rounded shadow-sm">
              <div className="text-gray-500 text-xs">EPS Growth</div>
              <div className="font-bold text-green-600">≥ {data.screening_criteria.min_eps_growth_5y}</div>
            </div>
            <div className="bg-white px-3 py-2 rounded shadow-sm">
              <div className="text-gray-500 text-xs">P/E Ratio</div>
              <div className="font-bold text-blue-600">≤ {data.screening_criteria.max_pe_ratio}</div>
            </div>
            <div className="bg-white px-3 py-2 rounded shadow-sm">
              <div className="text-gray-500 text-xs">Debt/Equity</div>
              <div className="font-bold text-blue-600">≤ {data.screening_criteria.max_debt_to_equity}</div>
            </div>
            <div className="bg-white px-3 py-2 rounded shadow-sm">
              <div className="text-gray-500 text-xs">OPM</div>
              <div className="font-bold text-green-600">≥ {data.screening_criteria.min_opm}</div>
            </div>
          </div>
        </div>
      </div>

      {/* Stocks Table */}
      <div className="overflow-x-auto">
        <table className="min-w-full">
          <thead>
            <tr className="bg-gradient-to-r from-green-100 to-emerald-100 border-b-2 border-green-300">
              <th className="px-4 py-3 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider">
                Rank
              </th>
              <th className="px-4 py-3 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider">
                Company
              </th>
              <th className="px-4 py-3 text-right text-xs font-semibold text-gray-700 uppercase tracking-wider">
                Price (₹)
              </th>
              <th className="px-4 py-3 text-right text-xs font-semibold text-gray-700 uppercase tracking-wider">
                P/E
              </th>
              <th className="px-4 py-3 text-right text-xs font-semibold text-gray-700 uppercase tracking-wider">
                Quality Score
              </th>
              <th className="px-4 py-3 text-right text-xs font-semibold text-gray-700 uppercase tracking-wider">
                ROCE %
              </th>
              <th className="px-4 py-3 text-right text-xs font-semibold text-gray-700 uppercase tracking-wider">
                ROE %
              </th>
              <th className="px-4 py-3 text-right text-xs font-semibold text-gray-700 uppercase tracking-wider">
                Sales Growth 5Y %
              </th>
              <th className="px-4 py-3 text-right text-xs font-semibold text-gray-700 uppercase tracking-wider">
                EPS Growth 5Y %
              </th>
              <th className="px-4 py-3 text-center text-xs font-semibold text-gray-700 uppercase tracking-wider">
                Recommendation
              </th>
              <th className="px-4 py-3 text-center text-xs font-semibold text-gray-700 uppercase tracking-wider">
                Action
              </th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {data.stocks.map((stock, index) => (
              <tr 
                key={stock.symbol} 
                className="hover:bg-green-50 transition-colors duration-150"
              >
                <td className="px-4 py-4 whitespace-nowrap">
                  <div className="flex items-center">
                    {index === 0 && <span className="text-2xl mr-2">🥇</span>}
                    {index === 1 && <span className="text-2xl mr-2">🥈</span>}
                    {index === 2 && <span className="text-2xl mr-2">🥉</span>}
                    <span className="text-sm font-semibold text-gray-700">#{index + 1}</span>
                  </div>
                </td>
                <td className="px-4 py-4">
                  <div className="text-sm font-semibold text-gray-900">{stock.name}</div>
                  <div className="text-xs text-gray-500">{stock.sector}</div>
                </td>
                <td className="px-4 py-4 whitespace-nowrap text-right">
                  <div className="text-sm font-bold text-gray-900">₹{stock.price.toFixed(2)}</div>
                </td>
                <td className="px-4 py-4 whitespace-nowrap text-right">
                  <div className="text-sm text-gray-700">{stock.pe_ratio.toFixed(2)}</div>
                </td>
                <td className="px-4 py-4 whitespace-nowrap text-right">
                  <div className={`text-lg font-bold ${getScoreColor(stock.quality_score)}`}>
                    {stock.quality_score}/100
                  </div>
                </td>
                <td className="px-4 py-4 whitespace-nowrap text-right">
                  <div className="text-sm font-semibold text-green-600">{stock.roce.toFixed(1)}%</div>
                </td>
                <td className="px-4 py-4 whitespace-nowrap text-right">
                  <div className="text-sm font-semibold text-green-600">{stock.roe.toFixed(1)}%</div>
                </td>
                <td className="px-4 py-4 whitespace-nowrap text-right">
                  <div className="text-sm font-semibold text-blue-600">{stock.sales_growth_5y.toFixed(1)}%</div>
                </td>
                <td className="px-4 py-4 whitespace-nowrap text-right">
                  <div className="text-sm font-semibold text-blue-600">{stock.eps_growth_5y.toFixed(1)}%</div>
                </td>
                <td className="px-4 py-4 whitespace-nowrap text-center">
                  <span className={`px-3 py-1 inline-flex text-xs leading-5 font-semibold rounded-full border-2 ${getRecommendationColor(stock.recommendation)}`}>
                    {stock.recommendation}
                  </span>
                </td>
                <td className="px-4 py-4 whitespace-nowrap text-center">
                  <button
                    onClick={() => onAnalyzeStock(stock.name)}
                    className="px-4 py-2 bg-gradient-to-r from-green-600 to-emerald-600 text-white text-xs font-semibold rounded-lg hover:from-green-700 hover:to-emerald-700 transition-all shadow-md hover:shadow-lg"
                  >
                    Analyze
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Footer Note */}
      <div className="mt-6 p-4 bg-blue-50 rounded-lg border-l-4 border-blue-500">
        <p className="text-sm text-gray-700">
          <strong>📊 Quality Score Methodology:</strong> Composite score based on ROCE (25%), ROE (20%), 
          Growth Metrics (30%), and Valuation (25%). Higher scores indicate better quality businesses at 
          attractive valuations.
        </p>
      </div>
    </div>
  );
}

export default HiddenGemsCard;
