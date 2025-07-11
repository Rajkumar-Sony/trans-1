"""
Translation Request DTO

Data Transfer Object for translation requests.
"""

from dataclasses import dataclass
from typing import Optional, List, Dict, Any


@dataclass
class CellTranslationRequest:
    """Request for translating a single cell."""
    text: str
    row: int
    column: int
    preserve_formatting: bool = True


@dataclass
class BatchTranslationSettings:
    """Settings for batch translation operations."""
    batch_size: int = 50
    max_concurrent_requests: int = 5
    retry_attempts: int = 3
    retry_delay: float = 1.0
    ignore_empty_cells: bool = True
    ignore_formula_cells: bool = True


@dataclass
class LanguageSettings:
    """Language configuration for translation."""
    source_language: Optional[str]  # None for auto-detect
    target_language: str
    auto_detect_source: bool = False
    preserve_source_formatting: bool = True


@dataclass
class ContentFilters:
    """Filters for content that should not be translated."""
    ignore_square_brackets: bool = True  # Ignore text in []
    ignore_japanese_quotes: bool = True  # Ignore text in 「」
    ignore_urls: bool = True
    ignore_emails: bool = True
    ignore_numbers_only: bool = True
    custom_patterns: List[str] = None  # Regex patterns to ignore
    
    def __post_init__(self):
        if self.custom_patterns is None:
            self.custom_patterns = []


@dataclass
class TranslationRequest:
    """Complete translation request DTO."""
    file_path: str
    sheet_names: List[str]  # Empty list means all sheets
    language_settings: LanguageSettings
    batch_settings: BatchTranslationSettings
    content_filters: ContentFilters
    cells: List[CellTranslationRequest]
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}
    
    @classmethod
    def create_simple(cls, file_path: str, source_lang: Optional[str], 
                      target_lang: str) -> 'TranslationRequest':
        """Create a simple translation request with default settings."""
        return cls(
            file_path=file_path,
            sheet_names=[],
            language_settings=LanguageSettings(
                source_language=source_lang,
                target_language=target_lang,
                auto_detect_source=(source_lang is None)
            ),
            batch_settings=BatchTranslationSettings(),
            content_filters=ContentFilters(),
            cells=[]
        )
    
    def add_cell(self, text: str, row: int, column: int, 
                 preserve_formatting: bool = True) -> None:
        """Add a cell to be translated."""
        self.cells.append(CellTranslationRequest(
            text=text,
            row=row,
            column=column,
            preserve_formatting=preserve_formatting
        ))
    
    def get_total_cells(self) -> int:
        """Get total number of cells to translate."""
        return len(self.cells)
    
    def get_total_characters(self) -> int:
        """Get total number of characters to translate."""
        return sum(len(cell.text) for cell in self.cells)
    
    def should_ignore_text(self, text: str) -> bool:
        """Check if text should be ignored based on filters."""
        import re
        
        if not text or not text.strip():
            return True
        
        # Check square brackets
        if self.content_filters.ignore_square_brackets and '[' in text and ']' in text:
            return True
        
        # Check Japanese quotes
        if self.content_filters.ignore_japanese_quotes and '「' in text and '」' in text:
            return True
        
        # Check URLs
        if self.content_filters.ignore_urls:
            url_pattern = r'https?://[^\s]+'
            if re.search(url_pattern, text):
                return True
        
        # Check emails
        if self.content_filters.ignore_emails:
            email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            if re.search(email_pattern, text):
                return True
        
        # Check numbers only
        if self.content_filters.ignore_numbers_only:
            if re.match(r'^[\d\s\.,\-\+\(\)%$€¥£]+$', text.strip()):
                return True
        
        # Check custom patterns
        for pattern in self.content_filters.custom_patterns:
            try:
                if re.search(pattern, text):
                    return True
            except re.error:
                # Invalid regex pattern, skip
                continue
        
        return False
