"""
Enhanced Trading Strategies with Budget-Based Position Sizing
Supports Intraday (Aggressive) and Long-Term Investment strategies
"""
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)

class TradingStrategy:
    """Calculate position sizes, entry/exit prices, and timing for different trading strategies"""
    
    def __init__(self):
        pass
    
    def _get_currency_info(self, symbol: str) -> Dict:
        """Get currency symbol and name based on stock symbol"""
        # Indian markets: NSE (.NS) and BSE (.BO)
        if symbol.endswith('.NS') or symbol.endswith('.BO'):
            return {'symbol': '₹', 'code': 'INR', 'name': 'Indian Rupee'}
        # Default to USD for US markets
        return {'symbol': '$', 'code': 'USD', 'name': 'US Dollar'}
    
    def calculate_position(
        self,
        symbol: str,
        strategy_type: str,  # 'aggressive' (intraday) or 'long_term'
        current_price: float,
        predicted_price: float,
        budget: float,
        rsi: float,
        technical_signal: str,
        volatility: float = None
    ) -> Dict:
        """
        Calculate position sizing and trading plan based on strategy
        
        Args:
            symbol: Stock symbol
            strategy_type: 'aggressive' for intraday, 'long_term' for investment
            current_price: Current stock price
            predicted_price: ML predicted price
            budget: Available budget for this trade
            rsi: RSI indicator value
            technical_signal: BUY/SELL/HOLD
            volatility: Price volatility (optional)
            
        Returns:
            Complete trading plan with entry/exit prices and position size
        """
        
        if strategy_type == 'aggressive':
            return self._calculate_intraday_position(
                symbol, current_price, predicted_price, budget, rsi, technical_signal
            )
        elif strategy_type == 'long_term':
            return self._calculate_longterm_position(
                symbol, current_price, predicted_price, budget, rsi, technical_signal
            )
        else:  # balanced
            return self._calculate_balanced_position(
                symbol, current_price, predicted_price, budget, rsi, technical_signal
            )
    
    def _calculate_intraday_position(
        self,
        symbol: str,
        current_price: float,
        predicted_price: float,
        budget: float,
        rsi: float,
        technical_signal: str
    ) -> Dict:
        """
        Aggressive/Intraday Strategy:
        - Quick trades (same day or 1-2 days)
        - Tight stop losses (1-2%)
        - Use up to 80-90% of provided budget
        - Higher position turnover
        """
        
        # For intraday, use up to 90% of budget (keep 10% buffer for price movements)
        max_position_size = budget * 0.90  # Use 90% of budget
        
        # Stop loss: 1.5% below entry
        stop_loss_pct = 0.015
        stop_loss_price = current_price * (1 - stop_loss_pct)
        
        # Target: 3-5% profit (3x risk-reward ratio)
        target_pct = 0.04  # 4% target
        target_price = current_price * (1 + target_pct)
        
        # Calculate position size based on budget
        # Maximum shares we can buy with available budget
        max_shares_affordable = int(max_position_size / current_price)
        
        # Risk management check: ensure we don't risk too much per share
        risk_per_share = current_price - stop_loss_price
        max_risk_amount = budget * 0.03  # Maximum 3% total risk
        max_shares_by_risk = int(max_risk_amount / risk_per_share) if risk_per_share > 0 else max_shares_affordable
        
        # Use the smaller of: what we can afford OR what risk allows
        # But prioritize using the budget if risk allows
        recommended_shares = min(max_shares_affordable, max_shares_by_risk) if max_shares_by_risk < max_shares_affordable else max_shares_affordable
        position_value = recommended_shares * current_price
        
        # Entry timing based on RSI
        if rsi < 35:
            entry_timing = "BUY NOW - Oversold"
            entry_confidence = "HIGH"
        elif rsi < 45:
            entry_timing = "BUY TODAY - Good entry"
            entry_confidence = "MEDIUM"
        elif rsi > 65:
            entry_timing = "WAIT - Overbought"
            entry_confidence = "LOW"
        else:
            entry_timing = "MONITOR - Neutral"
            entry_confidence = "MEDIUM"
        
        # Exit timing
        if technical_signal == "BUY":
            exit_timing = f"TARGET: {target_price:.2f} (4% gain) or END OF DAY"
            holding_period = "Intraday to 1-2 days"
        else:
            exit_timing = "DO NOT ENTER - Wait for better signal"
            holding_period = "N/A"
        
        currency = self._get_currency_info(symbol)
        
        return {
            'strategy': 'AGGRESSIVE (Intraday)',
            'description': 'Quick trades with tight risk management',
            'budget_required': round(position_value, 2),
            'recommended_shares': recommended_shares,
            'entry_price': round(current_price, 2),
            'stop_loss': round(stop_loss_price, 2),
            'target_price': round(target_price, 2),
            'risk_per_share': round(risk_per_share, 2),
            'potential_loss': round(recommended_shares * risk_per_share, 2),
            'potential_profit': round(recommended_shares * (target_price - current_price), 2),
            'risk_reward_ratio': '1:2.5',
            'entry_timing': entry_timing,
            'entry_confidence': entry_confidence,
            'exit_timing': exit_timing,
            'holding_period': holding_period,
            'risk_level': 'HIGH',
            'capital_used_pct': round((position_value / budget) * 100, 1) if budget > 0 else 0,
            'currency': currency
        }
    
    def _calculate_longterm_position(
        self,
        symbol: str,
        current_price: float,
        predicted_price: float,
        budget: float,
        rsi: float,
        technical_signal: str
    ) -> Dict:
        """
        Long-Term Investment Strategy:
        - Hold for weeks/months
        - Wider stop losses (8-10%)
        - Use up to 85% of provided budget (more conservative than intraday)
        - Focus on fundamentals
        """
        
        # For long-term, use up to 85% of budget (keep 15% buffer)
        max_position_size = budget * 0.85  # Use 85% of budget
        
        # Stop loss: 8% below entry (give room for volatility)
        stop_loss_pct = 0.08
        stop_loss_price = current_price * (1 - stop_loss_pct)
        
        # Target: 15-25% profit (long-term growth)
        target_pct = 0.20  # 20% target
        target_price = current_price * (1 + target_pct)
        
        # Calculate position size based on budget
        max_shares_affordable = int(max_position_size / current_price)
        
        # Risk management check
        risk_per_share = current_price - stop_loss_price
        max_risk_amount = budget * 0.07  # Maximum 7% total risk for long-term
        max_shares_by_risk = int(max_risk_amount / risk_per_share) if risk_per_share > 0 else max_shares_affordable
        
        # For long-term, prefer using the full budget if risk allows
        recommended_shares = min(max_shares_affordable, max_shares_by_risk) if max_shares_by_risk < max_shares_affordable else max_shares_affordable
        position_value = recommended_shares * current_price
        
        # Entry timing (more patient for long-term)
        if rsi < 40:
            entry_timing = "STRONG BUY - Accumulate position"
            entry_confidence = "VERY HIGH"
        elif rsi < 50:
            entry_timing = "BUY - Good long-term entry"
            entry_confidence = "HIGH"
        elif rsi < 60:
            entry_timing = "CONSIDER BUYING - Reasonable entry"
            entry_confidence = "MEDIUM"
        else:
            entry_timing = "WAIT FOR PULLBACK - Currently expensive"
            entry_confidence = "LOW"
        
        # Exit timing
        if technical_signal == "BUY":
            exit_timing = f"TARGET: {target_price:.2f} (20% gain) or HOLD 3-6 months"
            holding_period = "3-6 months minimum"
        elif technical_signal == "HOLD":
            exit_timing = f"HOLD for long-term growth, review quarterly"
            holding_period = "6-12 months"
        else:
            exit_timing = "AVOID - Wait for trend reversal"
            holding_period = "N/A"
        
        # Strategy-specific advice
        strategy_notes = [
            "✓ This is a long-term investment position",
            "✓ Don't panic on daily fluctuations",
            "✓ Review position quarterly",
            "✓ Consider averaging down on dips"
        ]
        
        currency = self._get_currency_info(symbol)
        
        return {
            'strategy': 'LONG-TERM (Investment)',
            'description': 'Buy and hold for sustained growth',
            'budget_required': round(position_value, 2),
            'recommended_shares': recommended_shares,
            'entry_price': round(current_price, 2),
            'stop_loss': round(stop_loss_price, 2),
            'target_price': round(target_price, 2),
            'risk_per_share': round(risk_per_share, 2),
            'potential_loss': round(recommended_shares * risk_per_share, 2),
            'potential_profit': round(recommended_shares * (target_price - current_price), 2),
            'risk_reward_ratio': '1:2.5',
            'entry_timing': entry_timing,
            'entry_confidence': entry_confidence,
            'exit_timing': exit_timing,
            'holding_period': holding_period,
            'risk_level': 'MEDIUM',
            'capital_used_pct': round((position_value / budget) * 100, 1) if budget > 0 else 0,
            'strategy_notes': strategy_notes,
            'currency': currency
        }
    
    def _calculate_balanced_position(
        self,
        symbol: str,
        current_price: float,
        predicted_price: float,
        budget: float,
        rsi: float,
        technical_signal: str
    ) -> Dict:
        """
        Balanced Strategy:
        - Hold for 1-4 weeks
        - Moderate stop losses (4-5%)
        - Use up to 80% of provided budget
        """
        
        # For balanced, use up to 80% of budget
        max_position_size = budget * 0.80  # Use 80% of budget
        
        # Stop loss: 5% below entry
        stop_loss_pct = 0.05
        stop_loss_price = current_price * (1 - stop_loss_pct)
        
        # Target: 10% profit
        target_pct = 0.10
        target_price = current_price * (1 + target_pct)
        
        # Calculate position size based on budget
        max_shares_affordable = int(max_position_size / current_price)
        
        # Risk management check
        risk_per_share = current_price - stop_loss_price
        max_risk_amount = budget * 0.05  # Maximum 5% total risk
        max_shares_by_risk = int(max_risk_amount / risk_per_share) if risk_per_share > 0 else max_shares_affordable
        
        # Use budget allocation if risk allows
        recommended_shares = min(max_shares_affordable, max_shares_by_risk) if max_shares_by_risk < max_shares_affordable else max_shares_affordable
        position_value = recommended_shares * current_price
        
        # Entry timing
        if rsi < 40:
            entry_timing = "BUY - Good entry point"
            entry_confidence = "HIGH"
        elif rsi < 55:
            entry_timing = "CONSIDER BUYING"
            entry_confidence = "MEDIUM"
        else:
            entry_timing = "WAIT - Monitor for dip"
            entry_confidence = "LOW"
        
        # Exit timing
        if technical_signal == "BUY":
            exit_timing = f"TARGET: {target_price:.2f} (10% gain) in 2-4 weeks"
            holding_period = "1-4 weeks"
        else:
            exit_timing = "MONITOR - Wait for clearer signal"
            holding_period = "2-4 weeks"
        
        currency = self._get_currency_info(symbol)
        
        return {
            'strategy': 'BALANCED (Swing)',
            'description': 'Medium-term position with balanced risk',
            'budget_required': round(position_value, 2),
            'recommended_shares': recommended_shares,
            'entry_price': round(current_price, 2),
            'stop_loss': round(stop_loss_price, 2),
            'target_price': round(target_price, 2),
            'risk_per_share': round(risk_per_share, 2),
            'potential_loss': round(recommended_shares * risk_per_share, 2),
            'potential_profit': round(recommended_shares * (target_price - current_price), 2),
            'risk_reward_ratio': '1:2',
            'entry_timing': entry_timing,
            'entry_confidence': entry_confidence,
            'exit_timing': exit_timing,
            'holding_period': holding_period,
            'risk_level': 'MEDIUM',
            'capital_used_pct': round((position_value / budget) * 100, 1) if budget > 0 else 0,
            'currency': currency
        }
