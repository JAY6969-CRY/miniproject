"""
Stock Screener for Long-Term Investment Opportunities
Identifies high-quality stocks with strong fundamentals at attractive valuations
"""
import logging
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)

class StockScreener:
    """Screen stocks based on fundamental criteria for long-term investment"""
    
    # Sample data - Top quality stocks from screener.in analysis
    QUALITY_STOCKS = [
        {
            'name': 'IMEC Services',
            'symbol': 'IMEC.NS',
            'price': 229.65,
            'pe_ratio': 1.77,
            'market_cap': 43.63,
            'roce': 177.14,
            'roe': 90.98,
            'sales_growth_5y': 57.52,
            'eps_growth_5y': 822.72,
            'opm': 90.98,
            'debt_to_equity': 0.0,
            'sector': 'Services'
        },
        {
            'name': 'Tips Music',
            'symbol': 'TIPSMUSIC.NS',
            'price': 495.20,
            'pe_ratio': 36.42,
            'market_cap': 6332.16,
            'roce': 108.83,
            'roe': 65.14,
            'sales_growth_5y': 27.84,
            'eps_growth_5y': 74.26,
            'opm': 65.14,
            'debt_to_equity': 0.0,
            'sector': 'Media & Entertainment'
        },
        {
            'name': 'Stellant Security',
            'symbol': 'STELLANT.NS',
            'price': 368.20,
            'pe_ratio': 4.37,
            'market_cap': 136.32,
            'roce': 106.67,
            'roe': 94.96,
            'sales_growth_5y': 26.08,
            'eps_growth_5y': 38.36,
            'opm': 94.96,
            'debt_to_equity': 0.0,
            'sector': 'Security Services'
        },
        {
            'name': 'Waaree Renewable',
            'symbol': 'WAAREERENEWABLE.NS',
            'price': 1106.90,
            'pe_ratio': 32.66,
            'market_cap': 11534.45,
            'roce': 82.31,
            'roe': 21.39,
            'sales_growth_5y': 208.91,
            'eps_growth_5y': 142.45,
            'opm': 21.39,
            'debt_to_equity': 0.0,
            'sector': 'Renewable Energy'
        },
        {
            'name': 'Shilchar Technologies',
            'symbol': 'SHILCHAR.NS',
            'price': 4283.10,
            'pe_ratio': 27.60,
            'market_cap': 4899.95,
            'roce': 71.30,
            'roe': 30.79,
            'sales_growth_5y': 54.29,
            'eps_growth_5y': 151.28,
            'opm': 30.79,
            'debt_to_equity': 0.0,
            'sector': 'Technology'
        },
        {
            'name': 'Esab India',
            'symbol': 'ESABINDIA.NS',
            'price': 5553.60,
            'pe_ratio': 46.48,
            'market_cap': 8539.29,
            'roce': 70.03,
            'roe': 17.54,
            'sales_growth_5y': 14.50,
            'eps_growth_5y': 19.74,
            'opm': 17.54,
            'debt_to_equity': 0.0,
            'sector': 'Manufacturing'
        },
        {
            'name': 'Websol Energy',
            'symbol': 'WEBSOLENERGY.NS',
            'price': 115.70,
            'pe_ratio': 24.68,
            'market_cap': 5019.04,
            'roce': 59.25,
            'roe': 45.49,
            'sales_growth_5y': 24.10,
            'eps_growth_5y': 57.14,
            'opm': 45.49,
            'debt_to_equity': 0.0,
            'sector': 'Solar Energy'
        },
        {
            'name': 'Shakti Pumps',
            'symbol': 'SHAKTIPUMP.NS',
            'price': 701.75,
            'pe_ratio': 21.57,
            'market_cap': 8667.97,
            'roce': 55.31,
            'roe': 22.97,
            'sales_growth_5y': 45.73,
            'eps_growth_5y': 95.60,
            'opm': 22.97,
            'debt_to_equity': 0.0,
            'sector': 'Industrial'
        },
        {
            'name': 'CAMS Services',
            'symbol': 'CAMS.NS',
            'price': 3929.00,
            'pe_ratio': 44.22,
            'market_cap': 19458.17,
            'roce': 54.75,
            'roe': 45.55,
            'sales_growth_5y': 15.06,
            'eps_growth_5y': 21.63,
            'opm': 45.55,
            'debt_to_equity': 0.0,
            'sector': 'Financial Services'
        },
        {
            'name': 'Indian Energy Exchange',
            'symbol': 'IEX.NS',
            'price': 137.11,
            'pe_ratio': 27.18,
            'market_cap': 12226.00,
            'roce': 53.61,
            'roe': 85.11,
            'sales_growth_5y': 15.81,
            'eps_growth_5y': 19.98,
            'opm': 85.11,
            'debt_to_equity': 0.0,
            'sector': 'Power Exchange'
        },
        {
            'name': 'IRCTC',
            'symbol': 'IRCTC.NS',
            'price': 705.00,
            'pe_ratio': 42.17,
            'market_cap': 56395.99,
            'roce': 49.03,
            'roe': 33.42,
            'sales_growth_5y': 15.60,
            'eps_growth_5y': 20.04,
            'opm': 33.42,
            'debt_to_equity': 0.0,
            'sector': 'Travel & Tourism'
        },
        {
            'name': 'HDFC AMC',
            'symbol': 'HDFCAMC.NS',
            'price': 5392.00,
            'pe_ratio': 42.06,
            'market_cap': 115495.51,
            'roce': 43.33,
            'roe': 80.15,
            'sales_growth_5y': 13.77,
            'eps_growth_5y': 14.18,
            'opm': 80.15,
            'debt_to_equity': 0.0,
            'sector': 'Asset Management'
        },
        {
            'name': 'Mazagon Dock',
            'symbol': 'MAZDOCK.NS',
            'price': 2783.40,
            'pe_ratio': 48.12,
            'market_cap': 112306.88,
            'roce': 43.19,
            'roe': 16.03,
            'sales_growth_5y': 18.44,
            'eps_growth_5y': 38.30,
            'opm': 16.03,
            'debt_to_equity': 0.0,
            'sector': 'Defense'
        },
        {
            'name': 'Premier Energies',
            'symbol': 'PREMIERENERGIES.NS',
            'price': 994.10,
            'pe_ratio': 37.70,
            'market_cap': 45027.65,
            'roce': 41.12,
            'roe': 30.77,
            'sales_growth_5y': 47.08,
            'eps_growth_5y': 69.14,
            'opm': 30.77,
            'debt_to_equity': 0.0,
            'sector': 'Solar Energy'
        },
        {
            'name': 'Infosys',
            'symbol': 'INFY.NS',
            'price': 1541.10,
            'pe_ratio': 22.78,
            'market_cap': 640558.00,
            'roce': 37.50,
            'roe': 23.88,
            'sales_growth_5y': 12.41,
            'eps_growth_5y': 10.56,
            'opm': 23.88,
            'debt_to_equity': 0.0,
            'sector': 'IT Services'
        }
    ]
    
    def __init__(self):
        self.stocks = self.QUALITY_STOCKS.copy()
    
    def calculate_quality_score(self, stock: Dict) -> float:
        """
        Calculate a composite quality score (0-100)
        Weights: ROCE 25%, ROE 20%, Growth 30%, Valuation 25%
        """
        try:
            # ROCE Score (0-25): Higher is better, cap at 100%
            roce_score = min(stock['roce'] / 100 * 25, 25)
            
            # ROE Score (0-20): Higher is better, cap at 50%
            roe_score = min(stock['roe'] / 50 * 20, 20)
            
            # Growth Score (0-30): Average of sales and EPS growth
            avg_growth = (stock['sales_growth_5y'] + stock['eps_growth_5y']) / 2
            growth_score = min(avg_growth / 50 * 30, 30)  # Cap at 50% growth
            
            # Valuation Score (0-25): Lower P/E is better
            if stock['pe_ratio'] <= 15:
                valuation_score = 25
            elif stock['pe_ratio'] <= 25:
                valuation_score = 20
            elif stock['pe_ratio'] <= 35:
                valuation_score = 15
            elif stock['pe_ratio'] <= 45:
                valuation_score = 10
            else:
                valuation_score = 5
            
            total_score = roce_score + roe_score + growth_score + valuation_score
            return round(total_score, 1)
        except Exception as e:
            logger.error(f"Error calculating quality score: {e}")
            return 0.0
    
    def screen_stocks(
        self,
        min_roce: float = 40.0,
        min_roe: float = 15.0,
        min_sales_growth: float = 15.0,
        min_eps_growth: float = 15.0,
        max_pe: float = 50.0,
        max_debt_to_equity: float = 0.5,
        min_opm: float = 15.0,
        top_n: int = 10
    ) -> List[Dict]:
        """
        Screen stocks based on fundamental criteria
        
        Returns top N stocks sorted by quality score
        """
        filtered_stocks = []
        
        for stock in self.stocks:
            # Apply filters
            if (stock['roce'] >= min_roce and
                stock['roe'] >= min_roe and
                stock['sales_growth_5y'] >= min_sales_growth and
                stock['eps_growth_5y'] >= min_eps_growth and
                stock['pe_ratio'] <= max_pe and
                stock['debt_to_equity'] <= max_debt_to_equity and
                stock['opm'] >= min_opm):
                
                # Calculate quality score
                quality_score = self.calculate_quality_score(stock)
                
                # Add to results
                filtered_stocks.append({
                    **stock,
                    'quality_score': quality_score,
                    'recommendation': self._get_recommendation(quality_score, stock['pe_ratio'])
                })
        
        # Sort by quality score descending
        filtered_stocks.sort(key=lambda x: x['quality_score'], reverse=True)
        
        # Return top N
        return filtered_stocks[:top_n]
    
    def _get_recommendation(self, quality_score: float, pe_ratio: float) -> str:
        """Generate investment recommendation based on score and valuation"""
        if quality_score >= 75 and pe_ratio <= 25:
            return "STRONG BUY"
        elif quality_score >= 70 and pe_ratio <= 35:
            return "BUY"
        elif quality_score >= 60:
            return "ACCUMULATE"
        elif quality_score >= 50:
            return "HOLD & WATCH"
        else:
            return "RESEARCH MORE"
    
    def get_hidden_gems(self) -> Dict:
        """
        Get top hidden gems - quality stocks at attractive valuations
        """
        # Screen with specific criteria for hidden gems
        gems = self.screen_stocks(
            min_roce=40.0,
            min_roe=15.0,
            min_sales_growth=15.0,
            min_eps_growth=15.0,
            max_pe=50.0,
            max_debt_to_equity=0.5,
            min_opm=15.0,
            top_n=10
        )
        
        return {
            'success': True,
            'total_found': len(gems),
            'screening_criteria': {
                'min_roce': '40%',
                'min_roe': '15%',
                'min_sales_growth_5y': '15%',
                'min_eps_growth_5y': '15%',
                'max_pe_ratio': '50',
                'max_debt_to_equity': '0.5',
                'min_opm': '15%'
            },
            'stocks': gems,
            'description': 'High-quality stocks with strong fundamentals at attractive valuations for long-term wealth creation'
        }
