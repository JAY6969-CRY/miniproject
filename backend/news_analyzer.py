"""
News Fetcher and Sentiment Analyzer
Fetches recent news about stocks and analyzes sentiment
"""
import requests
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from textblob import TextBlob
from config import settings
import logging

logger = logging.getLogger(__name__)

class NewsAnalyzer:
    """Fetch and analyze news sentiment for stocks"""
    
    def __init__(self):
        self.news_api_key = settings.NEWS_API_KEY
        self.news_api_url = "https://newsapi.org/v2/everything"
        
    def get_stock_news(self, symbol: str, company_name: str, days: int = 7) -> List[Dict]:
        """
        Fetch recent news about a stock
        
        Args:
            symbol: Stock symbol (e.g., AAPL, RELIANCE.NS)
            company_name: Company name for better search results
            days: Number of days to look back
            
        Returns:
            List of news articles with sentiment
        """
        try:
            # Clean symbol for search
            search_symbol = symbol.replace('.NS', '').replace('.BO', '')
            
            # Build search query
            query = f'"{company_name}" OR "{search_symbol}" stock'
            
            # Calculate date range
            to_date = datetime.now()
            from_date = to_date - timedelta(days=days)
            
            # Fetch news (with fallback if no API key)
            if not self.news_api_key or self.news_api_key == "":
                logger.warning("NEWS_API_KEY not set, using mock news")
                return self._get_mock_news(company_name)
            
            params = {
                'q': query,
                'from': from_date.strftime('%Y-%m-%d'),
                'to': to_date.strftime('%Y-%m-%d'),
                'language': 'en',
                'sortBy': 'relevancy',
                'pageSize': 10,
                'apiKey': self.news_api_key
            }
            
            response = requests.get(self.news_api_url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                articles = data.get('articles', [])
                return self._process_articles(articles)
            else:
                logger.error(f"News API error: {response.status_code}")
                return self._get_mock_news(company_name)
                
        except Exception as e:
            logger.error(f"Error fetching news: {str(e)}")
            return self._get_mock_news(company_name)
    
    def _process_articles(self, articles: List[Dict]) -> List[Dict]:
        """Process and analyze sentiment of articles"""
        processed = []
        
        for article in articles[:5]:  # Limit to top 5
            try:
                title = article.get('title', '')
                description = article.get('description', '') or ''
                content = f"{title}. {description}"
                
                # Analyze sentiment
                sentiment = self._analyze_sentiment(content)
                
                processed.append({
                    'title': title,
                    'description': description,
                    'url': article.get('url', ''),
                    'source': article.get('source', {}).get('name', 'Unknown'),
                    'published_at': article.get('publishedAt', ''),
                    'sentiment': sentiment
                })
            except Exception as e:
                logger.error(f"Error processing article: {str(e)}")
                continue
        
        return processed
    
    def _analyze_sentiment(self, text: str) -> Dict:
        """
        Analyze sentiment of text using TextBlob
        
        Returns:
            Dictionary with sentiment label and score
        """
        try:
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity  # -1 to 1
            
            # Classify sentiment
            if polarity > 0.1:
                label = 'positive'
                emoji = '📈'
            elif polarity < -0.1:
                label = 'negative'
                emoji = '📉'
            else:
                label = 'neutral'
                emoji = '➡️'
            
            return {
                'label': label,
                'score': round(polarity, 3),
                'emoji': emoji,
                'confidence': abs(polarity)
            }
        except Exception as e:
            logger.error(f"Sentiment analysis error: {str(e)}")
            return {
                'label': 'neutral',
                'score': 0.0,
                'emoji': '➡️',
                'confidence': 0.0
            }
    
    def get_overall_sentiment(self, articles: List[Dict]) -> Dict:
        """
        Calculate overall sentiment from multiple articles
        
        Returns:
            Aggregated sentiment with average score
        """
        if not articles:
            return {
                'label': 'neutral',
                'score': 0.0,
                'emoji': '➡️',
                'article_count': 0,
                'positive_count': 0,
                'negative_count': 0,
                'neutral_count': 0
            }
        
        scores = []
        positive_count = 0
        negative_count = 0
        neutral_count = 0
        
        for article in articles:
            sentiment = article.get('sentiment', {})
            score = sentiment.get('score', 0)
            scores.append(score)
            
            label = sentiment.get('label', 'neutral')
            if label == 'positive':
                positive_count += 1
            elif label == 'negative':
                negative_count += 1
            else:
                neutral_count += 1
        
        avg_score = sum(scores) / len(scores) if scores else 0.0
        
        # Determine overall label
        if avg_score > 0.1:
            label = 'positive'
            emoji = '📈'
        elif avg_score < -0.1:
            label = 'negative'
            emoji = '📉'
        else:
            label = 'neutral'
            emoji = '➡️'
        
        return {
            'label': label,
            'score': round(avg_score, 3),
            'emoji': emoji,
            'article_count': len(articles),
            'positive_count': positive_count,
            'negative_count': negative_count,
            'neutral_count': neutral_count
        }
    
    def _get_mock_news(self, company_name: str) -> List[Dict]:
        """Generate mock news when API is not available"""
        return [
            {
                'title': f'{company_name} Shows Strong Performance in Recent Quarter',
                'description': f'{company_name} reported better-than-expected earnings, showing resilience in challenging market conditions.',
                'url': '#',
                'source': 'Financial Times',
                'published_at': datetime.now().isoformat(),
                'sentiment': {
                    'label': 'positive',
                    'score': 0.5,
                    'emoji': '📈',
                    'confidence': 0.5
                }
            },
            {
                'title': f'{company_name} Faces Market Headwinds',
                'description': f'Analysts note that {company_name} may face challenges due to increased competition and market volatility.',
                'url': '#',
                'source': 'Bloomberg',
                'published_at': (datetime.now() - timedelta(days=1)).isoformat(),
                'sentiment': {
                    'label': 'neutral',
                    'score': 0.0,
                    'emoji': '➡️',
                    'confidence': 0.0
                }
            },
            {
                'title': f'{company_name} Announces Strategic Partnership',
                'description': f'{company_name} enters new partnership to expand market reach and drive innovation.',
                'url': '#',
                'source': 'Reuters',
                'published_at': (datetime.now() - timedelta(days=2)).isoformat(),
                'sentiment': {
                    'label': 'positive',
                    'score': 0.3,
                    'emoji': '📈',
                    'confidence': 0.3
                }
            }
        ]
