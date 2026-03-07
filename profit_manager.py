"""
Profit management module for converting profits to stablecoins and timing base currency re-entries
"""

import logging
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class ProfitManager:
    """Manages profit conversion to USDC and base currency market timing"""
    
    def __init__(self, w3, config: Dict):
        self.w3 = w3
        self.config = config
        self.usdc_balance = 0.0  # Track USDC balance
        self.base_currency_prices: List[Dict] = []  # Historical base currency prices
        self.conversion_history: List[Dict] = []  # Track all conversions
        # Resolve chain_id from config: prefer active wallet chain, fall back to first wallet
        wallets = config.get('wallets', [])
        self._chain_id = wallets[0].get('chain_id', 1) if wallets else 1

    def get_base_currency_name(self) -> str:
        """Get the name of the base currency (ETH, SOL, BNB, etc.)"""
        chain_id = self._chain_id
        
        # Map chain IDs to currency names
        chain_map = {
            1: 'ETH',      # Ethereum Mainnet
            56: 'BNB',     # BSC
            137: 'MATIC',  # Polygon
            43114: 'AVAX', # Avalanche
            250: 'FTM',    # Fantom
            42161: 'ETH',  # Arbitrum
            10: 'ETH',     # Optimism
        }
        
        return chain_map.get(chain_id, 'ETH')
        
    def get_base_currency_price(self) -> float:
        """
        Get current price of base currency in USD
        Returns price in USD
        """
        try:
            base_currency = self.get_base_currency_name()
            
            # In a real implementation, this would:
            # 1. Query price oracle (Chainlink, etc.)
            # 2. Query DEX for base/USDC pair
            # 3. Query external API (CoinGecko, etc.)
            
            logger.info(f"Getting {base_currency} price in USD")
            
            # Placeholder - return a sample price
            prices = {
                'ETH': 3000.0,
                'BNB': 300.0,
                'MATIC': 0.80,
                'AVAX': 35.0,
                'FTM': 0.50,
            }
            
            return prices.get(base_currency, 3000.0)
            
        except Exception as e:
            logger.error(f"Error getting base currency price: {e}")
            return 0.0
            
    def record_base_currency_price(self):
        """Record current base currency price for trend analysis"""
        try:
            price = self.get_base_currency_price()
            base_currency = self.get_base_currency_name()
            
            self.base_currency_prices.append({
                'timestamp': datetime.now().isoformat(),
                'currency': base_currency,
                'price_usd': price
            })
            
            # Keep only last 100 prices to avoid memory issues
            if len(self.base_currency_prices) > 100:
                self.base_currency_prices = self.base_currency_prices[-100:]
                
        except Exception as e:
            logger.error(f"Error recording base currency price: {e}")
            
    def convert_to_usdc(self, base_amount: float, reason: str = "profit_taking") -> Dict:
        """
        Convert base currency (ETH, SOL, etc.) to USDC
        Returns conversion result
        """
        logger.info(f"Converting {base_amount} {self.get_base_currency_name()} to USDC")
        
        try:
            base_currency = self.get_base_currency_name()
            current_price = self.get_base_currency_price()
            
            # Calculate USDC received
            usdc_received = base_amount * current_price
            
            # In a real implementation, this would:
            # 1. Build swap transaction (base -> USDC)
            # 2. Calculate slippage
            # 3. Execute swap on DEX
            # 4. Wait for confirmation
            
            # Update balance
            self.usdc_balance += usdc_received
            
            # Record conversion
            conversion = {
                'timestamp': datetime.now().isoformat(),
                'type': 'to_usdc',
                'reason': reason,
                'base_currency': base_currency,
                'base_amount': base_amount,
                'base_price': current_price,
                'usdc_received': usdc_received,
                'success': True
            }
            
            self.conversion_history.append(conversion)
            
            logger.info(f"✅ Converted {base_amount:.6f} {base_currency} to {usdc_received:.2f} USDC at ${current_price:.2f}")
            
            return conversion
            
        except Exception as e:
            logger.error(f"Error converting to USDC: {e}")
            return {'success': False, 'error': str(e)}
            
    def convert_to_base_currency(self, usdc_amount: float, reason: str = "market_opportunity") -> Dict:
        """
        Convert USDC to base currency (ETH, SOL, etc.)
        Returns conversion result
        """
        logger.info(f"Converting {usdc_amount} USDC to {self.get_base_currency_name()}")
        
        try:
            base_currency = self.get_base_currency_name()
            current_price = self.get_base_currency_price()
            
            # Check if we have enough USDC
            if usdc_amount > self.usdc_balance:
                logger.error(f"Insufficient USDC balance: {self.usdc_balance:.2f} < {usdc_amount:.2f}")
                return {'success': False, 'error': 'Insufficient USDC balance'}
            
            # Calculate base currency received
            base_received = usdc_amount / current_price
            
            # In a real implementation, this would:
            # 1. Build swap transaction (USDC -> base)
            # 2. Calculate slippage
            # 3. Execute swap on DEX
            # 4. Wait for confirmation
            
            # Update balance
            self.usdc_balance -= usdc_amount
            
            # Record conversion
            conversion = {
                'timestamp': datetime.now().isoformat(),
                'type': 'to_base',
                'reason': reason,
                'base_currency': base_currency,
                'usdc_amount': usdc_amount,
                'base_price': current_price,
                'base_received': base_received,
                'success': True
            }
            
            self.conversion_history.append(conversion)
            
            logger.info(f"✅ Converted {usdc_amount:.2f} USDC to {base_received:.6f} {base_currency} at ${current_price:.2f}")
            
            return conversion
            
        except Exception as e:
            logger.error(f"Error converting to base currency: {e}")
            return {'success': False, 'error': str(e)}
            
    def calculate_base_currency_trend(self) -> Dict:
        """
        Analyze base currency price trend
        Returns trend analysis
        """
        if len(self.base_currency_prices) < 2:
            return {
                'trend': 'unknown',
                'change_percent': 0,
                'current_price': self.get_base_currency_price()
            }
            
        try:
            # Get recent prices
            recent_prices = [p['price_usd'] for p in self.base_currency_prices[-10:]]
            current_price = recent_prices[-1]
            
            # Calculate price change
            if len(recent_prices) >= 10:
                old_price = recent_prices[0]
            else:
                old_price = recent_prices[0]
                
            change_percent = ((current_price - old_price) / old_price) * 100
            
            # Determine trend
            if change_percent > 2:
                trend = 'up'
            elif change_percent < -2:
                trend = 'down'
            else:
                trend = 'sideways'
                
            return {
                'trend': trend,
                'change_percent': change_percent,
                'current_price': current_price,
                'old_price': old_price
            }
            
        except Exception as e:
            logger.error(f"Error calculating trend: {e}")
            return {
                'trend': 'unknown',
                'change_percent': 0,
                'current_price': self.get_base_currency_price()
            }
            
    def is_good_time_to_buy_base(self) -> Tuple[bool, str]:
        """
        Determine if it's a good time to buy base currency
        Returns (should_buy, reason)
        """
        try:
            # Need minimum price history
            if len(self.base_currency_prices) < 10:
                return False, "Insufficient price history"
                
            base_currency = self.get_base_currency_name()
            trend = self.calculate_base_currency_trend()
            current_price = trend['current_price']
            
            # Get price statistics
            recent_prices = [p['price_usd'] for p in self.base_currency_prices[-50:]]
            avg_price = sum(recent_prices) / len(recent_prices)
            max_price = max(recent_prices)
            min_price = min(recent_prices)
            
            # Calculate position in range
            price_range = max_price - min_price
            if price_range == 0:
                return False, "No price movement"
                
            position_in_range = (current_price - min_price) / price_range
            
            # Get configuration
            buy_dip_threshold = self.config['profit_management']['buy_base_dip_threshold_percent']
            buy_below_avg_threshold = self.config['profit_management']['buy_base_below_avg_percent']
            
            # Check if price has dipped significantly
            dip_from_max = ((max_price - current_price) / max_price) * 100
            below_avg = ((avg_price - current_price) / avg_price) * 100
            
            # Buy signals
            if dip_from_max >= buy_dip_threshold:
                return True, f"Price dipped {dip_from_max:.1f}% from recent high"
                
            if below_avg >= buy_below_avg_threshold and trend['trend'] != 'down':
                return True, f"Price {below_avg:.1f}% below average and not trending down"
                
            if position_in_range < 0.3:  # In bottom 30% of recent range
                return True, f"Price in lower 30% of recent range"
                
            return False, f"No clear buy signal (position: {position_in_range:.1%})"
            
        except Exception as e:
            logger.error(f"Error checking buy timing: {e}")
            return False, str(e)
            
    def should_convert_to_base(self) -> Tuple[bool, float, str]:
        """
        Determine if we should convert some USDC to base currency
        Returns (should_convert, amount, reason)
        """
        # Check if we have USDC to convert
        min_usdc = self.config['profit_management']['min_usdc_for_conversion']
        if self.usdc_balance < min_usdc:
            return False, 0, f"USDC balance {self.usdc_balance:.2f} below minimum {min_usdc}"
            
        # Check if it's a good time to buy
        should_buy, buy_reason = self.is_good_time_to_buy_base()
        
        if not should_buy:
            return False, 0, buy_reason
            
        # Calculate how much to convert
        conversion_percent = self.config['profit_management']['base_buyback_percent']
        amount_to_convert = self.usdc_balance * (conversion_percent / 100)
        
        # Ensure we don't convert more than max
        max_conversion = self.config['profit_management']['max_usdc_per_conversion']
        amount_to_convert = min(amount_to_convert, max_conversion)
        
        return True, amount_to_convert, buy_reason
        
    def get_profit_summary(self) -> Dict:
        """Get summary of profit management status"""
        base_currency = self.get_base_currency_name()
        current_base_price = self.get_base_currency_price()
        trend = self.calculate_base_currency_trend()
        
        # Calculate total conversions
        total_to_usdc = sum(c['usdc_received'] for c in self.conversion_history if c.get('type') == 'to_usdc' and c.get('success'))
        total_to_base = sum(c['usdc_amount'] for c in self.conversion_history if c.get('type') == 'to_base' and c.get('success'))
        
        return {
            'base_currency': base_currency,
            'current_base_price': current_base_price,
            'base_currency_trend': trend,
            'usdc_balance': self.usdc_balance,
            'total_converted_to_usdc': total_to_usdc,
            'total_converted_to_base': total_to_base,
            'net_usdc_position': self.usdc_balance,
            'conversion_count': len(self.conversion_history)
        }
