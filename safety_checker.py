"""
Safety checks module for token analysis
Enhanced with AI-powered risk assessment
"""

import logging
from typing import Dict, Optional
from ai_analyzer import AITokenAnalyzer

logger = logging.getLogger(__name__)


class SafetyChecker:
    """Performs safety checks on tokens before buying"""
    
    def __init__(self, w3, config: Dict):
        self.w3 = w3
        self.config = config
        # Initialize AI analyzer
        self.ai_analyzer = AITokenAnalyzer(config)
        
    def check_honeypot(self, token_address: str) -> bool:
        """
        Check if token is a honeypot (can buy but not sell)
        Returns True if honeypot detected
        """
        try:
            # In a real implementation, this would:
            # 1. Simulate a buy transaction
            # 2. Simulate a sell transaction
            # 3. Compare gas usage and success
            # 4. Check for blacklist functions
            # 5. Verify transfer restrictions
            
            logger.info(f"Checking honeypot status for {token_address}")
            return False
            
        except Exception as e:
            logger.error(f"Error checking honeypot: {e}")
            return True  # Assume unsafe if check fails
            
    def check_liquidity(self, token_address: str) -> float:
        """
        Check liquidity pool size in ETH
        Returns liquidity amount
        """
        try:
            # In a real implementation, this would:
            # 1. Get pair address from factory
            # 2. Query pair reserves
            # 3. Calculate ETH liquidity
            
            logger.info(f"Checking liquidity for {token_address}")
            return 0.0
            
        except Exception as e:
            logger.error(f"Error checking liquidity: {e}")
            return 0.0
            
    def get_tax_info(self, token_address: str) -> Dict[str, float]:
        """
        Get buy and sell tax percentages
        Returns dict with buy_tax and sell_tax
        """
        try:
            # In a real implementation, this would:
            # 1. Simulate buy and sell
            # 2. Compare expected vs actual tokens
            # 3. Calculate tax percentages
            
            logger.info(f"Checking taxes for {token_address}")
            return {
                'buy_tax': 0.0,
                'sell_tax': 0.0
            }
            
        except Exception as e:
            logger.error(f"Error getting tax info: {e}")
            return {
                'buy_tax': 100.0,  # Assume unsafe if check fails
                'sell_tax': 100.0
            }
            
    def check_contract_verified(self, token_address: str) -> bool:
        """
        Check if contract is verified on block explorer
        Returns True if verified
        """
        try:
            # In a real implementation, this would:
            # 1. Query Etherscan/BSCscan API
            # 2. Check verification status
            
            logger.info(f"Checking verification for {token_address}")
            return False
            
        except Exception as e:
            logger.error(f"Error checking verification: {e}")
            return False
            
    def get_holder_count(self, token_address: str) -> int:
        """
        Get number of token holders
        Returns holder count
        """
        try:
            # In a real implementation, this would:
            # 1. Query block explorer API
            # 2. Get holder count from contract
            
            logger.info(f"Checking holder count for {token_address}")
            return 0
            
        except Exception as e:
            logger.error(f"Error getting holder count: {e}")
            return 0
            
    def check_contract_age(self, token_address: str) -> int:
        """
        Get contract age in seconds
        Returns age in seconds
        """
        try:
            # In a real implementation, this would:
            # 1. Get contract creation transaction
            # 2. Calculate time since creation
            
            logger.info(f"Checking contract age for {token_address}")
            return 0
            
        except Exception as e:
            logger.error(f"Error checking contract age: {e}")
            return 0
            
    def perform_full_check(self, token_address: str, token_name: str = '') -> Dict:
        """
        Perform all safety checks and return results
        Enhanced with AI-powered analysis
        """
        logger.info(f"Performing full safety check for {token_address}")
        
        results = {
            'address': token_address,
            'is_honeypot': self.check_honeypot(token_address),
            'liquidity_eth': self.check_liquidity(token_address),
            'contract_verified': self.check_contract_verified(token_address),
            'holder_count': self.get_holder_count(token_address),
            'contract_age': self.check_contract_age(token_address),
        }
        
        # Get tax info
        tax_info = self.get_tax_info(token_address)
        results.update(tax_info)
        
        # AI-powered analysis
        if self.ai_analyzer.enabled:
            logger.info(f"🤖 Running AI analysis for {token_address}")
            
            # Contract risk analysis
            ai_contract_analysis = self.ai_analyzer.analyze_token_contract(token_address)
            results['ai_contract_analysis'] = ai_contract_analysis
            
            # Sentiment analysis
            ai_sentiment = self.ai_analyzer.analyze_social_sentiment(token_address, token_name)
            results['ai_sentiment'] = ai_sentiment
            
            # Get comprehensive trading recommendation
            token_data = {
                'address': token_address,
                'name': token_name,
                'liquidity_eth': results['liquidity_eth'],
                'buy_tax': results['buy_tax'],
                'sell_tax': results['sell_tax'],
                'holder_count': results['holder_count'],
                'contract_verified': results['contract_verified'],
                'is_honeypot': results['is_honeypot']
            }
            ai_recommendation = self.ai_analyzer.get_trading_recommendation(token_data)
            results['ai_recommendation'] = ai_recommendation
            
            # Store AI risk score
            results['ai_risk_score'] = ai_contract_analysis.get('risk_score', 50)
            results['ai_sentiment_score'] = ai_sentiment.get('sentiment_score', 50)
        
        # Determine if safe (traditional checks)
        min_liquidity = self.config['trading']['min_liquidity_eth']
        max_buy_tax = self.config['trading']['max_buy_tax']
        max_sell_tax = self.config['trading']['max_sell_tax']
        min_holders = self.config['monitoring']['min_holder_count']
        
        traditional_safe = (
            not results['is_honeypot'] and
            results['liquidity_eth'] >= min_liquidity and
            results['buy_tax'] <= max_buy_tax and
            results['sell_tax'] <= max_sell_tax and
            results['holder_count'] >= min_holders
        )
        
        # Enhanced safety check with AI (if enabled)
        if self.ai_analyzer.enabled and 'ai_recommendation' in results:
            ai_rec = results['ai_recommendation'].get('recommendation', 'neutral')
            ai_risk = results.get('ai_risk_score', 50)
            
            # Get risk threshold from config
            risk_threshold = self.ai_analyzer.ai_config.get('risk_threshold', 70)
            
            # Consider AI recommendation in final decision
            # Token is safe if traditional checks pass AND AI doesn't recommend avoiding
            # Also check AI risk score is acceptable (< risk_threshold)
            results['safe'] = traditional_safe and ai_rec != 'avoid' and ai_risk < risk_threshold
            results['ai_enhanced'] = True
            
            if not results['safe'] and traditional_safe:
                logger.warning(f"⚠️ AI analysis flagged token {token_address} as risky despite passing traditional checks (risk: {ai_risk}, threshold: {risk_threshold})")
        else:
            results['safe'] = traditional_safe
            results['ai_enhanced'] = False
        
        return results
