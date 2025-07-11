"""
DeepL Translator Plugin

Implementation of translation service using DeepL API.
"""

import logging
import asyncio
from typing import List, Optional, Dict, Any
import time

import deepl

from ...interfaces.services.translation_service_interface import (
    TranslationServiceInterface, LanguageDetectionResult
)
from ...domain.entities.translation import TranslationProvider


class DeepLTranslator(TranslationServiceInterface):
    """DeepL translation service implementation."""
    
    def __init__(self, api_key: str, is_pro: bool = False):
        """Initialize DeepL translator with API key."""
        self.api_key = api_key
        self.is_pro = is_pro
        self.client = None
        self.logger = logging.getLogger(__name__)
        self._initialize_client()
    
    def _initialize_client(self) -> None:
        """Initialize DeepL client."""
        try:
            self.client = deepl.Translator(self.api_key)
            self.logger.info("DeepL client initialized successfully")
        except Exception as e:
            self.logger.error(f"Failed to initialize DeepL client: {str(e)}")
            self.client = None
    
    async def translate_text(self, text: str, target_language: str, 
                           source_language: Optional[str] = None) -> str:
        """Translate a single text."""
        if not self.client:
            raise Exception("DeepL client not initialized")
        
        try:
            # Convert language codes to DeepL format
            target_lang = self._convert_to_deepl_code(target_language)
            source_lang = self._convert_to_deepl_code(source_language) if source_language else None
            
            # Perform translation
            result = self.client.translate_text(
                text, 
                target_lang=target_lang,
                source_lang=source_lang
            )
            
            return result.text
            
        except Exception as e:
            self.logger.error(f"Translation failed: {str(e)}")
            raise Exception(f"DeepL translation failed: {str(e)}")
    
    async def translate_batch(self, texts: List[str], target_language: str,
                            source_language: Optional[str] = None) -> List[str]:
        """Translate multiple texts in a batch."""
        if not self.client:
            raise Exception("DeepL client not initialized")
        
        try:
            # Convert language codes
            target_lang = self._convert_to_deepl_code(target_language)
            source_lang = self._convert_to_deepl_code(source_language) if source_language else None
            
            # DeepL supports batch translation
            results = self.client.translate_text(
                texts,
                target_lang=target_lang,
                source_lang=source_lang
            )
            
            # Extract translated texts
            if isinstance(results, list):
                return [result.text for result in results]
            else:
                return [results.text]
                
        except Exception as e:
            self.logger.error(f"Batch translation failed: {str(e)}")
            raise Exception(f"DeepL batch translation failed: {str(e)}")
    
    async def detect_language(self, text: str) -> LanguageDetectionResult:
        """Detect the language of given text."""
        if not self.client:
            raise Exception("DeepL client not initialized")
        
        try:
            # DeepL doesn't have a separate language detection API
            # We'll attempt translation with auto-detect and check the detected language
            result = self.client.translate_text(text, target_lang="EN")
            
            # Extract detected source language
            detected_lang = result.detected_source_lang
            confidence = 0.9 if detected_lang else 0.0
            
            return LanguageDetectionResult(
                language_code=detected_lang.lower() if detected_lang else "unknown",
                confidence=confidence
            )
            
        except Exception as e:
            self.logger.error(f"Language detection failed: {str(e)}")
            return LanguageDetectionResult("unknown", 0.0)
    
    async def get_supported_languages(self) -> List[str]:
        """Get list of supported language codes."""
        if not self.client:
            return []
        
        try:
            # Get source and target languages
            source_langs = self.client.get_source_languages()
            target_langs = self.client.get_target_languages()
            
            # Combine and convert to standard codes
            all_langs = set()
            for lang in source_langs:
                all_langs.add(lang.code.lower())
            for lang in target_langs:
                all_langs.add(lang.code.lower())
            
            return list(all_langs)
            
        except Exception as e:
            self.logger.error(f"Failed to get supported languages: {str(e)}")
            return ['en', 'ja', 'vi', 'zh', 'ko', 'es', 'fr', 'de', 'it', 'pt', 'ru']
    
    async def get_usage_statistics(self) -> Dict[str, Any]:
        """Get API usage statistics."""
        if not self.client:
            return {}
        
        try:
            usage = self.client.get_usage()
            
            return {
                'character_count': usage.character.count,
                'character_limit': usage.character.limit,
                'character_remaining': usage.character.limit - usage.character.count,
                'usage_percentage': (usage.character.count / usage.character.limit) * 100 if usage.character.limit else 0,
                'is_pro_account': self.is_pro
            }
            
        except Exception as e:
            self.logger.error(f"Failed to get usage statistics: {str(e)}")
            return {}
    
    async def validate_api_key(self) -> bool:
        """Validate if API key is valid and working."""
        try:
            if not self.client:
                return False
            
            # Try to get usage information as a validation test
            usage = self.client.get_usage()
            return True
            
        except Exception as e:
            self.logger.error(f"API key validation failed: {str(e)}")
            return False
    
    def get_provider(self) -> TranslationProvider:
        """Get the translation provider type."""
        return TranslationProvider.DEEPL
    
    async def estimate_cost(self, character_count: int) -> float:
        """Estimate cost for translating given number of characters."""
        # DeepL pricing (approximate, may vary)
        if self.is_pro:
            # Pro: $25 per 1M characters
            cost_per_char = 25.0 / 1000000
        else:
            # Free: 500,000 characters per month free
            cost_per_char = 0.0  # Free tier
        
        return character_count * cost_per_char
    
    async def get_rate_limits(self) -> Dict[str, Any]:
        """Get current rate limit information."""
        # DeepL rate limits (approximate)
        if self.is_pro:
            return {
                'requests_per_second': 10,
                'characters_per_month': 1000000,
                'max_text_length': 130000,
                'max_batch_size': 50
            }
        else:
            return {
                'requests_per_second': 5,
                'characters_per_month': 500000,
                'max_text_length': 5000,
                'max_batch_size': 25
            }
    
    def is_available(self) -> bool:
        """Check if service is currently available."""
        return self.client is not None
    
    async def health_check(self) -> Dict[str, Any]:
        """Perform health check on the service."""
        try:
            start_time = time.time()
            
            # Test with a simple translation
            result = await self.translate_text("Hello", "ja")
            
            end_time = time.time()
            response_time = end_time - start_time
            
            return {
                'status': 'healthy',
                'response_time_ms': response_time * 1000,
                'api_accessible': True,
                'test_translation_success': bool(result),
                'timestamp': time.time()
            }
            
        except Exception as e:
            return {
                'status': 'unhealthy',
                'error': str(e),
                'api_accessible': False,
                'test_translation_success': False,
                'timestamp': time.time()
            }
    
    def _convert_to_deepl_code(self, language_code: str) -> str:
        """Convert standard language code to DeepL format."""
        if not language_code:
            return language_code
        
        # DeepL uses uppercase codes and specific formats
        mapping = {
            'en': 'EN',
            'ja': 'JA',
            'vi': 'VI',  # Check if DeepL supports Vietnamese
            'zh': 'ZH',
            'ko': 'KO',
            'es': 'ES',
            'fr': 'FR',
            'de': 'DE',
            'it': 'IT',
            'pt': 'PT',
            'ru': 'RU',
            'ar': 'AR',
            'hi': 'HI',
            'th': 'TH',
            'id': 'ID',
            'ms': 'MS',
            'tl': 'TL'
        }
        
        return mapping.get(language_code.lower(), language_code.upper())
    
    def _convert_from_deepl_code(self, deepl_code: str) -> str:
        """Convert DeepL language code to standard format."""
        if not deepl_code:
            return deepl_code
        
        # Reverse mapping
        mapping = {
            'EN': 'en',
            'JA': 'ja',
            'VI': 'vi',
            'ZH': 'zh',
            'KO': 'ko',
            'ES': 'es',
            'FR': 'fr',
            'DE': 'de',
            'IT': 'it',
            'PT': 'pt',
            'RU': 'ru',
            'AR': 'ar',
            'HI': 'hi',
            'TH': 'th',
            'ID': 'id',
            'MS': 'ms',
            'TL': 'tl'
        }
        
        return mapping.get(deepl_code.upper(), deepl_code.lower())
