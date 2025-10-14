import React from 'react';
import { getCurrencySymbol } from '../utils/currency';

const AnalysisCard = ({ data }) => {
  if (!data || !data.success) {
    return (
      <div className="bg-red-50 border-l-4 border-red-500 p-6 rounded-lg">
        <div className="flex items-center">
          <div className="text-red-500 text-2xl mr-3">⚠️</div>
          <div>
            <h3 className="text-lg font-semibold text-red-800">Error</h3>
            <p className="text-red-600">{data?.error || 'Failed to analyze query'}</p>
          </div>
        </div>
        {data?.examples && (
          <div className="mt-4">
            <p className="text-sm text-gray-700 mb-2">Try queries like:</p>
            <ul className="text-sm text-gray-600 list-disc list-inside">
              {data.examples.slice(0, 3).map((example, idx) => (
                <li key={idx}>{example}</li>
              ))}
            </ul>
          </div>
        )}
      </div>
    );
  }

  const { 
    symbol, 
    company_name, 
    quote, 
    analysis, 
    news_sentiment, 
    news_articles,
    parsed_query,
    trading_plan 
  } = data;

  // Use currency from trading_plan if available, otherwise detect from symbol
  const currencySymbol = trading_plan?.currency?.symbol || getCurrencySymbol(symbol);
  const currencyCode = trading_plan?.currency?.code || (symbol.includes('.NS') || symbol.includes('.BO') ? 'INR' : 'USD');
  const recommendation = analysis?.recommendation || 'HOLD';
  const confidence = analysis?.confidence || 'MEDIUM';
  
  // Get recommendation color
  const getRecommendationColor = (rec) => {
    if (rec.includes('STRONG BUY') || rec === 'BUY') return 'bg-green-100 text-green-800 border-green-300';
    if (rec.includes('SELL')) return 'bg-red-100 text-red-800 border-red-300';
    return 'bg-yellow-100 text-yellow-800 border-yellow-300';
  };

  const getConfidenceColor = (conf) => {
    if (conf === 'VERY HIGH' || conf === 'HIGH') return 'text-green-600';
    if (conf === 'VERY LOW' || conf === 'LOW') return 'text-red-600';
    return 'text-yellow-600';
  };

  return (
    <div className="space-y-6">
      {/* Query Understanding */}
      <div className="bg-blue-50 border-l-4 border-blue-500 p-4 rounded-lg">
        <div className="flex items-start">
          <div className="text-blue-500 text-2xl mr-3">💬</div>
          <div className="flex-1">
            <h3 className="text-lg font-semibold text-blue-800 mb-2">Understanding Your Query</h3>
            <p className="text-gray-700 italic">"{parsed_query?.original}"</p>
            <div className="mt-3 grid grid-cols-2 gap-3 text-sm">
              <div>
                <span className="text-gray-600">Detected Stock:</span>
                <span className="ml-2 font-semibold text-gray-900">
                  {parsed_query?.detected_company || symbol} ({symbol})
                </span>
              </div>
              <div>
                <span className="text-gray-600">Intent:</span>
                <span className="ml-2 font-semibold text-gray-900 capitalize">
                  {parsed_query?.detected_intent}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Recommendation Card */}
      <div className={`border-2 p-6 rounded-lg ${getRecommendationColor(recommendation)}`}>
        <div className="flex items-center justify-between mb-4">
          <div>
            <h2 className="text-2xl font-bold">{recommendation}</h2>
            <p className="text-sm mt-1">
              Confidence: <span className={`font-semibold ${getConfidenceColor(confidence)}`}>{confidence}</span>
              {' '}({analysis?.confidence_score}/1.0)
            </p>
          </div>
          <div className="text-4xl">
            {analysis?.should_invest ? '✅' : '⚠️'}
          </div>
        </div>
        
        {/* Current Price Info */}
        <div className="bg-white bg-opacity-50 p-3 rounded mb-4">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <p className="text-sm text-gray-600">Current Price</p>
              <p className="text-xl font-bold">{currencySymbol}{quote?.price?.toFixed(2)}</p>
            </div>
            <div>
              <p className="text-sm text-gray-600">Daily Change</p>
              <p className={`text-xl font-bold ${quote?.change >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                {quote?.change >= 0 ? '+' : ''}{quote?.change?.toFixed(2)} ({quote?.change_percent})
              </p>
            </div>
          </div>
        </div>

        {/* Reasoning */}
        <div className="bg-white bg-opacity-50 p-4 rounded">
          <h3 className="font-semibold mb-2 flex items-center">
            <span className="text-lg mr-2">🧠</span> Analysis
          </h3>
          <p className="text-gray-700 leading-relaxed">{analysis?.reasoning}</p>
        </div>
      </div>

      {/* Trading Plan - NEW FEATURE */}
      {trading_plan && (
        <div className="bg-gradient-to-r from-indigo-50 to-purple-50 border-2 border-indigo-300 p-6 rounded-lg">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-xl font-semibold text-indigo-900 flex items-center">
              <span className="text-3xl mr-2">📋</span> {trading_plan.strategy} Trading Plan
            </h3>
            <span className={`px-3 py-1 rounded-full text-sm font-semibold ${
              trading_plan.risk_level === 'HIGH' ? 'bg-red-100 text-red-800' :
              trading_plan.risk_level === 'MEDIUM' ? 'bg-yellow-100 text-yellow-800' :
              'bg-green-100 text-green-800'
            }`}>
              {trading_plan.risk_level} RISK
            </span>
          </div>
          
          <p className="text-gray-600 mb-4">{trading_plan.description}</p>
          
          {/* Position Details */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
            <div className="bg-white p-4 rounded-lg shadow-sm">
              <p className="text-xs text-gray-500 mb-1">SHARES TO BUY</p>
              <p className="text-2xl font-bold text-indigo-900">{trading_plan.recommended_shares}</p>
            </div>
            <div className="bg-white p-4 rounded-lg shadow-sm">
              <p className="text-xs text-gray-500 mb-1">CAPITAL NEEDED</p>
              <p className="text-2xl font-bold text-indigo-900">{currencySymbol}{trading_plan.budget_required.toLocaleString()}</p>
              <p className="text-xs text-gray-500">{trading_plan.capital_used_pct}% of budget</p>
            </div>
            <div className="bg-white p-4 rounded-lg shadow-sm">
              <p className="text-xs text-gray-500 mb-1">POTENTIAL PROFIT</p>
              <p className="text-2xl font-bold text-green-600">+{currencySymbol}{trading_plan.potential_profit.toLocaleString()}</p>
            </div>
            <div className="bg-white p-4 rounded-lg shadow-sm">
              <p className="text-xs text-gray-500 mb-1">MAX LOSS</p>
              <p className="text-2xl font-bold text-red-600">-{currencySymbol}{trading_plan.potential_loss.toLocaleString()}</p>
            </div>
          </div>
          
          {/* Entry & Exit Prices */}
          <div className="grid md:grid-cols-3 gap-4 mb-4">
            <div className="bg-green-50 border-2 border-green-300 p-4 rounded-lg">
              <p className="text-sm font-semibold text-green-800 mb-2">💵 ENTRY PRICE</p>
              <p className="text-3xl font-bold text-green-900">{currencySymbol}{trading_plan.entry_price}</p>
              <p className="text-sm text-green-700 mt-2">{trading_plan.entry_timing}</p>
              <span className={`inline-block mt-2 px-2 py-1 rounded text-xs font-semibold ${
                trading_plan.entry_confidence === 'HIGH' || trading_plan.entry_confidence === 'VERY HIGH' ? 'bg-green-200 text-green-800' :
                trading_plan.entry_confidence === 'MEDIUM' ? 'bg-yellow-200 text-yellow-800' :
                'bg-red-200 text-red-800'
              }`}>
                {trading_plan.entry_confidence} CONFIDENCE
              </span>
            </div>
            
            <div className="bg-red-50 border-2 border-red-300 p-4 rounded-lg">
              <p className="text-sm font-semibold text-red-800 mb-2">🛑 STOP LOSS</p>
              <p className="text-3xl font-bold text-red-900">{currencySymbol}{trading_plan.stop_loss}</p>
              <p className="text-sm text-red-700 mt-2">
                Exit if price drops {((1 - trading_plan.stop_loss / trading_plan.entry_price) * 100).toFixed(1)}%
              </p>
              <p className="text-xs text-red-600 mt-2">⚠️ Use stop loss to protect capital</p>
            </div>
            
            <div className="bg-blue-50 border-2 border-blue-300 p-4 rounded-lg">
              <p className="text-sm font-semibold text-blue-800 mb-2">🎯 TARGET PRICE</p>
              <p className="text-3xl font-bold text-blue-900">{currencySymbol}{trading_plan.target_price}</p>
              <p className="text-sm text-blue-700 mt-2">
                Profit target: +{((trading_plan.target_price / trading_plan.entry_price - 1) * 100).toFixed(1)}%
              </p>
              <p className="text-xs text-blue-600 mt-2">Risk:Reward = {trading_plan.risk_reward_ratio}</p>
            </div>
          </div>
          
          {/* Timing & Exit Strategy */}
          <div className="bg-white p-4 rounded-lg shadow-sm">
            <div className="grid md:grid-cols-2 gap-4">
              <div>
                <p className="font-semibold text-gray-800 mb-2">⏰ WHEN TO EXIT:</p>
                <p className="text-gray-700">{trading_plan.exit_timing}</p>
              </div>
              <div>
                <p className="font-semibold text-gray-800 mb-2">⏳ HOLDING PERIOD:</p>
                <p className="text-gray-700">{trading_plan.holding_period}</p>
              </div>
            </div>
          </div>
          
          {/* Strategy Notes for Long-term */}
          {trading_plan.strategy_notes && (
            <div className="mt-4 bg-blue-50 p-4 rounded-lg">
              <p className="font-semibold text-blue-900 mb-2">📝 Strategy Notes:</p>
              <ul className="space-y-1">
                {trading_plan.strategy_notes.map((note, idx) => (
                  <li key={idx} className="text-sm text-blue-800">{note}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}

      {/* Investment Metrics */}
      {analysis?.investment_metrics && (
        <div className="bg-gradient-to-r from-purple-50 to-pink-50 border border-purple-200 p-6 rounded-lg">
          <h3 className="text-lg font-semibold text-purple-800 mb-4 flex items-center">
            <span className="text-2xl mr-2">💰</span> Investment Calculator
          </h3>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="bg-white p-3 rounded">
              <p className="text-sm text-gray-600">Quantity</p>
              <p className="text-xl font-bold text-gray-900">
                {analysis.investment_metrics.quantity} shares
              </p>
            </div>
            <div className="bg-white p-3 rounded">
              <p className="text-sm text-gray-600">Total Investment</p>
              <p className="text-xl font-bold text-gray-900">
                {currencySymbol}{analysis.investment_metrics.total_investment.toLocaleString()}
              </p>
            </div>
            <div className="bg-white p-3 rounded">
              <p className="text-sm text-gray-600">Predicted Value</p>
              <p className="text-xl font-bold text-gray-900">
                {currencySymbol}{analysis.investment_metrics.predicted_value.toLocaleString()}
              </p>
            </div>
            <div className="bg-white p-3 rounded">
              <p className="text-sm text-gray-600">Expected P&L</p>
              <p className={`text-xl font-bold ${analysis.investment_metrics.predicted_profit >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                {analysis.investment_metrics.predicted_profit >= 0 ? '+' : ''}
                {currencySymbol}{analysis.investment_metrics.predicted_profit.toLocaleString()}
                <span className="text-sm ml-1">
                  ({analysis.investment_metrics.predicted_return_pct >= 0 ? '+' : ''}
                  {analysis.investment_metrics.predicted_return_pct}%)
                </span>
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Scores Breakdown */}
      <div className="grid md:grid-cols-2 gap-4">
        <div className="bg-white border border-gray-200 p-5 rounded-lg">
          <h3 className="font-semibold text-gray-800 mb-3 flex items-center">
            <span className="text-xl mr-2">📊</span> Technical Score
          </h3>
          <div className="flex items-center">
            <div className="flex-1 bg-gray-200 rounded-full h-3">
              <div 
                className="bg-blue-500 h-3 rounded-full" 
                style={{ width: `${analysis?.technical_score * 100}%` }}
              ></div>
            </div>
            <span className="ml-3 font-bold text-gray-700">
              {(analysis?.technical_score * 100).toFixed(0)}%
            </span>
          </div>
        </div>

        <div className="bg-white border border-gray-200 p-5 rounded-lg">
          <h3 className="font-semibold text-gray-800 mb-3 flex items-center">
            <span className="text-xl mr-2">📰</span> Sentiment Score
          </h3>
          <div className="flex items-center">
            <div className="flex-1 bg-gray-200 rounded-full h-3">
              <div 
                className="bg-green-500 h-3 rounded-full" 
                style={{ width: `${analysis?.sentiment_score * 100}%` }}
              ></div>
            </div>
            <span className="ml-3 font-bold text-gray-700">
              {(analysis?.sentiment_score * 100).toFixed(0)}%
            </span>
          </div>
        </div>
      </div>

      {/* Growth Factors */}
      <div className="bg-green-50 border border-green-200 p-5 rounded-lg">
        <h3 className="text-lg font-semibold text-green-800 mb-3 flex items-center">
          <span className="text-2xl mr-2">📈</span> What's Making This Stock Grow?
        </h3>
        <ul className="space-y-2">
          {analysis?.growth_factors?.map((factor, idx) => (
            <li key={idx} className="flex items-start text-gray-700">
              <span className="mr-2 text-green-600">•</span>
              <span>{factor}</span>
            </li>
          ))}
        </ul>
      </div>

      {/* Risk Factors */}
      <div className="bg-orange-50 border border-orange-200 p-5 rounded-lg">
        <h3 className="text-lg font-semibold text-orange-800 mb-3 flex items-center">
          <span className="text-2xl mr-2">⚠️</span> Risk Factors to Consider
        </h3>
        <ul className="space-y-2">
          {analysis?.risk_factors?.map((factor, idx) => (
            <li key={idx} className="flex items-start text-gray-700">
              <span className="mr-2 text-orange-600">•</span>
              <span>{factor}</span>
            </li>
          ))}
        </ul>
      </div>

      {/* News Sentiment */}
      {news_sentiment && (
        <div className="bg-white border border-gray-200 p-5 rounded-lg">
          <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center">
            <span className="text-2xl mr-2">📰</span> Recent News Sentiment
          </h3>
          <div className="flex items-center justify-between mb-4 p-4 bg-gray-50 rounded">
            <div>
              <p className="text-sm text-gray-600">Overall Sentiment</p>
              <p className="text-xl font-bold capitalize flex items-center">
                <span className="text-2xl mr-2">{news_sentiment.emoji}</span>
                {news_sentiment.label}
              </p>
            </div>
            <div className="text-right">
              <p className="text-sm text-gray-600">Articles Analyzed</p>
              <p className="text-xl font-bold text-gray-900">{news_sentiment.article_count}</p>
              <p className="text-xs text-gray-500">
                {news_sentiment.positive_count} 📈 · {news_sentiment.neutral_count} ➡️ · {news_sentiment.negative_count} 📉
              </p>
            </div>
          </div>

          {/* News Articles */}
          {news_articles && news_articles.length > 0 && (
            <div className="space-y-3">
              <h4 className="font-semibold text-gray-700 text-sm">Recent Headlines:</h4>
              {news_articles.map((article, idx) => (
                <div key={idx} className="border-l-4 border-gray-300 pl-3 py-2">
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <a 
                        href={article.url} 
                        target="_blank" 
                        rel="noopener noreferrer"
                        className="text-blue-600 hover:text-blue-800 font-medium text-sm"
                      >
                        {article.title}
                      </a>
                      <p className="text-xs text-gray-600 mt-1">{article.source}</p>
                    </div>
                    <span className="text-xl ml-2">{article.sentiment?.emoji}</span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Portfolio Alignment */}
      {analysis?.portfolio_alignment && (
        <div className="bg-indigo-50 border border-indigo-200 p-4 rounded-lg">
          <p className="text-sm text-indigo-800">
            <span className="font-semibold">Portfolio Strategy:</span> {analysis.portfolio_alignment}
          </p>
        </div>
      )}
    </div>
  );
};

export default AnalysisCard;
