"""
EVM DEX Trader (Uniswap/PancakeSwap integration)
Handles buy/sell operations for EVM tokens.
"""

import logging
from web3 import Web3
from eth_account import Account

logger = logging.getLogger(__name__)

# WETH addresses per chain ID
WETH_ADDRESSES = {
    1: '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2',      # Ethereum Mainnet
    56: '0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c',     # BSC (WBNB)
    137: '0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270',    # Polygon (WMATIC)
    43114: '0xB31f66AA3C1e785363F0875A1B74E27b85FD66c7',  # Avalanche (WAVAX)
    250: '0x21be370D5312f44cB42ce377BC9b8a0cEF1A4C83',    # Fantom (WFTM)
    42161: '0x82aF49447D8a07e3bd95BD0d56f35241523fBab1',   # Arbitrum (WETH)
    10: '0x4200000000000000000000000000000000000006',      # Optimism (WETH)
}

ERC20_APPROVE_ABI = [
    {
        "inputs": [
            {"internalType": "address", "name": "spender", "type": "address"},
            {"internalType": "uint256", "name": "amount", "type": "uint256"}
        ],
        "name": "approve",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "nonpayable",
        "type": "function"
    },
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

class EVMDexTrader:
    def __init__(self, w3: Web3, account: Account, router_address: str):
        self.w3 = w3
        self.account = account
        self.router_address = router_address
        # Detect chain ID to look up WETH address
        try:
            self.chain_id = self.w3.eth.chain_id
        except Exception:
            self.chain_id = 1
        self.weth_address = WETH_ADDRESSES.get(self.chain_id, WETH_ADDRESSES[1])
        # Uniswap/PancakeSwap V2 Router ABI
        self.router_abi = [
            {
                "inputs": [
                    {"internalType": "uint256", "name": "amountOutMin", "type": "uint256"},
                    {"internalType": "address[]", "name": "path", "type": "address[]"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "deadline", "type": "uint256"}
                ],
                "name": "swapExactETHForTokens",
                "outputs": [
                    {"internalType": "uint256[]", "name": "amounts", "type": "uint256[]"}
                ],
                "stateMutability": "payable",
                "type": "function"
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "amountIn", "type": "uint256"},
                    {"internalType": "uint256", "name": "amountOutMin", "type": "uint256"},
                    {"internalType": "address[]", "name": "path", "type": "address[]"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "deadline", "type": "uint256"}
                ],
                "name": "swapExactTokensForETH",
                "outputs": [
                    {"internalType": "uint256[]", "name": "amounts", "type": "uint256[]"}
                ],
                "stateMutability": "nonpayable",
                "type": "function"
            }
        ]
        self.router = self.w3.eth.contract(address=self.router_address, abi=self.router_abi)

    def buy_token(self, token_address: str, amount_eth: float, slippage: float = 0.05):
        """Buy a token using Uniswap/PancakeSwap V2 Router (ETH -> token)."""
        try:
            weth = self.w3.to_checksum_address(self.weth_address)
            token = self.w3.to_checksum_address(token_address)
            path = [weth, token]
            deadline = self.w3.eth.get_block('latest').timestamp + 1200
            amount_in_wei = self.w3.to_wei(amount_eth, 'ether')
            txn = self.router.functions.swapExactETHForTokens(
                0, path, self.account.address, deadline
            ).build_transaction({
                'from': self.account.address,
                'value': amount_in_wei,
                'gas': 300000,
                'gasPrice': self.w3.to_wei('5', 'gwei'),
                'nonce': self.w3.eth.get_transaction_count(self.account.address)
            })
            signed = self.account.sign_transaction(txn)
            tx_hash = self.w3.eth.send_raw_transaction(signed.rawTransaction)
            logger.info(f"[EVM DEX] Buy tx sent: {tx_hash.hex()}")
            return {"success": True, "txid": tx_hash.hex()}
        except Exception as e:
            logger.error(f"EVM buy_token error: {e}")
            return {"success": False, "error": str(e)}

    def sell_token(self, token_address: str, amount_token: float, slippage: float = 0.05):
        """Sell a token using Uniswap/PancakeSwap V2 Router (token -> ETH)."""
        try:
            token = self.w3.to_checksum_address(token_address)
            weth = self.w3.to_checksum_address(self.weth_address)
            path = [token, weth]
            deadline = self.w3.eth.get_block('latest').timestamp + 1200

            # Get token decimals and convert amount to raw units
            token_contract = self.w3.eth.contract(address=token, abi=ERC20_APPROVE_ABI)
            decimals = token_contract.functions.decimals().call()
            amount_in_raw = int(amount_token * (10 ** decimals))

            # Approve router to spend tokens
            approve_txn = token_contract.functions.approve(
                self.router_address, amount_in_raw
            ).build_transaction({
                'from': self.account.address,
                'gas': 100000,
                'gasPrice': self.w3.to_wei('5', 'gwei'),
                'nonce': self.w3.eth.get_transaction_count(self.account.address)
            })
            signed_approve = self.account.sign_transaction(approve_txn)
            self.w3.eth.send_raw_transaction(signed_approve.rawTransaction)

            # Execute swap
            swap_txn = self.router.functions.swapExactTokensForETH(
                amount_in_raw, 0, path, self.account.address, deadline
            ).build_transaction({
                'from': self.account.address,
                'gas': 300000,
                'gasPrice': self.w3.to_wei('5', 'gwei'),
                'nonce': self.w3.eth.get_transaction_count(self.account.address)
            })
            signed_swap = self.account.sign_transaction(swap_txn)
            tx_hash = self.w3.eth.send_raw_transaction(signed_swap.rawTransaction)
            logger.info(f"[EVM DEX] Sell tx sent: {tx_hash.hex()}")
            return {"success": True, "txid": tx_hash.hex()}
        except Exception as e:
            logger.error(f"EVM sell_token error: {e}")
            return {"success": False, "error": str(e)}
