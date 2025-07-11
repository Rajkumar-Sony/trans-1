"""
Translation Response DTO

Data Transfer Object for translation responses.
"""

from dataclasses import dataclass
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


class TranslationStatus(Enum):
    """Translation status enumeration."""
    SUCCESS = "success"
    PARTIAL_SUCCESS = "partial_success"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class CellTranslationResult:
    """Result of translating a single cell."""
    original_text: str
    translated_text: str
    row: int
    column: int
    source_language_detected: Optional[str]
    confidence_score: Optional[float]
    processing_time: float
    error_message: Optional[str] = None
    
    @property
    def is_successful(self) -> bool:
        """Check if translation was successful."""
        return self.error_message is None and self.translated_text is not None


@dataclass
class SheetTranslationResult:
    """Result of translating a single sheet."""
    sheet_name: str
    total_cells: int
    successful_translations: int
    failed_translations: int
    skipped_cells: int
    cell_results: List[CellTranslationResult]
    processing_time: float
    error_message: Optional[str] = None
    
    @property
    def success_rate(self) -> float:
        """Get success rate as percentage."""
        if self.total_cells == 0:
            return 0.0
        return (self.successful_translations / self.total_cells) * 100
    
    @property
    def is_successful(self) -> bool:
        """Check if sheet translation was successful."""
        return self.error_message is None and self.successful_translations > 0


@dataclass
class TranslationMetrics:
    """Metrics for the translation operation."""
    total_files: int
    total_sheets: int
    total_cells: int
    total_characters: int
    successful_translations: int
    failed_translations: int
    skipped_cells: int
    api_calls_made: int
    total_processing_time: float
    average_time_per_cell: float
    characters_per_second: float
    
    @property
    def overall_success_rate(self) -> float:
        """Get overall success rate as percentage."""
        if self.total_cells == 0:
            return 0.0
        return (self.successful_translations / self.total_cells) * 100


@dataclass
class ErrorInfo:
    """Information about errors that occurred during translation."""
    error_type: str
    error_message: str
    sheet_name: Optional[str] = None
    cell_position: Optional[tuple] = None  # (row, column)
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()


@dataclass
class TranslationResponse:
    """Complete translation response DTO."""
    request_id: str
    status: TranslationStatus
    file_path: str
    output_file_path: Optional[str]
    sheet_results: List[SheetTranslationResult]
    metrics: TranslationMetrics
    errors: List[ErrorInfo]
    warnings: List[str]
    started_at: datetime
    completed_at: datetime
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}
    
    @property
    def total_processing_time(self) -> float:
        """Get total processing time in seconds."""
        return (self.completed_at - self.started_at).total_seconds()
    
    @property
    def is_successful(self) -> bool:
        """Check if translation was successful."""
        return self.status in [TranslationStatus.SUCCESS, TranslationStatus.PARTIAL_SUCCESS]
    
    def get_successful_sheets(self) -> List[SheetTranslationResult]:
        """Get list of successfully translated sheets."""
        return [sheet for sheet in self.sheet_results if sheet.is_successful]
    
    def get_failed_sheets(self) -> List[SheetTranslationResult]:
        """Get list of sheets that failed translation."""
        return [sheet for sheet in self.sheet_results if not sheet.is_successful]
    
    def get_overall_success_rate(self) -> float:
        """Get overall success rate across all sheets."""
        return self.metrics.overall_success_rate
    
    def add_error(self, error_type: str, error_message: str, 
                  sheet_name: Optional[str] = None, 
                  cell_position: Optional[tuple] = None) -> None:
        """Add an error to the response."""
        error = ErrorInfo(
            error_type=error_type,
            error_message=error_message,
            sheet_name=sheet_name,
            cell_position=cell_position
        )
        self.errors.append(error)
    
    def add_warning(self, warning_message: str) -> None:
        """Add a warning to the response."""
        self.warnings.append(warning_message)
    
    def get_summary(self) -> Dict[str, Any]:
        """Get a summary of the translation results."""
        return {
            'status': self.status.value,
            'total_sheets': len(self.sheet_results),
            'successful_sheets': len(self.get_successful_sheets()),
            'failed_sheets': len(self.get_failed_sheets()),
            'total_cells': self.metrics.total_cells,
            'successful_translations': self.metrics.successful_translations,
            'failed_translations': self.metrics.failed_translations,
            'success_rate': self.get_overall_success_rate(),
            'processing_time': self.total_processing_time,
            'errors_count': len(self.errors),
            'warnings_count': len(self.warnings)
        }
