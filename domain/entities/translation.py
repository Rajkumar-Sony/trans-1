"""
Translation Domain Entity

Represents a translation operation and its results.
"""

from dataclasses import dataclass
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


class TranslationStatus(Enum):
    """Translation status enumeration."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class TranslationProvider(Enum):
    """Translation provider enumeration."""
    DEEPL = "deepl"
    GOOGLE = "google"


@dataclass
class TranslationRequest:
    """Translation request data."""
    text: str
    source_language: Optional[str]
    target_language: str
    preserve_formatting: bool = True
    ignore_brackets: bool = True
    ignore_japanese_quotes: bool = True


@dataclass
class TranslationResult:
    """Result of a single translation."""
    original_text: str
    translated_text: str
    source_language_detected: Optional[str]
    confidence: Optional[float]
    provider: TranslationProvider
    processing_time: float
    error_message: Optional[str] = None


@dataclass
class BatchTranslationMetrics:
    """Metrics for batch translation operations."""
    total_texts: int
    successful_translations: int
    failed_translations: int
    total_characters: int
    processing_time: float
    average_time_per_text: float
    api_calls_made: int
    rate_limit_hits: int


@dataclass
class Translation:
    """Domain entity representing a translation operation."""
    id: str
    sheet_name: str
    source_language: Optional[str]
    target_language: str
    provider: TranslationProvider
    status: TranslationStatus
    requests: List[TranslationRequest]
    results: List[TranslationResult]
    metrics: Optional[BatchTranslationMetrics]
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None
    
    @classmethod
    def create(cls, sheet_name: str, source_language: Optional[str], 
               target_language: str, provider: TranslationProvider) -> 'Translation':
        """Create a new translation instance."""
        import uuid
        return cls(
            id=str(uuid.uuid4()),
            sheet_name=sheet_name,
            source_language=source_language,
            target_language=target_language,
            provider=provider,
            status=TranslationStatus.PENDING,
            requests=[],
            results=[],
            metrics=None,
            created_at=datetime.now()
        )
    
    def add_request(self, request: TranslationRequest) -> None:
        """Add a translation request."""
        self.requests.append(request)
    
    def add_result(self, result: TranslationResult) -> None:
        """Add a translation result."""
        self.results.append(result)
    
    def start_processing(self) -> None:
        """Mark translation as started."""
        self.status = TranslationStatus.IN_PROGRESS
        self.started_at = datetime.now()
    
    def complete_successfully(self, metrics: BatchTranslationMetrics) -> None:
        """Mark translation as completed successfully."""
        self.status = TranslationStatus.COMPLETED
        self.completed_at = datetime.now()
        self.metrics = metrics
    
    def fail(self, error_message: str) -> None:
        """Mark translation as failed."""
        self.status = TranslationStatus.FAILED
        self.completed_at = datetime.now()
        self.error_message = error_message
    
    def cancel(self) -> None:
        """Cancel the translation."""
        self.status = TranslationStatus.CANCELLED
        self.completed_at = datetime.now()
    
    def get_success_rate(self) -> float:
        """Get translation success rate."""
        if not self.results:
            return 0.0
        successful = sum(1 for result in self.results if result.error_message is None)
        return successful / len(self.results)
    
    def get_total_processing_time(self) -> float:
        """Get total processing time in seconds."""
        if self.started_at and self.completed_at:
            return (self.completed_at - self.started_at).total_seconds()
        return 0.0
