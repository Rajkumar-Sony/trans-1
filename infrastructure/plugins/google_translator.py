"""
Google Translator Plugin

Implementation of translation service using Google Translate API.
"""

import logging
import asyncio
from typing import List, Optional, Dict, Any
import time

try:
    from google.cloud import translate_v2 as translate
    from google.oauth2 import service_account
    GOOGLE_AVAILABLE = True
except ImportError:
    GOOGLE_AVAILABLE = False

from ...interfaces.services.translation_service_interface import (
    TranslationServiceInterface, LanguageDetectionResult
)
from ...domain.entities.translation import TranslationProvider


class GoogleTranslator(TranslationServiceInterface):
    """Google Translate service implementation."""
    
    def __init__(self, credentials_path: Optional[str] = None, api_key: Optional[str] = None):
        """Initialize Google translator with credentials or API key."""
        self.credentials_path = credentials_path
        self.api_key = api_key
        self.client = None
        self.logger = logging.getLogger(__name__)
        
        if not GOOGLE_AVAILABLE:
            self.logger.error("Google Cloud Translate library not available")
            return
        
        self._initialize_client()
    
    def _initialize_client(self) -> None:
        """Initialize Google Translate client."""
        try:
            if self.credentials_path:
                # Use service account credentials
                credentials = service_account.Credentials.from_service_account_file(
                    self.credentials_path
                )
                self.client = translate.Client(credentials=credentials)
            elif self.api_key:
                # Use API key
                self.client = translate.Client(api_key=self.api_key)
            else:
                # Use default credentials
                self.client = translate.Client()
            
            self.logger.info("Google Translate client initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize Google Translate client: {str(e)}")
            self.client = None
    
    async def translate_text(self, text: str, target_language: str, 
                           source_language: Optional[str] = None) -> str:
        """Translate a single text."""
        if not self.client:
            raise Exception("Google Translate client not initialized")
        
        try:
            # Convert language codes
            target_lang = self._convert_to_google_code(target_language)
            source_lang = self._convert_to_google_code(source_language) if source_language else None
            
            # Perform translation
            result = self.client.translate(
                text,
                target_language=target_lang,
                source_language=source_lang
            )
            
            return result['translatedText']
            
        except Exception as e:
            self.logger.error(f"Translation failed: {str(e)}")
            raise Exception(f"Google Translate failed: {str(e)}")
    
    async def translate_batch(self, texts: List[str], target_language: str,
                            source_language: Optional[str] = None) -> List[str]:
        """Translate multiple texts in a batch."""
        if not self.client:
            raise Exception("Google Translate client not initialized")
        
        try:
            # Convert language codes
            target_lang = self._convert_to_google_code(target_language)
            source_lang = self._convert_to_google_code(source_language) if source_language else None
            
            # Google Translate supports batch translation
            results = self.client.translate(
                texts,
                target_language=target_lang,
                source_language=source_lang
            )
            
            # Extract translated texts
            if isinstance(results, list):
                return [result['translatedText'] for result in results]
            else:
                return [results['translatedText']]
                
        except Exception as e:
            self.logger.error(f"Batch translation failed: {str(e)}")
            raise Exception(f"Google Translate batch failed: {str(e)}")
    
    async def detect_language(self, text: str) -> LanguageDetectionResult:
        """Detect the language of given text."""
        if not self.client:
            raise Exception("Google Translate client not initialized")
        
        try:
            result = self.client.detect_language(text)
            
            language_code = result['language']
            confidence = result.get('confidence', 0.0)
            
            return LanguageDetectionResult(
                language_code=language_code.lower(),
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
            languages = self.client.get_languages()
            return [lang['language'] for lang in languages]
            
        except Exception as e:
            self.logger.error(f"Failed to get supported languages: {str(e)}")
            # Return common languages as fallback
            return [
                'en', 'ja', 'vi', 'zh', 'ko', 'es', 'fr', 'de', 'it', 'pt', 'ru',
                'ar', 'hi', 'th', 'id', 'ms', 'tl', 'nl', 'sv', 'no', 'da', 'fi'
            ]
    
    async def get_usage_statistics(self) -> Dict[str, Any]:
        """Get API usage statistics."""
        # Google Translate doesn't provide usage statistics via API
        # Return placeholder information
        return {
            'provider': 'Google Translate',
            'note': 'Usage statistics not available via API',
            'check_console': 'Please check Google Cloud Console for usage details'
        }
    
    async def validate_api_key(self) -> bool:
        """Validate if API key/credentials are valid and working."""
        try:
            if not self.client:
                return False
            
            # Try a simple operation to validate credentials
            test_result = self.client.detect_language("Hello")
            return True
            
        except Exception as e:
            self.logger.error(f"API validation failed: {str(e)}")
            return False
    
    def get_provider(self) -> TranslationProvider:
        """Get the translation provider type."""
        return TranslationProvider.GOOGLE
    
    async def estimate_cost(self, character_count: int) -> float:
        """Estimate cost for translating given number of characters."""
        # Google Translate pricing (approximate, may vary)
        # Basic: $20 per 1M characters
        # Advanced: $100 per 1M characters
        # Using Basic pricing as default
        cost_per_char = 20.0 / 1000000
        return character_count * cost_per_char
    
    async def get_rate_limits(self) -> Dict[str, Any]:
        """Get current rate limit information."""
        # Google Translate rate limits (approximate)
        return {
            'requests_per_second': 100,
            'characters_per_request': 30000,
            'characters_per_month': 'unlimited',  # Depends on billing
            'max_text_length': 30000,
            'max_batch_size': 100
        }
    
    def is_available(self) -> bool:
        """Check if service is currently available."""
        return self.client is not None and GOOGLE_AVAILABLE
    
    async def health_check(self) -> Dict[str, Any]:
        """Perform health check on the service."""
        try:
            if not GOOGLE_AVAILABLE:
                return {
                    'status': 'unavailable',
                    'error': 'Google Cloud Translate library not installed',
                    'api_accessible': False,
                    'timestamp': time.time()
                }
            
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
    
    def _convert_to_google_code(self, language_code: str) -> str:
        """Convert standard language code to Google Translate format."""
        if not language_code:
            return language_code
        
        # Google Translate uses lowercase codes
        mapping = {
            'en': 'en',
            'ja': 'ja',
            'vi': 'vi',
            'zh': 'zh',
            'ko': 'ko',
            'es': 'es',
            'fr': 'fr',
            'de': 'de',
            'it': 'it',
            'pt': 'pt',
            'ru': 'ru',
            'ar': 'ar',
            'hi': 'hi',
            'th': 'th',
            'id': 'id',
            'ms': 'ms',
            'tl': 'tl',
            'nl': 'nl',
            'sv': 'sv',
            'no': 'no',
            'da': 'da',
            'fi': 'fi'
        }
        
        return mapping.get(language_code.lower(), language_code.lower())
    
    @staticmethod
    def is_library_available() -> bool:
        """Check if Google Cloud Translate library is available."""
        return GOOGLE_AVAILABLE
    
    @staticmethod
    def get_installation_instructions() -> str:
        """Get installation instructions for Google Cloud Translate."""
        return (
            "To use Google Translate, install the required library:\n"
            "pip install google-cloud-translate\n\n"
            "Then set up authentication:\n"
            "1. Create a service account in Google Cloud Console\n"
            "2. Download the JSON key file\n"
            "3. Set GOOGLE_APPLICATION_CREDENTIALS environment variable\n"
            "   or provide the path to the key file when initializing"
        )
