"""
AI-Powered Token Analysis Module
Uses AI APIs to analyze tokens for safety, sentiment, and profit potential
"""

import logging
import requests
import json
from typing import Dict, Optional, List
from datetime import datetime

logger = logging.getLogger(__name__)


class AITokenAnalyzer:
    """
    AI-powered token analyzer that provides intelligent risk assessment
    and sentiment analysis for token trading decisions
    """
    
    def __init__(self, config: Dict):
        """
        Initialize AI analyzer with configuration
        
        Args:
            config: Configuration dictionary containing AI settings
        """
        self.config = config
        self.ai_config = config.get('ai_analysis', {})
        self.enabled = self.ai_config.get('enabled', False)
        self.api_provider = self.ai_config.get('provider', 'openai')
        self.api_key = self.ai_config.get('api_key', '')
        self.model = self.ai_config.get('model', 'gpt-4')
        self.max_tokens = self.ai_config.get('max_tokens', 500)
        
        if self.enabled and not self.api_key:
            logger.warning("⚠️ AI analysis enabled but no API key provided")
            self.enabled = False
        elif self.enabled:
            logger.info(f"🤖 AI Token Analyzer initialized with {self.api_provider}")
    
    def analyze_token_contract(self, token_address: str, contract_code: Optional[str] = None) -> Dict:
        """
        Analyze token contract using AI to detect suspicious patterns
        
        Args:
            token_address: Token contract address
            contract_code: Optional contract source code
            
        Returns:
            Dictionary with analysis results including risk_score, flags, and reasoning
        """
        if not self.enabled:
            return {
                'ai_enabled': False,
                'risk_score': 50,  # Neutral score
                'analysis': 'AI analysis disabled'
            }
        
        try:
            # Prepare analysis prompt
            prompt = self._create_contract_analysis_prompt(token_address, contract_code)
            
            # Call AI API
            response = self._call_ai_api(prompt)
            
            # Parse response
            analysis = self._parse_analysis_response(response)
            
            logger.info(f"🤖 AI Risk Score for {token_address}: {analysis.get('risk_score', 'N/A')}/100")
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error in AI contract analysis: {e}")
            return {
                'ai_enabled': True,
                'error': str(e),
                'risk_score': 50,  # Neutral on error
                'analysis': 'Analysis failed'
            }
    
    def analyze_social_sentiment(self, token_address: str, token_name: str = '') -> Dict:
        """
        Analyze social media sentiment for a token
        
        Args:
            token_address: Token contract address
            token_name: Optional token name for better search
            
        Returns:
            Dictionary with sentiment analysis including score and signals
        """
        if not self.enabled:
            return {
                'ai_enabled': False,
                'sentiment_score': 50,
                'analysis': 'AI sentiment analysis disabled'
            }
        
        try:
            # Create sentiment analysis prompt
            prompt = f"""Analyze the potential social sentiment and community signals for a cryptocurrency token.
            
Token Address: {token_address}
Token Name: {token_name or 'Unknown'}

Based on typical patterns in crypto launches, provide:
1. Estimated sentiment score (0-100, where 0 is very negative, 100 is very positive)
2. Key factors to consider (hype indicators, community size, social presence)
3. Red flags or positive signals
4. Recommendation (buy, avoid, or monitor)

Provide your analysis in JSON format:
{{
    "sentiment_score": <0-100>,
    "community_strength": <weak/moderate/strong>,
    "hype_level": <low/medium/high>,
    "red_flags": [<list of concerns>],
    "positive_signals": [<list of positive indicators>],
    "recommendation": <buy/avoid/monitor>,
    "reasoning": "<brief explanation>"
}}"""
            
            response = self._call_ai_api(prompt)
            analysis = self._parse_sentiment_response(response)
            
            logger.info(f"🤖 AI Sentiment for {token_name or token_address}: {analysis.get('sentiment_score', 'N/A')}/100")
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error in AI sentiment analysis: {e}")
            return {
                'ai_enabled': True,
                'error': str(e),
                'sentiment_score': 50,
                'analysis': 'Sentiment analysis failed'
            }
    
    def get_trading_recommendation(self, token_data: Dict) -> Dict:
        """
        Get AI-powered trading recommendation based on multiple data points
        
        Args:
            token_data: Dictionary containing token information (address, liquidity, taxes, etc.)
            
        Returns:
            Dictionary with recommendation and confidence level
        """
        if not self.enabled:
            return {
                'ai_enabled': False,
                'recommendation': 'neutral',
                'confidence': 0,
                'analysis': 'AI recommendations disabled'
            }
        
        try:
            prompt = f"""Analyze this cryptocurrency token and provide a trading recommendation.

Token Data:
{json.dumps(token_data, indent=2)}

Provide a recommendation in JSON format:
{{
    "recommendation": <buy/avoid/monitor>,
    "confidence": <0-100>,
    "risk_level": <low/medium/high>,
    "profit_potential": <low/medium/high>,
    "key_factors": [<list of important factors>],
    "warnings": [<list of warnings if any>],
    "reasoning": "<detailed explanation>"
}}"""
            
            response = self._call_ai_api(prompt)
            recommendation = self._parse_recommendation_response(response)
            
            logger.info(f"🤖 AI Recommendation: {recommendation.get('recommendation', 'N/A')} (confidence: {recommendation.get('confidence', 0)}%)")
            
            return recommendation
            
        except Exception as e:
            logger.error(f"Error getting AI recommendation: {e}")
            return {
                'ai_enabled': True,
                'error': str(e),
                'recommendation': 'neutral',
                'confidence': 0,
                'analysis': 'Recommendation generation failed'
            }
    
    def _create_contract_analysis_prompt(self, token_address: str, contract_code: Optional[str]) -> str:
        """Create prompt for contract analysis"""
        prompt = f"""Analyze this cryptocurrency token contract for potential risks and red flags.

Token Address: {token_address}

"""
        if contract_code:
            prompt += f"Contract Code:\n{contract_code[:2000]}...\n\n"  # Limit code length
        
        prompt += """Analyze for:
1. Honeypot indicators (can buy but cannot sell)
2. Hidden mint functions
3. Excessive taxes or fees
4. Ownership concentration risks
5. Rug pull mechanisms (liquidity withdrawal, etc.)
6. Blacklist/whitelist functions
7. Pausable transfers

Provide analysis in JSON format:
{
    "risk_score": <0-100, where 0 is safest, 100 is most dangerous>,
    "risk_level": <low/medium/high/critical>,
    "red_flags": [<list of specific concerns>],
    "safe_features": [<list of positive security features>],
    "recommendation": <safe/caution/avoid>,
    "reasoning": "<brief explanation>"
}"""
        return prompt
    
    def _call_ai_api(self, prompt: str) -> str:
        """
        Call AI API with the given prompt
        
        Args:
            prompt: The prompt to send to AI
            
        Returns:
            AI response text
        """
        if self.api_provider == 'openai':
            return self._call_openai(prompt)
        elif self.api_provider == 'anthropic':
            return self._call_anthropic(prompt)
        else:
            raise ValueError(f"Unsupported AI provider: {self.api_provider}")
    
    def _call_openai(self, prompt: str) -> str:
        """Call OpenAI API"""
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "You are an expert cryptocurrency token analyzer specializing in detecting scams, rug pulls, and assessing token safety."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": self.max_tokens,
            "temperature": 0.3  # Lower temperature for more consistent analysis
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        return result['choices'][0]['message']['content']
    
    def _call_anthropic(self, prompt: str) -> str:
        """Call Anthropic Claude API"""
        url = "https://api.anthropic.com/v1/messages"
        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
        
        data = {
            "model": self.model,
            "max_tokens": self.max_tokens,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "system": "You are an expert cryptocurrency token analyzer specializing in detecting scams, rug pulls, and assessing token safety."
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        return result['content'][0]['text']
    
    def _parse_analysis_response(self, response: str) -> Dict:
        """Parse contract analysis response"""
        try:
            # Try to extract JSON from response
            start_idx = response.find('{')
            end_idx = response.rfind('}') + 1
            
            if start_idx >= 0 and end_idx > start_idx:
                json_str = response[start_idx:end_idx]
                data = json.loads(json_str)
                data['ai_enabled'] = True
                return data
        except Exception as e:
            logger.warning(f"Failed to parse JSON from AI response: {e}")
        
        # Fallback parsing
        return {
            'ai_enabled': True,
            'risk_score': 50,
            'analysis': response,
            'parsed': False
        }
    
    def _parse_sentiment_response(self, response: str) -> Dict:
        """Parse sentiment analysis response"""
        try:
            start_idx = response.find('{')
            end_idx = response.rfind('}') + 1
            
            if start_idx >= 0 and end_idx > start_idx:
                json_str = response[start_idx:end_idx]
                data = json.loads(json_str)
                data['ai_enabled'] = True
                return data
        except Exception as e:
            logger.warning(f"Failed to parse JSON from sentiment response: {e}")
        
        return {
            'ai_enabled': True,
            'sentiment_score': 50,
            'analysis': response,
            'parsed': False
        }
    
    def _parse_recommendation_response(self, response: str) -> Dict:
        """Parse trading recommendation response"""
        try:
            start_idx = response.find('{')
            end_idx = response.rfind('}') + 1
            
            if start_idx >= 0 and end_idx > start_idx:
                json_str = response[start_idx:end_idx]
                data = json.loads(json_str)
                data['ai_enabled'] = True
                return data
        except Exception as e:
            logger.warning(f"Failed to parse JSON from recommendation response: {e}")
        
        return {
            'ai_enabled': True,
            'recommendation': 'neutral',
            'confidence': 0,
            'analysis': response,
            'parsed': False
        }
