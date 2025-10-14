"""
Intelligent Stock Advisor
Combines technical analysis, news sentiment, and market data to provide recommendations
"""
from typing import Dict, List, Optional
from data_fetcher import DataFetcher
from predictor import Predictor
from news_analyzer import NewsAnalyzer
from trading_strategy import TradingStrategy
import logging

logger = logging.getLogger(__name__)

class StockAdvisor:
    """Provide intelligent stock investment advice"""
    
    def __init__(self):
        self.data_fetcher = DataFetcher()
        self.predictor = Predictor()
        self.news_analyzer = NewsAnalyzer()
        self.trading_strategy = TradingStrategy()
    
    def analyze_investment(
        self,
        symbol: str,
        company_name: str,
        user_intent: str = 'analyze',
        quantity: int = None,
        portfolio_type: str = 'balanced',
        budget: Optional[float] = None
    ) -> Dict:
        """
        Comprehensive investment analysis combining multiple factors
        
        Args:
            symbol: Stock symbol
            company_name: Company name
            user_intent: User's intent (buy/sell/hold/analyze)
            quantity: Number of shares to consider
            portfolio_type: Risk profile (aggressive/balanced/long_term)
            
        Returns:
            Comprehensive analysis with recommendation
        """
        try:
            # 1. Get current price and quote data
            quote = self.data_fetcher.get_quote(symbol)
            if not quote:
                return {
                    'success': False,
                    'error': f'Could not fetch data for {symbol}'
                }
            
            # 2. Get technical analysis and prediction
            prediction = self.predictor.predict_next_day(symbol)
            signal = self.predictor.generate_signal(symbol, portfolio_type)
            
            # 3. Get news and sentiment
            news_articles = self.news_analyzer.get_stock_news(symbol, company_name)
            news_sentiment = self.news_analyzer.get_overall_sentiment(news_articles)
            
            # 4. Calculate trading strategy if budget provided
            trading_plan = None
            if budget and budget > 0:
                trading_plan = self.trading_strategy.calculate_position(
                    symbol=symbol,
                    strategy_type=portfolio_type,
                    current_price=quote['price'],
                    predicted_price=prediction['predicted_price'],
                    budget=budget,
                    rsi=prediction['features']['rsi_14'],
                    technical_signal=signal['signal']
                )
            
            # 5. Generate comprehensive analysis
            analysis = self._generate_analysis(
                quote=quote,
                prediction=prediction,
                signal=signal,
                news_sentiment=news_sentiment,
                news_articles=news_articles,
                user_intent=user_intent,
                quantity=quantity,
                portfolio_type=portfolio_type,
                budget=budget
            )
            
            return {
                'success': True,
                'symbol': symbol,
                'company_name': company_name,
                'quote': quote,
                'prediction': prediction,
                'signal': signal,
                'news_sentiment': news_sentiment,
                'news_articles': news_articles[:3],  # Top 3 articles
                'analysis': analysis,
                'trading_plan': trading_plan
            }
            
        except Exception as e:
            logger.error(f"Error in investment analysis: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def _generate_analysis(
        self,
        quote: Dict,
        prediction: Dict,
        signal: Dict,
        news_sentiment: Dict,
        news_articles: List[Dict],
        user_intent: str,
        quantity: int,
        portfolio_type: str,
        budget: Optional[float] = None
    ) -> Dict:
        """Generate detailed investment analysis and recommendation"""
        
        current_price = quote.get('price', 0)
        predicted_price = prediction.get('predicted_price', 0)
        price_change_pct = prediction.get('change_percent', 0)
        
        technical_signal = signal.get('signal', 'HOLD')
        technical_confidence = signal.get('confidence', 'MEDIUM')
        
        news_label = news_sentiment.get('label', 'neutral')
        news_score = news_sentiment.get('score', 0)
        
        # Calculate scores for each factor
        technical_score = self._calculate_technical_score(technical_signal, technical_confidence, price_change_pct)
        sentiment_score = self._calculate_sentiment_score(news_label, news_score)
        
        # Combined score (60% technical, 40% sentiment)
        combined_score = (technical_score * 0.6) + (sentiment_score * 0.4)
        
        # Generate recommendation
        recommendation = self._get_recommendation(combined_score, user_intent)
        
        # Generate growth factors
        growth_factors = self._identify_growth_factors(
            technical_signal=technical_signal,
            price_change_pct=price_change_pct,
            news_sentiment=news_sentiment,
            signal_data=signal
        )
        
        # Generate risk factors
        risk_factors = self._identify_risk_factors(
            technical_signal=technical_signal,
            technical_confidence=technical_confidence,
            news_sentiment=news_sentiment,
            quote=quote
        )
        
        # Generate reasoning
        reasoning = self._generate_reasoning(
            recommendation=recommendation,
            technical_signal=technical_signal,
            news_sentiment=news_sentiment,
            price_change_pct=price_change_pct,
            growth_factors=growth_factors,
            risk_factors=risk_factors
        )
        
        # Calculate investment metrics if quantity provided
        investment_metrics = None
        if quantity and quantity > 0:
            investment_metrics = self._calculate_investment_metrics(
                quantity=quantity,
                current_price=current_price,
                predicted_price=predicted_price
            )
        
        return {
            'recommendation': recommendation,
            'confidence': self._get_confidence_label(combined_score),
            'confidence_score': round(combined_score, 2),
            'technical_score': round(technical_score, 2),
            'sentiment_score': round(sentiment_score, 2),
            'growth_factors': growth_factors,
            'risk_factors': risk_factors,
            'reasoning': reasoning,
            'investment_metrics': investment_metrics,
            'should_invest': combined_score > 0.5,
            'portfolio_alignment': self._check_portfolio_alignment(recommendation, portfolio_type)
        }
    
    def _calculate_technical_score(self, signal: str, confidence: str, price_change: float) -> float:
        """Calculate score from technical indicators"""
        # Base score from signal
        signal_scores = {'BUY': 0.8, 'SELL': 0.2, 'HOLD': 0.5}
        base_score = signal_scores.get(signal, 0.5)
        
        # Adjust for confidence
        confidence_multipliers = {'HIGH': 1.0, 'MEDIUM': 0.85, 'LOW': 0.7}
        confidence_mult = confidence_multipliers.get(confidence, 0.85)
        
        # Adjust for price change
        if price_change > 0:
            price_factor = min(price_change / 10, 0.2)  # Cap at 20%
        else:
            price_factor = max(price_change / 10, -0.2)
        
        score = (base_score * confidence_mult) + price_factor
        return max(0.0, min(1.0, score))  # Clamp between 0 and 1
    
    def _calculate_sentiment_score(self, label: str, score: float) -> float:
        """Calculate score from news sentiment"""
        # Normalize sentiment score (-1 to 1) to (0 to 1)
        normalized = (score + 1) / 2
        return max(0.0, min(1.0, normalized))
    
    def _get_recommendation(self, score: float, user_intent: str) -> str:
        """Get investment recommendation based on score"""
        if score >= 0.7:
            return 'STRONG BUY'
        elif score >= 0.55:
            return 'BUY'
        elif score >= 0.45:
            return 'HOLD'
        elif score >= 0.3:
            return 'SELL'
        else:
            return 'STRONG SELL'
    
    def _identify_growth_factors(
        self,
        technical_signal: str,
        price_change_pct: float,
        news_sentiment: Dict,
        signal_data: Dict
    ) -> List[str]:
        """Identify factors supporting growth"""
        factors = []
        
        # Technical factors
        if technical_signal == 'BUY':
            factors.append(f"📊 Technical indicators show BUY signal")
        
        if price_change_pct > 0:
            factors.append(f"📈 Predicted price increase of {abs(price_change_pct):.2f}%")
        
        # RSI factor
        rsi = signal_data.get('technical_indicators', {}).get('rsi')
        if rsi and rsi < 30:
            factors.append(f"💎 RSI at {rsi:.1f} indicates oversold condition (potential bounce)")
        elif rsi and 40 <= rsi <= 60:
            factors.append(f"⚖️ RSI at {rsi:.1f} shows balanced momentum")
        
        # News sentiment
        if news_sentiment.get('label') == 'positive':
            pos_count = news_sentiment.get('positive_count', 0)
            factors.append(f"📰 Positive news sentiment ({pos_count} positive articles)")
        
        # Volume
        if signal_data.get('technical_indicators', {}).get('volume_trend') == 'increasing':
            factors.append("📊 Increasing trading volume shows strong interest")
        
        if not factors:
            factors.append("ℹ️ Limited strong growth indicators at this time")
        
        return factors
    
    def _identify_risk_factors(
        self,
        technical_signal: str,
        technical_confidence: str,
        news_sentiment: Dict,
        quote: Dict
    ) -> List[str]:
        """Identify potential risks"""
        factors = []
        
        # Technical risks
        if technical_signal == 'SELL':
            factors.append("⚠️ Technical indicators show SELL signal")
        
        if technical_confidence == 'LOW':
            factors.append("⚠️ Low confidence in technical analysis")
        
        # Price volatility
        change_pct_str = quote.get('change_percent', '0%')
        try:
            change_pct = float(str(change_pct_str).replace('%', ''))
            if abs(change_pct) > 5:
                factors.append(f"⚠️ High volatility (daily change: {abs(change_pct):.2f}%)")
        except (ValueError, AttributeError):
            pass
        
        # News sentiment
        if news_sentiment.get('label') == 'negative':
            neg_count = news_sentiment.get('negative_count', 0)
            factors.append(f"⚠️ Negative news sentiment ({neg_count} negative articles)")
        
        if not factors:
            factors.append("✅ No major risk factors identified")
        
        return factors
    
    def _generate_reasoning(
        self,
        recommendation: str,
        technical_signal: str,
        news_sentiment: Dict,
        price_change_pct: float,
        growth_factors: List[str],
        risk_factors: List[str]
    ) -> str:
        """Generate human-readable reasoning for recommendation"""
        
        reasoning_parts = []
        
        # Introduction
        if recommendation in ['STRONG BUY', 'BUY']:
            reasoning_parts.append(f"✅ This stock shows positive signals for investment.")
        elif recommendation == 'HOLD':
            reasoning_parts.append(f"⚖️ This stock shows mixed signals. Consider holding or watching closely.")
        else:
            reasoning_parts.append(f"⚠️ This stock shows concerning signals. Exercise caution.")
        
        # Technical analysis
        if technical_signal == 'BUY':
            reasoning_parts.append(f"Technical analysis indicates a BUY opportunity with predicted upside of {abs(price_change_pct):.2f}%.")
        elif technical_signal == 'SELL':
            reasoning_parts.append(f"Technical analysis suggests caution with predicted movement of {price_change_pct:.2f}%.")
        else:
            reasoning_parts.append(f"Technical indicators suggest a neutral stance at current levels.")
        
        # News sentiment
        news_label = news_sentiment.get('label', 'neutral')
        if news_label == 'positive':
            reasoning_parts.append(f"Recent news sentiment is positive, suggesting favorable market perception.")
        elif news_label == 'negative':
            reasoning_parts.append(f"Recent news sentiment is negative, indicating potential headwinds.")
        else:
            reasoning_parts.append(f"News sentiment is neutral with no strong directional bias.")
        
        # Key factors
        if len(growth_factors) > 1:
            reasoning_parts.append(f"Key growth drivers include strong technical signals and positive momentum.")
        
        return " ".join(reasoning_parts)
    
    def _calculate_investment_metrics(
        self,
        quantity: int,
        current_price: float,
        predicted_price: float
    ) -> Dict:
        """Calculate investment metrics for given quantity"""
        total_investment = quantity * current_price
        predicted_value = quantity * predicted_price
        predicted_profit = predicted_value - total_investment
        predicted_return_pct = (predicted_profit / total_investment) * 100 if total_investment > 0 else 0
        
        return {
            'quantity': quantity,
            'current_price': round(current_price, 2),
            'predicted_price': round(predicted_price, 2),
            'total_investment': round(total_investment, 2),
            'predicted_value': round(predicted_value, 2),
            'predicted_profit': round(predicted_profit, 2),
            'predicted_return_pct': round(predicted_return_pct, 2)
        }
    
    def _get_confidence_label(self, score: float) -> str:
        """Convert confidence score to label"""
        if score >= 0.75:
            return 'VERY HIGH'
        elif score >= 0.60:
            return 'HIGH'
        elif score >= 0.45:
            return 'MEDIUM'
        elif score >= 0.30:
            return 'LOW'
        else:
            return 'VERY LOW'
    
    def _check_portfolio_alignment(self, recommendation: str, portfolio_type: str) -> str:
        """Check if recommendation aligns with portfolio strategy"""
        aggressive_aligned = ['STRONG BUY', 'BUY']
        balanced_aligned = ['BUY', 'HOLD']
        conservative_aligned = ['HOLD']
        
        if portfolio_type == 'aggressive':
            if recommendation in aggressive_aligned:
                return 'Well aligned with aggressive strategy'
            else:
                return 'May not suit aggressive strategy'
        elif portfolio_type == 'balanced':
            if recommendation in balanced_aligned:
                return 'Fits balanced portfolio approach'
            else:
                return 'Consider your balanced strategy goals'
        else:  # long_term
            if recommendation in conservative_aligned or 'BUY' in recommendation:
                return 'Suitable for long-term holding'
            else:
                return 'Evaluate against long-term objectives'
