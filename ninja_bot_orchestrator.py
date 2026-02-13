"""
Ninja Bot Orchestrator - Manages multiple concurrent wallet instances
Distributes operations across wallets to remain undetected
"""

import logging
import threading
import time
import random
from typing import Dict, List, Optional
from datetime import datetime
from scalper_bot import TokenScalper
from airdrop_finder import AirdropFinder
from config_loader import load_config_with_env

logger = logging.getLogger(__name__)


class NinjaBotOrchestrator:
    """
    Orchestrates multiple bot instances running concurrently
    Implements stealth features to avoid detection
    """
    
    def __init__(self, config_path: str = 'config.json'):
        """Initialize the ninja bot orchestrator"""
        self.config_path = config_path
        self.bot_instances: Dict[str, Dict] = {}
        self.shared_state = {
            'discovered_tokens': set(),
            'active_tokens': set(),
            'blacklisted_tokens': set(),
            'lock': threading.Lock(),
        }
        self.running = False
        self.threads: List[threading.Thread] = []
        
        logger.info("🥷 Ninja Bot Orchestrator initialized")
        
    def create_bot_instances(self, config: Dict) -> List[TokenScalper]:
        """Create a bot instance for each wallet"""
        wallets_config = config.get('wallets', [])
        bots = []
        
        logger.info(f"Creating {len(wallets_config)} bot instances...")
        
        for idx, wallet_config in enumerate(wallets_config):
            try:
                wallet_specific_config = config.copy()
                wallet_specific_config['wallets'] = [wallet_config]
                import tempfile
                import json
                temp_dir = tempfile.gettempdir()
                temp_config_path = f'{temp_dir}/ninja_bot_config_{idx}.json'
                with open(temp_config_path, 'w') as f:
                    json.dump(wallet_specific_config, f)
                # Create bot instance
                bot = TokenScalper(temp_config_path)
                
                wallet_id = f"{wallet_config.get('chain_id', 0)}:{bot.active_wallet_info['address'][:10]}"
                
                self.bot_instances[wallet_id] = {
                    'bot': bot,
                    'wallet_config': wallet_config,
                    'wallet_id': wallet_id,
                    'status': 'ready',
                    'positions_count': 0,
                    'last_trade_time': None,
                }
                
                bots.append(bot)
                logger.info(f"✅ Created bot instance for {wallet_id}")
                
            except Exception as e:
                logger.error(f"Failed to create bot instance {idx}: {e}")
                
        return bots
        
    def select_wallet_for_trade(self, token_address: str, config: Dict) -> Optional[str]:
        """
        Select which wallet should execute a trade
        Uses stealth logic to distribute trades
        """
        with self.shared_state['lock']:
            # Get max positions from config
            max_positions = config.get('ninja_mode', {}).get('max_positions_per_wallet', 5)
            
            # Filter available wallets
            available_wallets = []
            
            for wallet_id, instance_info in self.bot_instances.items():
                if instance_info['status'] == 'ready':
                    # Check if wallet has capacity (not too many positions)
                    if instance_info['positions_count'] < max_positions:
                        available_wallets.append(wallet_id)
                        
            if not available_wallets:
                logger.warning("No available wallets for trade")
                return None
                
            # Stealth selection: Random with bias toward less active wallets
            # This prevents patterns that could be detected
            wallet_weights = []
            for wallet_id in available_wallets:
                instance = self.bot_instances[wallet_id]
                # Weight inversely proportional to positions count
                weight = max_positions - instance['positions_count'] + 1
                
                # Add time-based factor (prefer wallets that haven't traded recently)
                if instance['last_trade_time']:
                    time_since_trade = (datetime.now() - instance['last_trade_time']).total_seconds()
                    if time_since_trade < 60:  # Less than 1 minute
                        weight *= 0.5  # Reduce weight
                        
                wallet_weights.append(weight)
                
            # Weighted random selection
            total_weight = sum(wallet_weights)
            if total_weight == 0:
                selected = random.choice(available_wallets)
            else:
                normalized_weights = [w / total_weight for w in wallet_weights]
                selected = random.choices(available_wallets, weights=normalized_weights)[0]
                
            logger.info(f"🎯 Selected wallet {selected} for trade")
            return selected
            
    def coordinate_token_discovery(self) -> List[str]:
        """
        Coordinate token discovery across all instances
        Prevents duplicate scanning
        """
        new_tokens = []
        
        # Use first available bot to scan (they all see the same blockchain)
        for wallet_id, instance_info in self.bot_instances.items():
            if instance_info['status'] == 'ready':
                bot = instance_info['bot']
                discovered = bot.scan_for_new_launches()
                
                with self.shared_state['lock']:
                    for token in discovered:
                        if token not in self.shared_state['discovered_tokens']:
                            self.shared_state['discovered_tokens'].add(token)
                            new_tokens.append(token)
                            
                break  # Only need one bot to scan
                
        return new_tokens
        
    def execute_trade_on_wallet(self, wallet_id: str, token_address: str, action: str):
        """Execute a trade on a specific wallet"""
        try:
            if wallet_id not in self.bot_instances:
                logger.error(f"Wallet {wallet_id} not found")
                return
                
            instance_info = self.bot_instances[wallet_id]
            bot = instance_info['bot']
            
            # Add stealth delay (randomized to avoid patterns)
            stealth_delay = random.uniform(1, 5)
            logger.info(f"🕐 Stealth delay: {stealth_delay:.2f}s")
            time.sleep(stealth_delay)
            
            if action == 'buy':
                # Analyze token first
                analysis = bot.analyze_token(token_address)
                
                if bot.should_buy_token(analysis):
                    # Randomize buy amount slightly for stealth
                    base_amount = bot.config['trading']['buy_amount_eth']
                    variation = random.uniform(0.9, 1.1)  # ±10% variation
                    adjusted_amount = base_amount * variation
                    
                    # Temporarily override config
                    original_amount = bot.config['trading']['buy_amount_eth']
                    bot.config['trading']['buy_amount_eth'] = adjusted_amount
                    
                    success = bot.buy_token(token_address)
                    
                    # Restore original config
                    bot.config['trading']['buy_amount_eth'] = original_amount
                    
                    if success:
                        with self.shared_state['lock']:
                            instance_info['positions_count'] += 1
                            instance_info['last_trade_time'] = datetime.now()
                            self.shared_state['active_tokens'].add(token_address)
                            
            elif action == 'sell':
                # This would be called by individual bot's monitoring
                pass
                
        except Exception as e:
            logger.error(f"Error executing trade on {wallet_id}: {e}")
            
    def run_bot_instance(self, wallet_id: str):
        """Run a single bot instance in a thread"""
        try:
            instance_info = self.bot_instances[wallet_id]
            bot = instance_info['bot']
            
            logger.info(f"🏃 Starting bot instance: {wallet_id}")
            instance_info['status'] = 'running'
            
            while self.running:
                try:
                    # Monitor positions for this wallet
                    bot.monitor_positions()
                    
                    # Check base currency opportunities
                    if hasattr(bot, 'check_base_currency_opportunities'):
                        bot.check_base_currency_opportunities()
                    
                    # Update position count
                    with self.shared_state['lock']:
                        instance_info['positions_count'] = len(bot.active_positions)
                    
                    # Random sleep to avoid synchronized patterns
                    sleep_time = random.uniform(2, 5)
                    time.sleep(sleep_time)
                    
                except Exception as e:
                    logger.error(f"Error in bot instance {wallet_id}: {e}")
                    time.sleep(5)
                    
            instance_info['status'] = 'stopped'
            logger.info(f"🛑 Stopped bot instance: {wallet_id}")
            
        except Exception as e:
            logger.error(f"Fatal error in bot instance {wallet_id}: {e}")
            instance_info['status'] = 'error'
            
    def start_all_instances(self):
        """Start all bot instances concurrently"""
        logger.info("🚀 Starting all bot instances...")
        self.running = True
        
        # Start a thread for each bot instance
        for wallet_id in self.bot_instances.keys():
            thread = threading.Thread(
                target=self.run_bot_instance,
                args=(wallet_id,),
                name=f"Bot-{wallet_id}",
                daemon=True
            )
            thread.start()
            self.threads.append(thread)
            
        logger.info(f"✅ Started {len(self.threads)} bot instances")
        
    def stop_all_instances(self):
        """Stop all bot instances"""
        logger.info("🛑 Stopping all bot instances...")
        self.running = False
        
        # Wait for all threads to finish
        for thread in self.threads:
            thread.join(timeout=10)
            
        logger.info("✅ All bot instances stopped")
        
    def get_status_summary(self) -> Dict:
        """Get status summary of all instances"""
        summary = {
            'total_instances': len(self.bot_instances),
            'running_instances': 0,
            'total_positions': 0,
            'total_balance_usd': 0,
            'instances': []
        }
        
        with self.shared_state['lock']:
            for wallet_id, instance_info in self.bot_instances.items():
                bot = instance_info['bot']
                
                if instance_info['status'] == 'running':
                    summary['running_instances'] += 1
                    
                summary['total_positions'] += instance_info['positions_count']
                
                instance_summary = {
                    'wallet_id': wallet_id,
                    'chain': bot.active_wallet_info['chain_name'],
                    'status': instance_info['status'],
                    'positions': instance_info['positions_count'],
                    'balance': bot.active_wallet_info['base_balance'],
                    'symbol': bot.active_wallet_info['base_symbol'],
                }
                
                summary['instances'].append(instance_summary)
                
        return summary
        
    def display_status(self):
        """Display status of all instances"""
        summary = self.get_status_summary()
        
        logger.info("=" * 80)
        logger.info("🥷 NINJA BOT STATUS")
        logger.info(f"Total Instances: {summary['total_instances']}")
        logger.info(f"Running: {summary['running_instances']}")
        logger.info(f"Total Positions: {summary['total_positions']}")
        logger.info("-" * 80)
        
        for instance in summary['instances']:
            logger.info(f"📍 {instance['wallet_id']}")
            logger.info(f"   Chain: {instance['chain']} | Status: {instance['status']}")
            logger.info(f"   Positions: {instance['positions']} | Balance: {instance['balance']:.4f} {instance['symbol']}")
            
        logger.info("=" * 80)
        
    def run_orchestrator(self):
        """Main orchestrator loop"""
        logger.info("🥷 Starting Ninja Bot Orchestrator")
        logger.info("=" * 80)
        
        # Load config with environment variable support
        config = load_config_with_env(self.config_path)
            
        # Create bot instances
        self.create_bot_instances(config)
        
        if not self.bot_instances:
            logger.error("No bot instances created, exiting")
            return
            
        # Start all instances
        self.start_all_instances()
        
        try:
            iteration = 0
            while True:
                iteration += 1
                
                # Coordinate token discovery (only one bot scans)
                new_tokens = self.coordinate_token_discovery()
                
                # Distribute new tokens across wallets
                for token_address in new_tokens:
                    # Select wallet for this trade (stealth distribution)
                    wallet_id = self.select_wallet_for_trade(token_address, config)
                    
                    if wallet_id:
                        # Execute trade in a separate thread to avoid blocking
                        trade_thread = threading.Thread(
                            target=self.execute_trade_on_wallet,
                            args=(wallet_id, token_address, 'buy'),
                            daemon=True
                        )
                        trade_thread.start()
                        
                # Display status periodically
                if iteration % 20 == 0:
                    self.display_status()
                    
                # Random sleep for stealth
                sleep_time = random.uniform(3, 7)
                time.sleep(sleep_time)
                
        except KeyboardInterrupt:
            logger.info("\n🛑 Shutting down Ninja Bot...")
            self.stop_all_instances()
            
        except Exception as e:
            logger.error(f"Fatal error in orchestrator: {e}")
            self.stop_all_instances()
            raise


def main():
    """Entry point for ninja bot orchestrator"""
    try:
        orchestrator = NinjaBotOrchestrator('config.json')
        orchestrator.run_orchestrator()
    except Exception as e:
        logger.error(f"Failed to start ninja bot: {e}")
        raise


if __name__ == "__main__":
    main()
