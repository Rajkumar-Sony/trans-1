"""
Translation Service Interface

Abstract interface for translation service operations.
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any, Union
from enum import Enum

from ...domain.entities.translation import TranslationProvider


class LanguageDetectionResult:
    """Result of language detection."""
    def __init__(self, language_code: str, confidence: float):
        self.language_code = language_code
        self.confidence = confidence


class TranslationServiceInterface(ABC):
    """Interface for translation service operations."""
    
    @abstractmethod
    async def translate_text(self, text: str, target_language: str, 
                           source_language: Optional[str] = None) -> str:
        """Translate a single text."""
        pass
    
    @abstractmethod
    async def translate_batch(self, texts: List[str], target_language: str,
                            source_language: Optional[str] = None) -> List[str]:
        """Translate multiple texts in a batch."""
        pass
    
    @abstractmethod
    async def detect_language(self, text: str) -> LanguageDetectionResult:
        """Detect the language of given text."""
        pass
    
    @abstractmethod
    async def get_supported_languages(self) -> List[str]:
        """Get list of supported language codes."""
        pass
    
    @abstractmethod
    async def get_usage_statistics(self) -> Dict[str, Any]:
        """Get API usage statistics."""
        pass
    
    @abstractmethod
    async def validate_api_key(self) -> bool:
        """Validate if API key is valid and working."""
        pass
    
    @abstractmethod
    def get_provider(self) -> TranslationProvider:
        """Get the translation provider type."""
        pass
    
    @abstractmethod
    async def estimate_cost(self, character_count: int) -> float:
        """Estimate cost for translating given number of characters."""
        pass
    
    @abstractmethod
    async def get_rate_limits(self) -> Dict[str, Any]:
        """Get current rate limit information."""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if service is currently available."""
        pass
    
    @abstractmethod
    async def health_check(self) -> Dict[str, Any]:
        """Perform health check on the service."""
        pass
