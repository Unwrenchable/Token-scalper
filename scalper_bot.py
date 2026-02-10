"""
Token Scalper Bot - Main Module
Monitors for new token launches and executes profitable trades with responsible selling
Includes rug pull protection, moonshot position retention, and USDC profit conversion
"""

import json
import time
import logging
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from web3 import Web3
from decimal import Decimal
from wallet_monitor import WalletMonitor
from profit_manager import ProfitManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scalper_bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class TokenScalper:
    """Main bot class for token scalping operations"""
    
    def __init__(self, config_path: str = 'config.json'):
        """Initialize the token scalper bot"""
        self.config = self._load_config(config_path)
        self.w3 = self._initialize_web3()
        self.wallet_monitor = WalletMonitor(self.w3, self.config)
        self.profit_manager = ProfitManager(self.w3, self.config)
        self.active_positions: Dict[str, Dict] = {}
        self.monitored_tokens: List[str] = []
        self.blacklisted_tokens: set = set(self.config['monitoring']['blacklisted_tokens'])
        
        logger.info("Token Scalper Bot initialized")
        logger.info("🛡️ Rug pull protection enabled" if self.config['rug_protection']['enable_dev_monitoring'] else "⚠️ Rug pull protection disabled")
        logger.info("💵 USDC profit conversion enabled" if self.config['profit_management']['auto_convert_to_usdc'] else "💰 Keeping profits in base currency")
        
    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from JSON file"""
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
            logger.info(f"Configuration loaded from {config_path}")
            return config
        except FileNotFoundError:
            logger.error(f"Config file not found: {config_path}")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in config file: {e}")
            raise
            
    def _initialize_web3(self) -> Web3:
        """Initialize Web3 connection"""
        rpc_url = self.config['network']['rpc_url']
        w3 = Web3(Web3.HTTPProvider(rpc_url))
        
        if not w3.is_connected():
            logger.error("Failed to connect to blockchain")
            raise ConnectionError("Cannot connect to RPC endpoint")
            
        logger.info(f"Connected to blockchain, Chain ID: {w3.eth.chain_id}")
        return w3
        
    def scan_for_new_launches(self) -> List[str]:
        """
        Scan blockchain for new token launches
        Returns list of new token addresses
        """
        logger.info("Scanning for new token launches...")
        new_tokens = []
        
        try:
            # Get latest block
            latest_block = self.w3.eth.block_number
            
            # In a real implementation, this would:
            # 1. Monitor DEX router events for new pairs
            # 2. Check liquidity additions
            # 3. Analyze contract creation events
            # For now, we'll return empty list as placeholder
            
            logger.info(f"Scanned block {latest_block}, found {len(new_tokens)} new tokens")
            
        except Exception as e:
            logger.error(f"Error scanning for launches: {e}")
            
        return new_tokens
        
    def analyze_token(self, token_address: str) -> Dict:
        """
        Analyze token for safety and profit potential
        Returns dict with analysis results
        """
        logger.info(f"Analyzing token: {token_address}")
        
        analysis = {
            'address': token_address,
            'safe': False,
            'liquidity_eth': 0,
            'holder_count': 0,
            'buy_tax': 0,
            'sell_tax': 0,
            'is_honeypot': False,
            'contract_verified': False,
        }
        
        try:
            # Check if token is blacklisted
            if token_address.lower() in self.blacklisted_tokens:
                logger.warning(f"Token {token_address} is blacklisted")
                return analysis
                
            # In a real implementation, this would:
            # 1. Check liquidity pool size
            # 2. Verify contract code
            # 3. Test for honeypot
            # 4. Check buy/sell taxes
            # 5. Count token holders
            # 6. Check contract age
            
            # Placeholder logic
            analysis['safe'] = True
            analysis['liquidity_eth'] = 10  # Example value
            
        except Exception as e:
            logger.error(f"Error analyzing token {token_address}: {e}")
            
        return analysis
        
    def should_buy_token(self, analysis: Dict) -> bool:
        """
        Determine if token should be bought based on analysis
        """
        if not analysis['safe']:
            return False
            
        # Check minimum liquidity
        min_liquidity = self.config['trading']['min_liquidity_eth']
        if analysis['liquidity_eth'] < min_liquidity:
            logger.info(f"Token liquidity {analysis['liquidity_eth']} < minimum {min_liquidity}")
            return False
            
        # Check buy tax
        max_buy_tax = self.config['trading']['max_buy_tax']
        if analysis['buy_tax'] > max_buy_tax:
            logger.info(f"Buy tax {analysis['buy_tax']}% > maximum {max_buy_tax}%")
            return False
            
        # Check sell tax
        max_sell_tax = self.config['trading']['max_sell_tax']
        if analysis['sell_tax'] > max_sell_tax:
            logger.info(f"Sell tax {analysis['sell_tax']}% > maximum {max_sell_tax}%")
            return False
            
        # Check if honeypot
        if analysis['is_honeypot']:
            logger.warning(f"Token {analysis['address']} appears to be a honeypot")
            return False
            
        return True
        
    def buy_token(self, token_address: str) -> bool:
        """
        Execute token purchase
        Returns True if successful
        """
        logger.info(f"Attempting to buy token: {token_address}")
        
        try:
            buy_amount = self.config['trading']['buy_amount_eth']
            
            # In a real implementation, this would:
            # 1. Prepare swap transaction through DEX router
            # 2. Calculate min tokens out with slippage
            # 3. Sign and send transaction
            # 4. Wait for confirmation
            # 5. Update position tracking
            
            # Placeholder - simulate successful purchase
            entry_price = 0.00001  # Example entry price
            tokens_bought = buy_amount / entry_price
            
            # Track position
            self.active_positions[token_address] = {
                'entry_price': entry_price,
                'entry_time': datetime.now().isoformat(),
                'amount': tokens_bought,
                'eth_invested': buy_amount,
                'sold_amount': 0,
                'realized_profit': 0,
                'kept_for_moonshot': 0
            }
            
            # Start tracking dev wallets
            if self.config['rug_protection']['enable_dev_monitoring']:
                self.wallet_monitor.identify_dev_wallets(token_address)
                self.wallet_monitor.track_wallet_balances(token_address)
            
            logger.info(f"✅ Successfully bought {tokens_bought} tokens at {entry_price} ETH")
            return True
            
        except Exception as e:
            logger.error(f"Error buying token {token_address}: {e}")
            return False
            
    def get_current_price(self, token_address: str) -> float:
        """Get current token price in ETH"""
        try:
            # In a real implementation, this would:
            # 1. Query DEX pair reserves
            # 2. Calculate price from reserve ratio
            
            # Placeholder - simulate price with some profit
            if token_address in self.active_positions:
                entry_price = self.active_positions[token_address]['entry_price']
                # DEMO: Simulate 60% profit for demonstration purposes
                # In production, this would query actual DEX pair reserves
                return entry_price * 1.6
                
            return 0
            
        except Exception as e:
            logger.error(f"Error getting price for {token_address}: {e}")
            return 0
            
    def calculate_profit_loss(self, token_address: str) -> Tuple[float, float]:
        """
        Calculate profit/loss for a position
        Returns (profit_percent, profit_eth)
        """
        if token_address not in self.active_positions:
            return 0.0, 0.0
            
        position = self.active_positions[token_address]
        current_price = self.get_current_price(token_address)
        entry_price = position['entry_price']
        
        # Calculate unrealized profit on remaining tokens
        remaining_tokens = position['amount'] - position['sold_amount']
        current_value = remaining_tokens * current_price
        initial_value = remaining_tokens * entry_price
        
        profit_eth = current_value - initial_value + position['realized_profit']
        profit_percent = (profit_eth / position['eth_invested']) * 100
        
        return profit_percent, profit_eth
        
    def should_sell_position(self, token_address: str) -> Tuple[bool, str]:
        """
        Determine if position should be sold
        Returns (should_sell, reason)
        """
        profit_percent, _ = self.calculate_profit_loss(token_address)
        
        profit_target = self.config['trading']['profit_target_percent']
        stop_loss = self.config['trading']['stop_loss_percent']
        
        # Check for rug pull / dev selling first
        if self.config['rug_protection']['enable_dev_monitoring']:
            should_exit, rug_reason = self.wallet_monitor.should_exit_position(token_address)
            if should_exit:
                logger.error(f"🚨 RUG PULL RISK: {rug_reason}")
                return True, f"rug_protection: {rug_reason}"
        
        # Check profit target
        if profit_percent >= profit_target:
            logger.info(f"Profit target reached: {profit_percent:.2f}%")
            return True, "profit_target"
            
        # Check stop loss
        if profit_percent <= -stop_loss:
            logger.warning(f"Stop loss triggered: {profit_percent:.2f}%")
            return True, "stop_loss"
            
        return False, ""
        
    def sell_token_responsibly(self, token_address: str, reason: str = "profit_target") -> bool:
        """
        Sell token position in chunks to avoid killing the chart
        Keeps a percentage for potential moonshots unless it's a rug pull
        This is the key feature for responsible selling
        """
        logger.info(f"Starting responsible sell for token: {token_address}, reason: {reason}")
        
        if token_address not in self.active_positions:
            logger.error(f"No active position for {token_address}")
            return False
            
        try:
            position = self.active_positions[token_address]
            remaining_tokens = position['amount'] - position['sold_amount'] - position['kept_for_moonshot']
            
            if remaining_tokens <= 0:
                logger.info("Position already fully sold")
                return True
                
            # Determine if we should keep some for moonshot
            keep_percentage = self.config['selling']['keep_percentage_for_moonshot']
            is_emergency_exit = reason.startswith('rug_protection')
            
            tokens_to_keep = 0
            if not is_emergency_exit and keep_percentage > 0:
                tokens_to_keep = position['amount'] * (keep_percentage / 100)
                logger.info(f"🌙 Keeping {tokens_to_keep:.2f} tokens ({keep_percentage}%) for potential moonshot")
            elif is_emergency_exit:
                logger.warning(f"⚠️ EMERGENCY EXIT - Selling ALL tokens including moonshot reserve")
                # Include any previously kept tokens in the sell
                remaining_tokens += position['kept_for_moonshot']
                tokens_to_keep = 0
                
            # Calculate tokens to sell now
            tokens_to_sell_total = remaining_tokens - tokens_to_keep
            
            if tokens_to_sell_total <= 0:
                logger.info("No tokens to sell after moonshot reserve")
                position['kept_for_moonshot'] = tokens_to_keep
                return True
            
            # Sell in chunks to minimize price impact
            num_chunks = self.config['selling']['sell_chunks']
            
            # For emergency exits, use fewer chunks and shorter delays
            if is_emergency_exit:
                num_chunks = min(num_chunks, 3)
                chunk_delay = 5  # Much shorter delay for emergency
            else:
                chunk_delay = self.config['selling']['chunk_delay_seconds']
                
            chunk_size = tokens_to_sell_total / num_chunks
            
            logger.info(f"Selling {tokens_to_sell_total:.2f} tokens in {num_chunks} chunks")
            
            for i in range(num_chunks):
                # Calculate tokens to sell in this chunk
                tokens_this_chunk = chunk_size
                if i == num_chunks - 1:
                    # Sell all remaining in last chunk
                    tokens_this_chunk = tokens_to_sell_total - (chunk_size * i)
                    
                # In a real implementation, this would:
                # 1. Check current price impact
                # 2. If impact > max, reduce chunk size
                # 3. Execute sell transaction
                # 4. Wait for confirmation
                
                current_price = self.get_current_price(token_address)
                eth_received = tokens_this_chunk * current_price
                
                # Update position tracking
                position['sold_amount'] += tokens_this_chunk
                position['realized_profit'] += eth_received - (tokens_this_chunk * position['entry_price'])
                
                logger.info(f"📊 Sold chunk {i+1}/{num_chunks}: {tokens_this_chunk:.2f} tokens for {eth_received:.6f} ETH")
                
                # Convert to USDC if enabled
                if self.config['profit_management']['auto_convert_to_usdc']:
                    # Keep a percentage in base currency
                    keep_percent = self.config['profit_management']['keep_base_currency_percent']
                    eth_to_keep = eth_received * (keep_percent / 100)
                    eth_to_convert = eth_received - eth_to_keep
                    
                    if eth_to_convert > 0:
                        conversion = self.profit_manager.convert_to_usdc(eth_to_convert, "profit_taking")
                        if conversion.get('success'):
                            logger.info(f"💵 Converted {eth_to_convert:.6f} ETH to {conversion['usdc_received']:.2f} USDC (kept {eth_to_keep:.6f} ETH)")
                
                # Wait between chunks to minimize market impact
                if i < num_chunks - 1:
                    logger.info(f"Waiting {chunk_delay}s before next chunk...")
                    time.sleep(chunk_delay)
                    
            # Update kept for moonshot
            if not is_emergency_exit:
                position['kept_for_moonshot'] = tokens_to_keep
                
            # Calculate final profit on sold portion
            profit_percent, profit_eth = self.calculate_profit_loss(token_address)
            
            if position['kept_for_moonshot'] > 0:
                logger.info(f"✅ Partial position closed: {profit_percent:.2f}% profit ({profit_eth:.6f} ETH)")
                logger.info(f"🌙 Kept {position['kept_for_moonshot']:.2f} tokens for moonshot potential")
                # Don't remove from active positions, keep monitoring
            else:
                logger.info(f"✅ Position fully closed: {profit_percent:.2f}% profit ({profit_eth:.6f} ETH)")
                # Remove from active positions
                del self.active_positions[token_address]
            
            return True
            
        except Exception as e:
            logger.error(f"Error selling token {token_address}: {e}")
            return False
            
    def check_moonshot_status(self, token_address: str) -> bool:
        """
        Check if kept tokens have moonshotted
        Returns True if moonshot target reached
        """
        if token_address not in self.active_positions:
            return False
            
        position = self.active_positions[token_address]
        
        # Only check if we have tokens kept for moonshot
        if position['kept_for_moonshot'] <= 0:
            return False
            
        current_price = self.get_current_price(token_address)
        entry_price = position['entry_price']
        
        price_multiplier = current_price / entry_price
        moonshot_multiplier = self.config['selling']['moonshot_multiplier']
        
        if price_multiplier >= moonshot_multiplier:
            logger.info(f"🚀 MOONSHOT! Price is {price_multiplier:.2f}x entry price (target was {moonshot_multiplier}x)")
            return True
            
        return False
        
    def sell_moonshot_tokens(self, token_address: str) -> bool:
        """
        Sell the tokens that were kept for moonshot potential
        """
        if token_address not in self.active_positions:
            return False
            
        position = self.active_positions[token_address]
        
        if position['kept_for_moonshot'] <= 0:
            logger.info("No moonshot tokens to sell")
            return True
            
        logger.info(f"🌙 Selling moonshot reserve: {position['kept_for_moonshot']:.2f} tokens")
        
        try:
            # Sell the kept tokens
            current_price = self.get_current_price(token_address)
            eth_received = position['kept_for_moonshot'] * current_price
            
            position['realized_profit'] += eth_received - (position['kept_for_moonshot'] * position['entry_price'])
            position['sold_amount'] += position['kept_for_moonshot']
            position['kept_for_moonshot'] = 0
            
            # Convert moonshot profits to USDC if enabled
            if self.config['profit_management']['auto_convert_to_usdc']:
                keep_percent = self.config['profit_management']['keep_base_currency_percent']
                eth_to_keep = eth_received * (keep_percent / 100)
                eth_to_convert = eth_received - eth_to_keep
                
                if eth_to_convert > 0:
                    conversion = self.profit_manager.convert_to_usdc(eth_to_convert, "moonshot_profit")
                    if conversion.get('success'):
                        logger.info(f"💵 Converted moonshot profit: {eth_to_convert:.6f} ETH to {conversion['usdc_received']:.2f} USDC")
            
            # Calculate final profit
            profit_percent = (position['realized_profit'] / position['eth_invested']) * 100
            
            logger.info(f"🎉 Moonshot tokens sold for {eth_received:.6f} ETH")
            logger.info(f"✅ Final profit: {profit_percent:.2f}% ({position['realized_profit']:.6f} ETH)")
            
            # Remove from active positions
            del self.active_positions[token_address]
            
            return True
            
        except Exception as e:
            logger.error(f"Error selling moonshot tokens: {e}")
            return False
            
    def monitor_positions(self):
        """Monitor active positions and take action when needed"""
        if not self.active_positions:
            return
            
        logger.info(f"Monitoring {len(self.active_positions)} active positions")
        
        for token_address in list(self.active_positions.keys()):
            try:
                position = self.active_positions[token_address]
                profit_percent, profit_eth = self.calculate_profit_loss(token_address)
                
                # Show position status
                status_parts = [f"Position {token_address[:10]}... P/L: {profit_percent:.2f}% ({profit_eth:.6f} ETH)"]
                if position['kept_for_moonshot'] > 0:
                    status_parts.append(f"[🌙 {position['kept_for_moonshot']:.2f} tokens held for moonshot]")
                logger.info(" ".join(status_parts))
                
                # Check if moonshot target reached for kept tokens
                if self.check_moonshot_status(token_address):
                    self.sell_moonshot_tokens(token_address)
                    continue
                
                # Check if we should sell the position
                should_sell, reason = self.should_sell_position(token_address)
                if should_sell:
                    self.sell_token_responsibly(token_address, reason)
                    
                # Update dev wallet monitoring
                if self.config['rug_protection']['enable_dev_monitoring']:
                    self.wallet_monitor.track_wallet_balances(token_address)
                    
            except Exception as e:
                logger.error(f"Error monitoring position {token_address}: {e}")
                
    def check_base_currency_opportunities(self):
        """Check if it's a good time to buy base currency with USDC"""
        if not self.config['profit_management']['auto_convert_to_usdc']:
            return
            
        try:
            should_convert, amount, reason = self.profit_manager.should_convert_to_base()
            
            if should_convert:
                logger.info(f"💰 Good time to buy {self.profit_manager.get_base_currency_name()}: {reason}")
                conversion = self.profit_manager.convert_to_base_currency(amount, reason)
                
                if conversion.get('success'):
                    logger.info(f"✅ Bought back {conversion['base_received']:.6f} {conversion['base_currency']} with {amount:.2f} USDC")
                    
        except Exception as e:
            logger.error(f"Error checking base currency opportunities: {e}")
            
    def display_profit_summary(self):
        """Display summary of profit management status"""
        if not self.config['profit_management']['auto_convert_to_usdc']:
            return
            
        try:
            summary = self.profit_manager.get_profit_summary()
            
            logger.info("=" * 60)
            logger.info("💰 PROFIT MANAGEMENT SUMMARY")
            logger.info(f"Base Currency: {summary['base_currency']}")
            logger.info(f"Current {summary['base_currency']} Price: ${summary['current_base_price']:.2f}")
            logger.info(f"Trend: {summary['base_currency_trend']['trend'].upper()} ({summary['base_currency_trend']['change_percent']:+.2f}%)")
            logger.info(f"USDC Balance: ${summary['usdc_balance']:.2f}")
            logger.info(f"Total Converted to USDC: ${summary['total_converted_to_usdc']:.2f}")
            logger.info(f"Total Converted to {summary['base_currency']}: ${summary['total_converted_to_base']:.2f}")
            logger.info("=" * 60)
            
        except Exception as e:
            logger.error(f"Error displaying profit summary: {e}")
                
    def run(self):
        """Main bot loop"""
        logger.info("🚀 Starting Token Scalper Bot")
        logger.info("=" * 60)
        
        scan_interval = self.config['monitoring']['scan_interval_seconds']
        iteration_count = 0
        
        try:
            while True:
                iteration_count += 1
                
                # Record base currency price for trend analysis
                if self.config['profit_management']['auto_convert_to_usdc']:
                    self.profit_manager.record_base_currency_price()
                
                # Scan for new launches
                new_tokens = self.scan_for_new_launches()
                
                # Analyze and potentially buy new tokens
                for token_address in new_tokens:
                    analysis = self.analyze_token(token_address)
                    
                    if self.should_buy_token(analysis):
                        self.buy_token(token_address)
                        
                # Monitor existing positions
                self.monitor_positions()
                
                # Check for base currency buying opportunities
                if iteration_count % 5 == 0:  # Check every 5 iterations
                    self.check_base_currency_opportunities()
                    
                # Display profit summary periodically
                if iteration_count % 20 == 0:  # Display every 20 iterations
                    self.display_profit_summary()
                
                # Wait before next scan
                time.sleep(scan_interval)
                
        except KeyboardInterrupt:
            logger.info("\n🛑 Bot stopped by user")
        except Exception as e:
            logger.error(f"Fatal error in bot loop: {e}")
            raise


def main():
    """Entry point for the bot"""
    try:
        bot = TokenScalper('config.json')
        bot.run()
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")
        raise


if __name__ == "__main__":
    main()
