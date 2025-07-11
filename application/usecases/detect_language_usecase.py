"""
Detect Language Use Case

Business logic for detecting the language of text content.
"""

import logging
from typing import Optional, Dict, Any, List

from ..dto.translation_request import TranslationRequest
from ...interfaces.services.translation_service_interface import TranslationServiceInterface, LanguageDetectionResult


class DetectLanguageUseCase:
    """Use case for detecting language of text content."""
    
    def __init__(self, translation_service: TranslationServiceInterface):
        """Initialize the use case with translation service."""
        self.translation_service = translation_service
        self.logger = logging.getLogger(__name__)
    
    async def execute(self, text: str, context: Optional[Dict[str, Any]] = None) -> LanguageDetectionResult:
        """Execute language detection for a single text."""
        self.logger.info(f"Detecting language for text of length {len(text)}")
        
        try:
            if not text or not text.strip():
                # Return default for empty text
                return LanguageDetectionResult("unknown", 0.0)
            
            # Use translation service to detect language
            result = await self.translation_service.detect_language(text)
            
            self.logger.info(f"Detected language: {result.language_code} (confidence: {result.confidence:.2f})")
            return result
            
        except Exception as e:
            self.logger.error(f"Language detection failed: {str(e)}", exc_info=True)
            # Return unknown language with zero confidence on error
            return LanguageDetectionResult("unknown", 0.0)
    
    async def execute_batch(self, texts: List[str], 
                           context: Optional[Dict[str, Any]] = None) -> List[LanguageDetectionResult]:
        """Execute language detection for multiple texts."""
        self.logger.info(f"Detecting language for batch of {len(texts)} texts")
        
        results = []
        for i, text in enumerate(texts):
            try:
                result = await self.execute(text, context)
                results.append(result)
            except Exception as e:
                self.logger.error(f"Failed to detect language for text {i}: {str(e)}")
                results.append(LanguageDetectionResult("unknown", 0.0))
        
        return results
    
    async def detect_most_common_language(self, texts: List[str], 
                                         min_confidence: float = 0.5) -> Optional[str]:
        """Detect the most common language in a list of texts."""
        self.logger.info(f"Detecting most common language from {len(texts)} texts")
        
        try:
            # Detect language for all texts
            results = await self.execute_batch(texts)
            
            # Count languages with sufficient confidence
            language_counts = {}
            for result in results:
                if result.confidence >= min_confidence and result.language_code != "unknown":
                    language_counts[result.language_code] = language_counts.get(result.language_code, 0) + 1
            
            if not language_counts:
                self.logger.warning("No languages detected with sufficient confidence")
                return None
            
            # Return most common language
            most_common = max(language_counts.items(), key=lambda x: x[1])
            self.logger.info(f"Most common language: {most_common[0]} ({most_common[1]} occurrences)")
            return most_common[0]
            
        except Exception as e:
            self.logger.error(f"Failed to detect most common language: {str(e)}", exc_info=True)
            return None
    
    async def analyze_language_distribution(self, texts: List[str], 
                                          min_confidence: float = 0.5) -> Dict[str, Dict[str, Any]]:
        """Analyze language distribution in a collection of texts."""
        self.logger.info(f"Analyzing language distribution for {len(texts)} texts")
        
        try:
            # Detect language for all texts
            results = await self.execute_batch(texts)
            
            # Analyze distribution
            distribution = {}
            total_detected = 0
            
            for result in results:
                lang = result.language_code
                if lang not in distribution:
                    distribution[lang] = {
                        'count': 0,
                        'total_confidence': 0.0,
                        'avg_confidence': 0.0,
                        'high_confidence_count': 0,
                        'percentage': 0.0
                    }
                
                distribution[lang]['count'] += 1
                distribution[lang]['total_confidence'] += result.confidence
                
                if result.confidence >= min_confidence:
                    distribution[lang]['high_confidence_count'] += 1
                    total_detected += 1
            
            # Calculate averages and percentages
            for lang, stats in distribution.items():
                stats['avg_confidence'] = stats['total_confidence'] / stats['count']
                stats['percentage'] = (stats['count'] / len(texts)) * 100
                stats['high_confidence_percentage'] = (stats['high_confidence_count'] / max(total_detected, 1)) * 100
            
            # Sort by count (most common first)
            sorted_distribution = dict(sorted(distribution.items(), 
                                            key=lambda x: x[1]['count'], 
                                            reverse=True))
            
            self.logger.info(f"Language distribution analysis complete. Found {len(sorted_distribution)} languages")
            return sorted_distribution
            
        except Exception as e:
            self.logger.error(f"Failed to analyze language distribution: {str(e)}", exc_info=True)
            return {}
    
    async def is_multilingual_content(self, texts: List[str], 
                                     min_confidence: float = 0.5,
                                     threshold_percentage: float = 10.0) -> bool:
        """Check if content contains multiple languages."""
        try:
            distribution = await self.analyze_language_distribution(texts, min_confidence)
            
            # Count languages that meet the threshold
            significant_languages = 0
            for lang, stats in distribution.items():
                if (lang != "unknown" and 
                    stats['high_confidence_percentage'] >= threshold_percentage):
                    significant_languages += 1
            
            is_multilingual = significant_languages > 1
            self.logger.info(f"Content is {'multilingual' if is_multilingual else 'monolingual'} "
                           f"({significant_languages} significant languages)")
            return is_multilingual
            
        except Exception as e:
            self.logger.error(f"Failed to check if content is multilingual: {str(e)}")
            return False
