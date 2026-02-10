"""
Token Opportunity Scorer
Identifies high-potential tokens worth "aping into"
"""

import logging
from typing import Dict, List, Tuple, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class TokenOpportunityScorer:
    """
    Analyzes tokens to identify high-potential opportunities
    Combines multiple factors to score "ape-worthiness"
    """
    
    def __init__(self, config: Dict):
        """
        Initialize opportunity scorer
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.scorer_config = config.get('opportunity_scorer', {})
        self.enabled = self.scorer_config.get('enabled', True)
        
        # Scoring weights
        self.weights = {
            'liquidity': self.scorer_config.get('weight_liquidity', 20),
            'safety': self.scorer_config.get('weight_safety', 25),
            'developer': self.scorer_config.get('weight_developer', 20),
            'sentiment': self.scorer_config.get('weight_sentiment', 15),
            'technical': self.scorer_config.get('weight_technical', 10),
            'community': self.scorer_config.get('weight_community', 10)
        }
        
        # Thresholds
        self.min_score_for_alert = self.scorer_config.get('min_score_for_alert', 75)
        self.excellent_score = self.scorer_config.get('excellent_score', 85)
        
        if self.enabled:
            logger.info("🎯 Token Opportunity Scorer initialized")
    
    def score_token(self, token_data: Dict, safety_results: Dict,
                   dev_reputation: Optional[Dict] = None,
                   ai_analysis: Optional[Dict] = None) -> Tuple[int, Dict]:
        """
        Calculate comprehensive opportunity score for a token
        
        Args:
            token_data: Basic token information
            safety_results: Results from safety checker
            dev_reputation: Developer reputation data
            ai_analysis: AI analysis results
            
        Returns:
            Tuple of (score, details_dict)
        """
        if not self.enabled:
            return 50, {'enabled': False}
        
        scores = {}
        reasons = []
        warnings = []
        
        # 1. Liquidity Score (0-100)
        liquidity_score, liq_reason = self._score_liquidity(token_data, safety_results)
        scores['liquidity'] = liquidity_score
        if liq_reason:
            reasons.append(liq_reason)
        
        # 2. Safety Score (0-100)
        safety_score, safety_reason = self._score_safety(safety_results)
        scores['safety'] = safety_score
        if safety_reason:
            reasons.append(safety_reason)
        
        # 3. Developer Reputation Score (0-100)
        dev_score, dev_reason = self._score_developer(dev_reputation)
        scores['developer'] = dev_score
        if dev_reason:
            if dev_score >= 60:
                reasons.append(dev_reason)
            else:
                warnings.append(dev_reason)
        
        # 4. AI Sentiment Score (0-100)
        sentiment_score, sent_reason = self._score_sentiment(ai_analysis)
        scores['sentiment'] = sentiment_score
        if sent_reason:
            reasons.append(sent_reason)
        
        # 5. Technical Score (0-100)
        technical_score, tech_reason = self._score_technical(token_data, safety_results)
        scores['technical'] = technical_score
        if tech_reason:
            reasons.append(tech_reason)
        
        # 6. Community Score (0-100)
        community_score, comm_reason = self._score_community(token_data)
        scores['community'] = community_score
        if comm_reason:
            reasons.append(comm_reason)
        
        # Calculate weighted average
        total_score = 0
        total_weight = 0
        
        for category, score in scores.items():
            weight = self.weights.get(category, 10)
            total_score += score * weight
            total_weight += weight
        
        final_score = int(total_score / total_weight) if total_weight > 0 else 50
        
        # Determine rating
        if final_score >= self.excellent_score:
            rating = 'excellent'
            rating_emoji = '🌟'
        elif final_score >= self.min_score_for_alert:
            rating = 'good'
            rating_emoji = '✅'
        elif final_score >= 60:
            rating = 'moderate'
            rating_emoji = '👌'
        elif final_score >= 40:
            rating = 'low'
            rating_emoji = '⚠️'
        else:
            rating = 'poor'
            rating_emoji = '❌'
        
        details = {
            'final_score': final_score,
            'rating': rating,
            'rating_emoji': rating_emoji,
            'category_scores': scores,
            'reasons': reasons,
            'warnings': warnings,
            'is_ape_worthy': final_score >= self.min_score_for_alert,
            'timestamp': datetime.now().isoformat()
        }
        
        logger.info(f"{rating_emoji} Token scored: {final_score}/100 ({rating})")
        
        return final_score, details
    
    def _score_liquidity(self, token_data: Dict, safety_results: Dict) -> Tuple[int, str]:
        """Score based on liquidity"""
        liquidity = safety_results.get('liquidity_eth', 0)
        
        if liquidity >= 50:
            return 100, f"Excellent liquidity: {liquidity:.1f} ETH"
        elif liquidity >= 20:
            return 85, f"Strong liquidity: {liquidity:.1f} ETH"
        elif liquidity >= 10:
            return 70, f"Good liquidity: {liquidity:.1f} ETH"
        elif liquidity >= 5:
            return 50, f"Moderate liquidity: {liquidity:.1f} ETH"
        elif liquidity >= 2:
            return 30, f"Low liquidity: {liquidity:.1f} ETH"
        else:
            return 10, f"Very low liquidity: {liquidity:.1f} ETH"
    
    def _score_safety(self, safety_results: Dict) -> Tuple[int, str]:
        """Score based on safety checks"""
        if not safety_results.get('safe', False):
            return 20, "Failed safety checks"
        
        score = 60  # Base score for passing
        reason_parts = []
        
        # Bonus for verified contract
        if safety_results.get('contract_verified', False):
            score += 15
            reason_parts.append("verified contract")
        
        # Bonus for low taxes
        buy_tax = safety_results.get('buy_tax', 100)
        sell_tax = safety_results.get('sell_tax', 100)
        
        if buy_tax <= 3 and sell_tax <= 3:
            score += 15
            reason_parts.append("low taxes")
        elif buy_tax <= 5 and sell_tax <= 5:
            score += 10
            reason_parts.append("reasonable taxes")
        
        # Penalty for honeypot
        if safety_results.get('is_honeypot', False):
            return 5, "Honeypot detected"
        
        reason = f"Passed safety checks" + (f" with {', '.join(reason_parts)}" if reason_parts else "")
        return min(100, score), reason
    
    def _score_developer(self, dev_reputation: Optional[Dict]) -> Tuple[int, str]:
        """Score based on developer reputation"""
        if not dev_reputation:
            return 50, "Unknown developer"
        
        rep_score = dev_reputation.get('reputation_score', 50)
        rug_count = dev_reputation.get('rug_pull_count', 0)
        scam_count = dev_reputation.get('scam_count', 0)
        successful = dev_reputation.get('successful_projects', 0)
        
        if rug_count > 0:
            return 5, f"Developer has {rug_count} rug pulls"
        
        if scam_count > 1:
            return 15, f"Developer has {scam_count} scams"
        
        if successful >= 3:
            return 95, f"Experienced developer with {successful} successful projects"
        elif successful >= 1:
            return 75, f"Developer has {successful} successful project(s)"
        elif rep_score >= 70:
            return 65, f"Good developer reputation ({rep_score}/100)"
        elif rep_score >= 50:
            return 50, f"Average developer reputation ({rep_score}/100)"
        else:
            return 30, f"Low developer reputation ({rep_score}/100)"
    
    def _score_sentiment(self, ai_analysis: Optional[Dict]) -> Tuple[int, str]:
        """Score based on AI sentiment analysis"""
        if not ai_analysis or not ai_analysis.get('ai_enabled', False):
            return 50, None
        
        sentiment = ai_analysis.get('ai_sentiment', {})
        sentiment_score = sentiment.get('sentiment_score', 50)
        
        if sentiment_score >= 75:
            return 90, f"Very positive sentiment ({sentiment_score}/100)"
        elif sentiment_score >= 60:
            return 70, f"Positive sentiment ({sentiment_score}/100)"
        elif sentiment_score >= 40:
            return 50, f"Neutral sentiment ({sentiment_score}/100)"
        else:
            return 30, f"Negative sentiment ({sentiment_score}/100)"
    
    def _score_technical(self, token_data: Dict, safety_results: Dict) -> Tuple[int, str]:
        """Score based on technical indicators"""
        score = 50  # Base score
        reasons = []
        
        # Holder count
        holders = safety_results.get('holder_count', 0)
        if holders >= 1000:
            score += 25
            reasons.append(f"{holders} holders")
        elif holders >= 500:
            score += 20
            reasons.append(f"{holders} holders")
        elif holders >= 100:
            score += 10
        
        # Contract age
        age = safety_results.get('contract_age', 0)
        if age >= 7 * 24 * 3600:  # 1 week
            score += 15
            reasons.append("mature contract")
        elif age >= 24 * 3600:  # 1 day
            score += 10
        
        reason = "Good technical indicators: " + ", ".join(reasons) if reasons else None
        return min(100, score), reason
    
    def _score_community(self, token_data: Dict) -> Tuple[int, str]:
        """Score based on community indicators"""
        # Placeholder for future community metrics
        # Could include: Twitter followers, Telegram members, Discord activity, etc.
        return 50, None
    
    def is_ape_worthy(self, token_data: Dict, safety_results: Dict,
                     dev_reputation: Optional[Dict] = None,
                     ai_analysis: Optional[Dict] = None) -> Tuple[bool, int, List[str]]:
        """
        Determine if a token is worth "aping into"
        
        Returns:
            Tuple of (is_worthy, score, reasons)
        """
        score, details = self.score_token(token_data, safety_results, 
                                         dev_reputation, ai_analysis)
        
        is_worthy = details['is_ape_worthy']
        reasons = details['reasons']
        
        return is_worthy, score, reasons
