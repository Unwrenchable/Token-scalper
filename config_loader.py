"""
Configuration loader with environment variable support
Loads config from JSON and merges with environment variables for security
"""

import os
import json
import logging
from typing import Dict, List, Optional
from dotenv import load_dotenv

logger = logging.getLogger(__name__)


class ConfigLoader:
    """Loads configuration from JSON and environment variables"""
    
    @staticmethod
    def load_config(config_path: str = 'config.json') -> Dict:
        """
        Load configuration with environment variable support
        
        Priority order:
        1. Environment variables (highest priority - most secure)
        2. config.json values (fallback)
        
        This allows sensitive data (private keys, RPC URLs) to be stored
        in .env file instead of config.json for better security.
        """
        # Load environment variables from .env file
        load_dotenv()
        
        # Load base config from JSON
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
            logger.info(f"Configuration loaded from {config_path}")
        except FileNotFoundError:
            logger.warning(f"Config file not found: {config_path}, using defaults")
            config = {}
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in config file: {e}")
            raise
            
        # Override wallets with environment variables if present
        config = ConfigLoader._load_wallets_from_env(config)
        
        # Override AI API key with environment variable if present
        config = ConfigLoader._load_ai_config_from_env(config)
        
        return config
        
    @staticmethod
    def _load_wallets_from_env(config: Dict) -> Dict:
        """
        Load wallet configurations from environment variables
        
        Environment variables format:
        WALLET_1_NAME, WALLET_1_RPC_URL, WALLET_1_CHAIN_ID, WALLET_1_PRIVATE_KEY
        WALLET_2_NAME, WALLET_2_RPC_URL, WALLET_2_CHAIN_ID, WALLET_2_PRIVATE_KEY
        etc.
        """
        env_wallets = []
        wallet_index = 1
        
        # Check for environment variable wallets
        while True:
            prefix = f"WALLET_{wallet_index}_"
            
            # Check if this wallet is defined in environment
            name = os.getenv(f"{prefix}NAME")
            rpc_url = os.getenv(f"{prefix}RPC_URL")
            chain_id = os.getenv(f"{prefix}CHAIN_ID")
            private_key = os.getenv(f"{prefix}PRIVATE_KEY")
            
            # If no RPC URL or private key, assume no more wallets
            if not rpc_url and not private_key:
                break
                
            # Validate required fields
            address = os.getenv(f"{prefix}ADDRESS")
            if rpc_url and private_key:
                wallet_config = {
                    'name': name or f"Wallet {wallet_index}",
                    'rpc_url': rpc_url,
                    'chain_id': int(chain_id) if chain_id else 1,
                    'private_key': private_key,
                }
                if address:
                    wallet_config['address'] = address
                env_wallets.append(wallet_config)
                logger.info(f"✅ Loaded wallet {wallet_index} from environment variables")
            else:
                logger.warning(f"⚠️ Incomplete wallet {wallet_index} config in environment, skipping")
                
            wallet_index += 1
            
        # Use environment wallets if found, otherwise use config wallets
        if env_wallets:
            logger.info(f"🔐 Using {len(env_wallets)} wallet(s) from environment variables (SECURE)")
            config['wallets'] = env_wallets
        elif 'wallets' in config:
            logger.warning(f"⚠️ Using {len(config['wallets'])} wallet(s) from config.json (LESS SECURE)")
            logger.warning("⚠️ Consider moving sensitive data to .env file for better security")
        else:
            logger.error("❌ No wallets configured in environment variables or config.json")
            
        return config
        
    @staticmethod
    def _load_ai_config_from_env(config: Dict) -> Dict:
        """
        Load AI configuration from environment variables
        
        Environment variables:
        AI_API_KEY - API key for OpenAI or Anthropic
        """
        ai_api_key = os.getenv("AI_API_KEY")
        
        if ai_api_key:
            # Ensure ai_analysis config exists
            if 'ai_analysis' not in config:
                config['ai_analysis'] = {
                    'enabled': False,
                    'provider': 'openai',
                    'model': 'gpt-4',
                    'max_tokens': 500
                }
            
            # Override API key from environment
            config['ai_analysis']['api_key'] = ai_api_key
            logger.info("🤖 AI API key loaded from environment variables (SECURE)")
            
            # Auto-enable AI if API key is present and not explicitly disabled
            if config['ai_analysis'].get('enabled') is None:
                config['ai_analysis']['enabled'] = True
        elif 'ai_analysis' in config and config['ai_analysis'].get('api_key'):
            logger.warning("⚠️ AI API key found in config.json (LESS SECURE)")
            logger.warning("⚠️ Consider moving AI_API_KEY to .env file for better security")
        
        return config
        
    @staticmethod
    def validate_config(config: Dict) -> bool:
        """
        Validate that configuration has required fields
        """
        if not config.get('wallets'):
            logger.error("No wallets configured")
            return False
            
        for idx, wallet in enumerate(config['wallets']):
            if not wallet.get('rpc_url'):
                logger.error(f"Wallet {idx+1} missing rpc_url")
                return False
            if not wallet.get('private_key'):
                logger.error(f"Wallet {idx+1} missing private_key")
                return False
            if not wallet.get('chain_id'):
                logger.error(f"Wallet {idx+1} missing chain_id")
                return False
                
        return True
        
    @staticmethod
    def get_example_env_content() -> str:
        """Get example .env content for documentation"""
        return """# Example .env file
WALLET_1_NAME="Ethereum Wallet"
WALLET_1_RPC_URL="https://mainnet.infura.io/v3/YOUR_INFURA_KEY"
WALLET_1_CHAIN_ID=1
WALLET_1_PRIVATE_KEY="your_private_key_here"

# Add more wallets as needed:
# WALLET_2_NAME="BSC Wallet"
# WALLET_2_RPC_URL="https://bsc-dataseed.binance.org/"
# WALLET_2_CHAIN_ID=56
# WALLET_2_PRIVATE_KEY="your_private_key_here"
"""


def load_config_with_env(config_path: str = 'config.json') -> Dict:
    """
    Convenience function to load config with environment variables
    """
    config = ConfigLoader.load_config(config_path)
    
    if not ConfigLoader.validate_config(config):
        raise ValueError("Invalid configuration")
        
    return config
