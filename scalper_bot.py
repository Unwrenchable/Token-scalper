"""
scalper_bot.py - Token-scalper

Main bot module for automated trading, scam detection, and responsible selling.
Features:
    - Multi-wallet/multi-chain support
    - Rug pull protection
    - Moonshot position retention
    - USDC profit management
    - Webhook alert integration
    - Professional logging and modular architecture

Author: Vault 77 Ecosystem
License: MIT
"""


import logging
import time
import requests
from typing import Dict, List, Optional
from wallet_monitor import WalletMonitor
from profit_manager import ProfitManager
from multi_wallet_manager import MultiWalletManager
from config_loader import ConfigLoader
from airdrop_finder import AirdropFinder
from webhook_sender import send_alert_to_webhooks
from sol_dex_trader import SolDexTrader
from evm_dex_trader import EVMDexTrader
from safety_checker import SafetyChecker
from ai_analyzer import AITokenAnalyzer
from token_opportunity_scorer import TokenOpportunityScorer

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

# DexScreener API for token discovery
DEXSCREENER_NEW_PAIRS_URL = "https://api.dexscreener.com/latest/dex/tokens/new"
DEXSCREENER_TOKEN_URL = "https://api.dexscreener.com/latest/dex/tokens/{}"

# Chain name to DexScreener chain ID mapping
CHAIN_NAME_TO_DEXSCREENER = {
    'Ethereum': 'ethereum',
    'Binance Smart Chain': 'bsc',
    'Polygon': 'polygon',
    'Avalanche': 'avalanche',
    'Fantom': 'fantom',
    'Arbitrum': 'arbitrum',
    'Optimism': 'optimism',
    'Solana': 'solana',
}


class TokenScalper:
    """Main bot class for token scalping operations"""
    def __init__(self, config_path: str = 'config.json'):
        self.config = ConfigLoader.load_config(config_path)
        self.multi_wallet_manager = None
        self.w3 = None
        self.active_wallet_info = None
        if 'wallets' in self.config:
            self._initialize_multi_wallet()
        else:
            raise ValueError("Invalid configuration format: missing 'wallets' key.")
        self.wallet_monitor = WalletMonitor(self.w3, self.config)
        self.profit_manager = ProfitManager(self.w3, self.config)
        self.safety_checker = SafetyChecker(self.w3, self.config)
        self.ai_analyzer = AITokenAnalyzer(self.config)
        self.opportunity_scorer = TokenOpportunityScorer(self.config)
        self.active_positions: Dict[str, Dict] = {}
        self.airdrop_finder = AirdropFinder()
        self.monitored_tokens: List[str] = []
        self.blacklisted_tokens: set = set(self.config.get('monitoring', {}).get('blacklisted_tokens', []))
        logger.info("Token Scalper Bot initialized")

    def _initialize_multi_wallet(self):
        wallets_config = self.config.get('wallets', [])
        if not wallets_config:
            raise ValueError("No wallets configured")
        self.multi_wallet_manager = MultiWalletManager(wallets_config, self.config)
        connected_wallets = self.multi_wallet_manager.connect_all_wallets()
        if not connected_wallets:
            raise ConnectionError("Failed to connect to any wallet")
        auto_select = self.config.get('wallet_selection', {}).get('auto_select_funded', True)
        selected_wallet = self.multi_wallet_manager.select_best_wallet(prefer_funded=auto_select)
        if not selected_wallet:
            raise ValueError("No wallet could be selected")
        # Solana wallets don't have a w3 attribute
        self.w3 = selected_wallet.get('w3')
        self.active_wallet_info = selected_wallet
        logger.info("\U0001F310 Active Chain: %s", selected_wallet['chain_name'])
        logger.info("\U0001F4BC Active Wallet: %s", selected_wallet['address'])
        logger.info(
            "\U0001F4B0 Balance: %.4f %s",
            selected_wallet['base_balance'],
            selected_wallet['base_symbol']
        )
        logger.info("\U0001F4B5 USDC: $%.2f", selected_wallet['usdc_balance'])

    def run(self):
        """Main bot loop."""
        logger.info("\U0001F680 Starting Token Scalper Bot")
        logger.info("=" * 60)
        scan_interval = self.config.get('monitoring', {}).get('scan_interval_seconds', 30)
        iteration_count = 0
        try:
            while True:
                iteration_count += 1
                logger.debug("Iteration %d", iteration_count)

                # 1. Scan for new token launches
                new_tokens = self.scan_for_new_launches()
                for token_address in new_tokens:
                    if token_address in self.blacklisted_tokens:
                        logger.debug("Skipping blacklisted token: %s", token_address)
                        continue
                    if token_address in self.active_positions:
                        continue
                    analysis = self.analyze_token(token_address)
                    if self.should_buy_token(analysis):
                        buy_amount = self.config.get('trading', {}).get('buy_amount_eth', 0.1)
                        logger.info("\U0001F6D2 Buying token %s (amount: %s)", token_address, buy_amount)
                        result = self.buy_token(token_address, buy_amount)
                        if result.get('success'):
                            self.active_positions[token_address] = {
                                'token_address': token_address,
                                'buy_amount': buy_amount,
                                'buy_time': time.time(),
                                'buy_txid': result.get('txid'),
                                'analysis': analysis,
                                'highest_multiplier': 1.0,
                            }
                            self.send_ui_alert(
                                'buy', token_address, 'info',
                                f"Bought {buy_amount} worth of {token_address}"
                            )

                # 2. Monitor active positions
                self.monitor_positions()

                # 3. Check base currency re-entry opportunities
                self.check_base_currency_opportunities()

                time.sleep(scan_interval)
        except KeyboardInterrupt:
            logger.info("\n\U0001F6D1 Bot stopped by user")
        except Exception as exc:
            logger.error("Fatal error in bot loop: %s", exc)
            raise

    def send_ui_alert(self, alert_type, token_address, severity, details):
        """Send alert to UI and Twitter bot with chain info."""
        alert = {
            "alert_type": alert_type,
            "chain": self.active_wallet_info.get("chain_name", "Unknown"),
            "wallet": self.active_wallet_info.get("address", "Unknown"),
            "token_address": token_address,
            "severity": severity,
            "details": details,
            "timestamp": time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
        }
        send_alert_to_webhooks(alert)
        logger.info(f"UI Alert sent: {alert}")

    def buy_token(self, token_address: str, amount: float):
        """Unified buy logic for EVM and Solana."""
        if self.active_wallet_info.get('chain_name') == 'Solana':
            trader = SolDexTrader(
                self.active_wallet_info['rpc_url'],
                self.active_wallet_info['sol_keypair']
            )
            result = trader.buy_token(token_address, amount)
            self.send_ui_alert('buy', token_address, 'info', f"Bought {amount} SOL worth of {token_address} (Solana)")
            return result
        else:
            dex_router = self.active_wallet_info.get('chain_config', {}).get('dex_router')
            if not dex_router:
                logger.error("No DEX router configured for chain %s", self.active_wallet_info.get('chain_name'))
                return {"success": False, "error": "No DEX router configured"}
            trader = EVMDexTrader(
                self.active_wallet_info['w3'],
                self.active_wallet_info['account'],
                dex_router
            )
            result = trader.buy_token(token_address, amount)
            self.send_ui_alert('buy', token_address, 'info', f"Bought {amount} ETH worth of {token_address} (EVM)")
            return result

    def sell_token(self, token_address: str, amount: float):
        """Unified sell logic for EVM and Solana."""
        if self.active_wallet_info.get('chain_name') == 'Solana':
            trader = SolDexTrader(
                self.active_wallet_info['rpc_url'],
                self.active_wallet_info['sol_keypair']
            )
            result = trader.sell_token(token_address, amount)
            self.send_ui_alert('sell', token_address, 'info', f"Sold {amount} {token_address} for SOL (Solana)")
            return result
        else:
            dex_router = self.active_wallet_info.get('chain_config', {}).get('dex_router')
            if not dex_router:
                logger.error("No DEX router configured for chain %s", self.active_wallet_info.get('chain_name'))
                return {"success": False, "error": "No DEX router configured"}
            trader = EVMDexTrader(
                self.active_wallet_info['w3'],
                self.active_wallet_info['account'],
                dex_router
            )
            result = trader.sell_token(token_address, amount)
            self.send_ui_alert('sell', token_address, 'info', f"Sold {amount} {token_address} for ETH (EVM)")
            return result

    def scan_for_new_launches(self) -> List[str]:
        """
        Scan for new token launches using the DexScreener API.
        Filters by the active chain and minimum liquidity requirements.
        Returns a list of token addresses not yet seen.
        """
        try:
            chain_name = self.active_wallet_info.get('chain_name', '')
            dex_chain = CHAIN_NAME_TO_DEXSCREENER.get(chain_name, '').lower()
            min_liquidity = self.config.get('trading', {}).get('min_liquidity_eth', 5)

            resp = requests.get(DEXSCREENER_NEW_PAIRS_URL, timeout=10)
            if resp.status_code != 200:
                logger.debug("DexScreener API returned %s", resp.status_code)
                return []

            data = resp.json()
            pairs = data.get('pairs') or data.get('data', [])
            new_tokens: List[str] = []

            for pair in pairs:
                if not isinstance(pair, dict):
                    continue
                # Filter by chain if we know ours
                if dex_chain and pair.get('chainId', '').lower() != dex_chain:
                    continue
                # Filter by liquidity
                liquidity = pair.get('liquidity', {})
                liquidity_usd = float(liquidity.get('usd', 0)) if isinstance(liquidity, dict) else 0
                if liquidity_usd < (min_liquidity * 2000):  # min_liquidity is in ETH; use ~$2000/ETH as conservative floor
                    continue
                token_address = pair.get('baseToken', {}).get('address', '')
                if not token_address:
                    continue
                if token_address in self.blacklisted_tokens:
                    continue
                if token_address not in self.active_positions and token_address not in self.monitored_tokens:
                    new_tokens.append(token_address)
                    self.monitored_tokens.append(token_address)

            if new_tokens:
                logger.info("\U0001F50D Found %d new token(s) to evaluate", len(new_tokens))
            return new_tokens

        except requests.exceptions.RequestException as exc:
            logger.debug("DexScreener request failed: %s", exc)
            return []
        except Exception as exc:
            logger.error("Error scanning for new launches: %s", exc)
            return []

    def analyze_token(self, token_address: str) -> Dict:
        """
        Analyze a token using SafetyChecker, AI analysis, and opportunity scoring.
        Returns a combined analysis dict.
        """
        logger.info("\U0001F50E Analyzing token: %s", token_address)
        analysis: Dict = {
            'token_address': token_address,
            'risk_score': 100,
            'buy_recommended': False,
            'opportunity_score': 0,
            'safety': {},
            'ai': {},
        }

        try:
            # Safety checks
            is_honeypot = self.safety_checker.check_honeypot(token_address)
            if is_honeypot:
                logger.warning("\U0001F6AB Honeypot detected: %s", token_address)
                self.blacklisted_tokens.add(token_address)
                analysis['safety']['honeypot'] = True
                return analysis
            analysis['safety']['honeypot'] = False

            liquidity = self.safety_checker.check_liquidity(token_address)
            analysis['safety']['liquidity'] = liquidity

            tax_info = self.safety_checker.get_tax_info(token_address)
            analysis['safety']['tax_info'] = tax_info

            max_buy_tax = self.config.get('trading', {}).get('max_buy_tax', 10)
            max_sell_tax = self.config.get('trading', {}).get('max_sell_tax', 10)
            if tax_info.get('buy_tax', 100) > max_buy_tax or tax_info.get('sell_tax', 100) > max_sell_tax:
                logger.warning(
                    "\U0001F6AB High tax detected for %s: buy=%s%% sell=%s%%",
                    token_address, tax_info.get('buy_tax'), tax_info.get('sell_tax')
                )
                return analysis

            # Safety results dict for scorer
            safety_results = {
                'honeypot': False,
                'liquidity': liquidity,
                'buy_tax': tax_info.get('buy_tax', 0),
                'sell_tax': tax_info.get('sell_tax', 0),
                'contract_verified': self.safety_checker.check_contract_verified(token_address),
            }

            # AI analysis (optional)
            ai_result: Optional[Dict] = None
            if self.ai_analyzer.enabled:
                ai_result = self.ai_analyzer.analyze_token_contract(token_address)
                analysis['ai'] = ai_result

            # Opportunity scoring (liquidity already in USD from check_liquidity)
            token_data = {'address': token_address, 'liquidity_usd': liquidity}
            opportunity_score, score_details = self.opportunity_scorer.score_token(
                token_data, safety_results, ai_analysis=ai_result
            )
            analysis['opportunity_score'] = opportunity_score
            analysis['score_details'] = score_details

            # Risk score: invert opportunity score
            analysis['risk_score'] = max(0, 100 - opportunity_score)

            # Buy decision: opportunity score above minimum threshold
            min_score = self.config.get('opportunity_scorer', {}).get('min_score_for_alert', 75)
            analysis['buy_recommended'] = opportunity_score >= min_score

            logger.info(
                "\U0001F4CA Token %s: opportunity=%d, risk=%d, buy=%s",
                token_address, opportunity_score, analysis['risk_score'], analysis['buy_recommended']
            )

        except Exception as exc:
            logger.error("Error analyzing token %s: %s", token_address, exc)

        return analysis

    def should_buy_token(self, analysis: Dict) -> bool:
        """Determine if a token should be bought based on analysis results."""
        if analysis.get('safety', {}).get('honeypot'):
            return False
        return analysis.get('buy_recommended', False)

    def monitor_positions(self):
        """
        Monitor active positions for profit targets, stop-losses, and rug pull risk.
        Sells positions that have hit their targets or triggered protection rules.
        """
        if not self.active_positions:
            return

        trading_cfg = self.config.get('trading', {})
        profit_target = trading_cfg.get('profit_target_percent', 50) / 100
        stop_loss = trading_cfg.get('stop_loss_percent', 30) / 100
        selling_cfg = self.config.get('selling', {})
        moonshot_keep_pct = selling_cfg.get('keep_percentage_for_moonshot', 20) / 100

        positions_to_close: List[str] = []

        for token_address, position in list(self.active_positions.items()):
            try:
                # Check rug pull risk via wallet monitor
                should_exit, exit_reason = self.wallet_monitor.should_exit_position(token_address)
                if should_exit:
                    logger.warning(
                        "\U0001F6A8 Rug pull risk for %s: %s - exiting position",
                        token_address, exit_reason
                    )
                    sell_amount = position.get('buy_amount', 0)
                    self.sell_token(token_address, sell_amount)
                    self.send_ui_alert('sell', token_address, 'critical', f"Emergency exit: {exit_reason}")
                    positions_to_close.append(token_address)
                    continue

                # Estimate current P&L using DexScreener price data
                current_multiplier = self._get_position_multiplier(token_address, position)
                if current_multiplier is None:
                    continue

                # Track highest multiplier for moonshot logic
                if current_multiplier > position.get('highest_multiplier', 1.0):
                    position['highest_multiplier'] = current_multiplier

                highest = position.get('highest_multiplier', 1.0)
                profit_pct = current_multiplier - 1.0

                # Stop-loss
                if profit_pct <= -stop_loss:
                    logger.warning(
                        "\U0001F4C9 Stop-loss triggered for %s (%.1f%% loss)",
                        token_address, profit_pct * 100
                    )
                    sell_amount = position.get('buy_amount', 0)
                    self.sell_token(token_address, sell_amount)
                    self.send_ui_alert('sell', token_address, 'warning',
                                       f"Stop-loss triggered at {profit_pct*100:.1f}%")
                    positions_to_close.append(token_address)
                    continue

                # Profit target: sell most of position, keep moonshot portion
                if profit_pct >= profit_target:
                    sell_amount = position.get('buy_amount', 0) * (1 - moonshot_keep_pct)
                    logger.info(
                        "\U0001F4C8 Profit target hit for %s (%.1f%% gain), selling %.0f%%",
                        token_address, profit_pct * 100, (1 - moonshot_keep_pct) * 100
                    )
                    self.sell_token(token_address, sell_amount)
                    self.send_ui_alert('sell', token_address, 'info',
                                       f"Profit target at {profit_pct*100:.1f}%, keeping {moonshot_keep_pct*100:.0f}% for moonshot")
                    # Update position to reflect remaining moonshot stake
                    position['buy_amount'] = position.get('buy_amount', 0) * moonshot_keep_pct
                    position['profit_taken'] = True
                    continue

                # Moonshot protection: if price has retraced 50% from peak, take remaining profits
                if highest >= 10.0 and current_multiplier < highest * 0.5:
                    logger.info(
                        "\U0001F319 Moonshot retraced 50%% from peak (%.1fx -> %.1fx), exiting",
                        highest, current_multiplier
                    )
                    sell_amount = position.get('buy_amount', 0)
                    self.sell_token(token_address, sell_amount)
                    self.send_ui_alert('sell', token_address, 'info',
                                       f"Moonshot peak retrace exit at {current_multiplier:.1f}x")
                    positions_to_close.append(token_address)

            except Exception as exc:
                logger.error("Error monitoring position %s: %s", token_address, exc)

        for token_address in positions_to_close:
            self.active_positions.pop(token_address, None)

    def _get_position_multiplier(self, token_address: str, position: Dict) -> Optional[float]:
        """
        Estimate the current value multiplier for a position using DexScreener.
        Returns None if price data is unavailable.
        """
        try:
            url = DEXSCREENER_TOKEN_URL.format(token_address)
            resp = requests.get(url, timeout=5)
            if resp.status_code != 200:
                return None
            data = resp.json()
            pairs = data.get('pairs') or []
            if not pairs:
                return None
            # Use the first pair's price change as a proxy
            pair = pairs[0]
            price_change = pair.get('priceChange', {})
            change_h1 = float(price_change.get('h1', 0))
            # Approximate multiplier from % change since entry
            buy_time = position.get('buy_time', time.time())
            age_seconds = time.time() - buy_time
            # Use h1 or h24 depending on position age
            if age_seconds < 3600:
                pct = change_h1
            else:
                pct = float(price_change.get('h24', 0))
            multiplier = 1.0 + (pct / 100.0)
            return max(0.0, multiplier)
        except Exception:
            return None

    def check_base_currency_opportunities(self):
        """
        Check if it's a good time to convert USDC back to the base currency
        (e.g. when ETH/SOL dips) using the ProfitManager trend analysis.
        """
        try:
            # Record current price for trend tracking
            self.profit_manager.record_base_currency_price()

            should_convert, amount, reason = self.profit_manager.should_convert_to_base()
            if should_convert and amount > 0:
                logger.info(
                    "\U0001F4B0 Converting %.2f USDC to base currency: %s",
                    amount, reason
                )
                self.profit_manager.convert_to_base_currency(amount, reason)
        except Exception as exc:
            logger.error("Error checking base currency opportunities: %s", exc)


def main():
    """Entry point for the bot"""
    try:
        bot = TokenScalper('config.json')
        bot.run()
    except Exception as exc:
        logger.error("Failed to start bot: %s", exc)
        raise

if __name__ == "__main__":
    main()
