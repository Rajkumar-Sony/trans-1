import deepl
import logging
import time
from typing import List, Optional, Dict, Any

class DeepLClient:
    """DeepL API client with error handling and rate limiting."""
    
    def __init__(self, api_key: str):
        """Initialize DeepL client.
        
        Args:
            api_key: DeepL API key
        """
        self.api_key = api_key
        self.translator = None
        self.usage_info = None
        self.logger = logging.getLogger(__name__)
        
        if api_key:
            self.initialize_translator()
    
    def initialize_translator(self):
        """Initialize the DeepL translator."""
        try:
            self.translator = deepl.Translator(self.api_key)
            # Test the connection
            self.usage_info = self.translator.get_usage()
            self.logger.info(f"DeepL API initialized. Usage: {self.usage_info.character.count}/{self.usage_info.character.limit}")
        except Exception as e:
            self.logger.error(f"Failed to initialize DeepL translator: {str(e)}")
            raise
    
    def is_valid(self) -> bool:
        """Check if the API key is valid."""
        return self.translator is not None
    
    def get_supported_languages(self) -> Dict[str, List[Dict[str, str]]]:
        """Get supported source and target languages."""
        if not self.translator:
            return {"source": [], "target": []}
        
        try:
            source_langs = self.translator.get_source_languages()
            target_langs = self.translator.get_target_languages()
            
            return {
                "source": [{"code": lang.code, "name": lang.name} for lang in source_langs],
                "target": [{"code": lang.code, "name": lang.name} for lang in target_langs]
            }
        except Exception as e:
            self.logger.error(f"Failed to get supported languages: {str(e)}")
            return {"source": [], "target": []}
    
    def translate_text(self, text: str, target_lang: str, source_lang: Optional[str] = None) -> str:
        """Translate a single text string.
        
        Args:
            text: Text to translate
            target_lang: Target language code
            source_lang: Source language code (optional)
            
        Returns:
            Translated text
        """
        if not self.translator:
            raise ValueError("DeepL translator not initialized")
        
        if not text or not text.strip():
            return text
        
        try:
            result = self.translator.translate_text(
                text, 
                target_lang=target_lang,
                source_lang=source_lang
            )
            return result.text
        except Exception as e:
            self.logger.error(f"Translation failed for text: {text[:50]}... Error: {str(e)}")
            raise
    
    def translate_batch(self, texts: List[str], target_lang: str, source_lang: Optional[str] = None) -> List[str]:
        """Translate multiple texts in batch.
        
        Args:
            texts: List of texts to translate
            target_lang: Target language code
            source_lang: Source language code (optional)
            
        Returns:
            List of translated texts
        """
        if not self.translator:
            raise ValueError("DeepL translator not initialized")
        
        if not texts:
            return []
        
        # Filter out empty texts but keep track of original positions
        text_mapping = {}
        filtered_texts = []
        
        for i, text in enumerate(texts):
            if text and text.strip():
                text_mapping[len(filtered_texts)] = i
                filtered_texts.append(text)
        
        if not filtered_texts:
            return texts
        
        try:
            results = self.translator.translate_text(
                filtered_texts,
                target_lang=target_lang,
                source_lang=source_lang
            )
            
            # Reconstruct the full results list
            translated_texts = texts.copy()
            for i, result in enumerate(results):
                original_index = text_mapping[i]
                translated_texts[original_index] = result.text
            
            return translated_texts
            
        except Exception as e:
            self.logger.error(f"Batch translation failed: {str(e)}")
            raise
    
    def get_usage(self) -> Optional[Dict[str, Any]]:
        """Get current API usage information."""
        if not self.translator:
            return None
        
        try:
            usage = self.translator.get_usage()
            return {
                "character_count": usage.character.count,
                "character_limit": usage.character.limit,
                "document_count": usage.document.count if usage.document else 0,
                "document_limit": usage.document.limit if usage.document else 0
            }
        except Exception as e:
            self.logger.error(f"Failed to get usage info: {str(e)}")
            return None
    
    def wait_for_rate_limit(self, delay: float = 1.0):
        """Wait for rate limit if needed."""
        time.sleep(delay)
