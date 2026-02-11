"""
Multi-wallet management module
Handles multiple wallets across different chains
"""


import logging
from typing import Dict, List, Optional, Tuple
from web3 import Web3
from decimal import Decimal
from solders.keypair import Keypair as SolKeypair
from solana.rpc.api import Client as SolanaClient
import requests

logger = logging.getLogger(__name__)


class MultiWalletManager:
    """Manages multiple wallets across different chains"""
    
    # Chain configurations with DEX routers and stablecoins
    CHAIN_CONFIG = {
        1: {  # Ethereum Mainnet
            'name': 'Ethereum',
            'symbol': 'ETH',
            'dex_router': '0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D',  # Uniswap V2
            'usdc_address': '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48',
            'usdt_address': '0xdAC17F958D2ee523a2206206994597C13D831ec7',
            'dai_address': '0x6B175474E89094C44Da98b954EedeAC495271d0F',
        },
        56: {  # BSC
            'name': 'Binance Smart Chain',
            'symbol': 'BNB',
            'dex_router': '0x10ED43C718714eb63d5aA57B78B54704E256024E',  # PancakeSwap
            'usdc_address': '0x8AC76a51cc950d9822D68b83fE1Ad97B32Cd580d',
            'usdt_address': '0x55d398326f99059fF775485246999027B3197955',
            'busd_address': '0xe9e7CEA3DedcA5984780Bafc599bD69ADd087D56',
        },
        137: {  # Polygon
            'name': 'Polygon',
            'symbol': 'MATIC',
            'dex_router': '0xa5E0829CaCEd8fFDD4De3c43696c57F7D7A678ff',  # QuickSwap
            'usdc_address': '0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174',
            'usdt_address': '0xc2132D05D31c914a87C6611C10748AEb04B58e8F',
            'dai_address': '0x8f3Cf7ad23Cd3CaDbD9735AFf958023239c6A063',
        },
        43114: {  # Avalanche
            'name': 'Avalanche',
            'symbol': 'AVAX',
            'dex_router': '0x60aE616a2155Ee3d9A68541Ba4544862310933d4',  # TraderJoe
            'usdc_address': '0xB97EF9Ef8734C71904D8002F8b6Bc66Dd9c48a6E',
            'usdt_address': '0x9702230A8Ea53601f5cD2dc00fDBc13d4dF4A8c7',
            'dai_address': '0xd586E7F844cEa2F87f50152665BCbc2C279D8d70',
        },
        250: {  # Fantom
            'name': 'Fantom',
            'symbol': 'FTM',
            'dex_router': '0xF491e7B69E4244ad4002BC14e878a34207E38c29',  # SpookySwap
            'usdc_address': '0x04068DA6C83AFCFA0e13ba15A6696662335D5B75',
            'usdt_address': '0x049d68029688eAbF473097a2fC38ef61633A3C7A',
            'dai_address': '0x8D11eC38a3EB5E956B052f67Da8Bdc9bef8Abf3E',
        },
        42161: {  # Arbitrum
            'name': 'Arbitrum',
            'symbol': 'ETH',
            'dex_router': '0x1b02dA8Cb0d097eB8D57A175b88c7D8b47997506',  # SushiSwap
            'usdc_address': '0xFF970A61A04b1cA14834A43f5dE4533eBDDB5CC8',
            'usdt_address': '0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9',
            'dai_address': '0xDA10009cBd5D07dd0CeCc66161FC93D7c9000da1',
        },
        10: {  # Optimism
            'name': 'Optimism',
            'symbol': 'ETH',
            'dex_router': '0x9c12939390052919aF3155f41Bf4160Fd3666A6f',  # Velodrome
            'usdc_address': '0x7F5c764cBc14f9669B88837ca1490cCa17c31607',
            'usdt_address': '0x94b008aA00579c1307B0EF2c499aD98a8ce58e58',
            'dai_address': '0xDA10009cBd5D07dd0CeCc66161FC93D7c9000da1',
        },
    }
    
    def __init__(self, wallets_config: List[Dict], config: Dict):
        """
        Initialize multi-wallet manager
        
        Args:
            wallets_config: List of wallet configurations
            config: Bot configuration
        """
        self.wallets = wallets_config
        self.config = config
        self.wallet_connections: Dict[str, Dict] = {}
        self.active_wallet: Optional[Dict] = None
        
        logger.info(f"MultiWalletManager initialized with {len(wallets_config)} wallet(s)")
        
    def connect_wallet(self, wallet_config: Dict) -> Optional[Dict]:
        """
        Connect to a wallet and get its details
        
        Returns dict with wallet info or None on failure
        """
        try:
            rpc_url = wallet_config.get('rpc_url')
            chain_id = wallet_config.get('chain_id')
            private_key = wallet_config.get('private_key')
            # Solana detection: chain_id == 'solana-devnet' or rpc_url contains 'solana'
            is_solana = str(chain_id).lower().startswith('solana') or (
                rpc_url and 'solana' in rpc_url)
            if is_solana:
                sol_client = SolanaClient(rpc_url)
                sol_keypair = SolKeypair.from_base58_string(private_key)
                address = str(sol_keypair.pubkey())
                # Get balance (lamports)
                balance_resp = sol_client.get_balance(address)
                base_balance = balance_resp['result']['value'] / 1e9  # SOL
                chain_name = 'Solana'
                base_symbol = 'SOL'
                # USDC SPL token address (devnet)
                usdc_token_address = '7XSzQZyQn5kQwQ6r5oXcQ2Yw1V6QwQ6r5oXcQ2Yw1V6Q'  # Example, replace with real devnet USDC mint
                usdc_balance = self._get_spl_token_balance(sol_client, address, usdc_token_address)
                wallet_info = {
                    'sol_client': sol_client,
                    'sol_keypair': sol_keypair,
                    'address': address,
                    'chain_id': chain_id,
                    'chain_name': chain_name,
                    'rpc_url': rpc_url,
                    'base_symbol': base_symbol,
                    'base_balance': float(base_balance),
                    'usdc_balance': usdc_balance,
                    'total_balance_usd': self._calculate_usd_value(float(base_balance), usdc_balance, chain_id),
                    'chain_config': {},
                }
                logger.info(f"✅ Connected to {chain_name} wallet: {address}")
                logger.info(f"   Balance: {base_balance:.4f} {base_symbol}, {usdc_balance:.2f} USDC")
                return wallet_info
                def _get_spl_token_balance(self, sol_client, owner_address, token_mint_address):
                    """Get SPL token balance for a Solana wallet."""
                    try:
                        resp = sol_client.get_token_accounts_by_owner(owner_address, {'mint': token_mint_address})
                        accounts = resp['result']['value']
                        if not accounts:
                            return 0.0
                        # Get balance from the first account
                        token_account = accounts[0]['pubkey']
                        balance_resp = sol_client.get_token_account_balance(token_account)
                        amount = float(balance_resp['result']['value']['uiAmount'])
                        return amount
                    except Exception as e:
                        logger.debug(f"Could not get SPL token balance for {token_mint_address}: {e}")
                        return 0.0
            else:
                # EVM logic
                w3 = Web3(Web3.HTTPProvider(rpc_url))
                if not w3.is_connected():
                    logger.error(f"Failed to connect to RPC: {rpc_url}")
                    return None
                account = w3.eth.account.from_key(private_key)
                address = account.address
                base_balance = w3.eth.get_balance(address)
                base_balance_eth = w3.from_wei(base_balance, 'ether')
                chain_info = self.CHAIN_CONFIG.get(chain_id, {})
                chain_name = chain_info.get('name', f'Chain {chain_id}')
                base_symbol = chain_info.get('symbol', 'ETH')
                usdc_balance = 0
                if 'usdc_address' in chain_info:
                    usdc_balance = self._get_token_balance(w3, address, chain_info['usdc_address'])
                wallet_info = {
                    'w3': w3,
                    'account': account,
                    'address': address,
                    'chain_id': chain_id,
                    'chain_name': chain_name,
                    'rpc_url': rpc_url,
                    'base_symbol': base_symbol,
                    'base_balance': float(base_balance_eth),
                    'usdc_balance': usdc_balance,
                    'total_balance_usd': self._calculate_usd_value(float(base_balance_eth), usdc_balance, chain_id),
                    'chain_config': chain_info,
                }
                logger.info(f"✅ Connected to {chain_name} wallet: {address}")
                logger.info(f"   Balance: {base_balance_eth:.4f} {base_symbol}, ${usdc_balance:.2f} USDC")
                return wallet_info
        except Exception as e:
            logger.error(f"Error connecting wallet: {e}")
            return None
            
    def _get_token_balance(self, w3: Web3, address: str, token_address: str) -> float:
        """Get ERC20 token balance"""
        try:
            # ERC20 balanceOf ABI
            erc20_abi = [
                {
                    "constant": True,
                    "inputs": [{"name": "_owner", "type": "address"}],
                    "name": "balanceOf",
                    "outputs": [{"name": "balance", "type": "uint256"}],
                    "type": "function"
                },
                {
                    "constant": True,
                    "inputs": [],
                    "name": "decimals",
                    "outputs": [{"name": "", "type": "uint8"}],
                    "type": "function"
                }
            ]
            
            contract = w3.eth.contract(address=token_address, abi=erc20_abi)
            balance = contract.functions.balanceOf(address).call()
            decimals = contract.functions.decimals().call()
            
            return balance / (10 ** decimals)
            
        except Exception as e:
            logger.debug(f"Could not get token balance for {token_address}: {e}")
            return 0.0
            
    def _get_live_price(self, symbol):
        """Get live USD price for a given symbol using CoinGecko."""
        try:
            coingecko_ids = {
                'ETH': 'ethereum',
                'BNB': 'binancecoin',
                'MATIC': 'matic-network',
                'AVAX': 'avalanche-2',
                'FTM': 'fantom',
                'SOL': 'solana',
            }
            coingecko_id = coingecko_ids.get(symbol.upper())
            if not coingecko_id:
                return None
            url = f'https://api.coingecko.com/api/v3/simple/price?ids={coingecko_id}&vs_currencies=usd'
            resp = requests.get(url, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            return float(data[coingecko_id]['usd'])
        except Exception as e:
            logger.debug(f"Could not fetch live price for {symbol}: {e}")
            return None
    def _calculate_usd_value(self, base_amount: float, usdc_amount: float, chain_id: int) -> float:
        """
        Calculate approximate USD value of wallet
        
        WARNING: Uses approximate/outdated prices for estimation only.
        In production, should use price oracles (Chainlink) or live APIs.
        """
        # Approximate prices (SHOULD BE REPLACED with real price feeds in production)
        # These are placeholder values for initial estimation
        base_prices = {
            'solana-devnet': 100.0,  # Approximate SOL price
            1: 3000.0,    # ETH - APPROXIMATE
            56: 300.0,    # BNB - APPROXIMATE
            137: 0.80,    # MATIC - APPROXIMATE
            43114: 35.0,  # AVAX - APPROXIMATE
            250: 0.50,    # FTM - APPROXIMATE
            42161: 3000.0, # ETH (Arbitrum) - APPROXIMATE
            10: 3000.0,   # ETH (Optimism) - APPROXIMATE
        }
        
        base_price = base_prices.get(chain_id, 0)
        if isinstance(chain_id, str) and chain_id.lower().startswith('solana'):
            base_price = base_prices['solana-devnet']
        return (base_amount * base_price) + usdc_amount
        return (base_amount * base_price) + usdc_amount
        
    def connect_all_wallets(self) -> List[Dict]:
        """Connect to all configured wallets"""
        connected_wallets = []
        
        for wallet_config in self.wallets:
            wallet_info = self.connect_wallet(wallet_config)
            if wallet_info:
                wallet_id = f"{wallet_info['chain_name']}:{wallet_info['address'][:10]}"
                self.wallet_connections[wallet_id] = wallet_info
                connected_wallets.append(wallet_info)
                
        logger.info(f"Connected to {len(connected_wallets)}/{len(self.wallets)} wallet(s)")
        return connected_wallets
        
    def select_best_wallet(self, prefer_funded: bool = True) -> Optional[Dict]:
        """
        Select the best wallet to use based on funding
        
        Args:
            prefer_funded: If True, prefer wallets with existing funds
            
        Returns selected wallet info or None
        """
        if not self.wallet_connections:
            logger.error("No wallets connected")
            return None
            
        wallets = list(self.wallet_connections.values())
        
        if prefer_funded:
            # Sort by total USD value (descending)
            funded_wallets = [w for w in wallets if w['total_balance_usd'] > 0]
            
            if funded_wallets:
                sorted_wallets = sorted(funded_wallets, key=lambda w: w['total_balance_usd'], reverse=True)
                selected = sorted_wallets[0]
                
                logger.info(f"📍 Selected wallet: {selected['chain_name']} ({selected['address'][:10]}...)")
                logger.info(f"   Total value: ${selected['total_balance_usd']:.2f}")
                
                self.active_wallet = selected
                return selected
            else:
                logger.warning("No funded wallets found, selecting first wallet")
                
        # Default: select first wallet
        selected = wallets[0]
        self.active_wallet = selected
        
        logger.info(f"📍 Selected wallet: {selected['chain_name']} ({selected['address'][:10]}...)")
        return selected
        
    def get_active_wallet(self) -> Optional[Dict]:
        """Get the currently active wallet"""
        return self.active_wallet
        
    def switch_wallet(self, wallet_id: str) -> bool:
        """Switch to a different wallet"""
        if wallet_id in self.wallet_connections:
            self.active_wallet = self.wallet_connections[wallet_id]
            logger.info(f"Switched to wallet: {wallet_id}")
            return True
        else:
            logger.error(f"Wallet not found: {wallet_id}")
            return False
            
    def get_wallet_summary(self) -> Dict:
        """Get summary of all connected wallets"""
        summary = {
            'total_wallets': len(self.wallet_connections),
            'active_wallet': None,
            'wallets': []
        }
        
        for wallet_id, wallet_info in self.wallet_connections.items():
            wallet_summary = {
                'id': wallet_id,
                'chain': wallet_info['chain_name'],
                'address': wallet_info['address'],
                'base_balance': wallet_info['base_balance'],
                'base_symbol': wallet_info['base_symbol'],
                'usdc_balance': wallet_info['usdc_balance'],
                'total_usd': wallet_info['total_balance_usd'],
                'is_active': wallet_info == self.active_wallet
            }
            
            summary['wallets'].append(wallet_summary)
            
            if wallet_info == self.active_wallet:
                summary['active_wallet'] = wallet_summary
                
        return summary
