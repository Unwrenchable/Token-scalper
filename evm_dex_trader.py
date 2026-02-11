"""
EVM DEX Trader (Uniswap/PancakeSwap integration)
Handles buy/sell operations for EVM tokens.
"""

import logging
from web3 import Web3
from eth_account import Account

logger = logging.getLogger(__name__)

class EVMDexTrader:
    def __init__(self, w3: Web3, account: Account, router_address: str):
        self.w3 = w3
        self.account = account
        self.router_address = router_address
        # Uniswap/PancakeSwap V2 Router ABI (swapExactETHForTokens)
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
            }
        ]
        self.router = self.w3.eth.contract(address=self.router_address, abi=self.router_abi)

    def buy_token(self, token_address: str, amount_eth: float, slippage: float = 0.05):
        """Buy a token using Uniswap/PancakeSwap V2 Router."""
        try:
            path = [self.w3.to_checksum_address(self.w3.eth.default_account), self.w3.to_checksum_address(token_address)]
            deadline = self.w3.eth.get_block('latest').timestamp + 1200
            amount_in_wei = self.w3.to_wei(amount_eth, 'ether')
            # For demo, set amountOutMin to 0 (should use real quote and slippage in prod)
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
        """Stub: Implement sell logic for EVM tokens (requires approve and swap)."""
        logger.info(f"[EVM DEX] Sell {amount_token} {token_address} (stub)")
        # TODO: Implement real sell logic
        return {"success": True, "txid": "stub-evm-sell"}
