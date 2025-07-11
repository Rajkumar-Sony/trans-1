"""
File Info DTO

Data Transfer Object for file information.
"""

from dataclasses import dataclass
from typing import List, Optional, Dict, Any
from datetime import datetime
from pathlib import Path


@dataclass
class SheetInfo:
    """Information about a single Excel sheet."""
    name: str
    index: int
    total_rows: int
    total_columns: int
    total_cells: int
    text_cells: int
    formula_cells: int
    empty_cells: int
    merged_cell_ranges: int
    has_formatting: bool
    has_comments: bool
    has_images: bool
    is_hidden: bool
    is_protected: bool
    
    @property
    def translatable_cells(self) -> int:
        """Get number of cells that can be translated."""
        return self.text_cells
    
    @property
    def completion_percentage(self) -> float:
        """Get completion percentage (cells with content vs total cells)."""
        if self.total_cells == 0:
            return 0.0
        return ((self.total_cells - self.empty_cells) / self.total_cells) * 100


@dataclass
class FileValidationResult:
    """Result of file validation."""
    is_valid: bool
    is_supported_format: bool
    is_readable: bool
    is_corrupted: bool
    has_password_protection: bool
    file_size_mb: float
    estimated_processing_time: float  # in seconds
    warnings: List[str]
    errors: List[str]
    
    @property
    def can_process(self) -> bool:
        """Check if file can be processed."""
        return (self.is_valid and self.is_supported_format and 
                self.is_readable and not self.is_corrupted)


@dataclass
class FileCharacteristics:
    """Characteristics of the Excel file for optimization."""
    total_size_mb: float
    total_cells: int
    total_translatable_cells: int
    total_characters: int
    largest_sheet_cells: int
    complexity_score: float  # 0-100 scale
    recommended_batch_size: int
    estimated_api_calls: int
    estimated_processing_time: float
    memory_requirements_mb: float


@dataclass
class FileInfo:
    """Complete file information DTO."""
    file_path: str
    file_name: str
    file_size: int
    file_format: str  # xlsx, xlsm, xls
    created_date: Optional[datetime]
    modified_date: Optional[datetime]
    accessed_date: Optional[datetime]
    
    # Content information
    total_sheets: int
    sheets: List[SheetInfo]
    total_cells: int
    total_translatable_cells: int
    estimated_translation_characters: int
    
    # Validation and characteristics
    validation_result: FileValidationResult
    characteristics: FileCharacteristics
    
    # Processing metadata
    analyzed_at: datetime
    analysis_time: float
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}
    
    @classmethod
    def create_from_path(cls, file_path: str) -> 'FileInfo':
        """Create FileInfo instance from file path."""
        path = Path(file_path)
        
        # Get file stats
        if path.exists():
            stat = path.stat()
            created_date = datetime.fromtimestamp(stat.st_ctime)
            modified_date = datetime.fromtimestamp(stat.st_mtime)
            accessed_date = datetime.fromtimestamp(stat.st_atime)
            file_size = stat.st_size
        else:
            created_date = None
            modified_date = None
            accessed_date = None
            file_size = 0
        
        return cls(
            file_path=file_path,
            file_name=path.name,
            file_size=file_size,
            file_format=path.suffix.lower().replace('.', ''),
            created_date=created_date,
            modified_date=modified_date,
            accessed_date=accessed_date,
            total_sheets=0,
            sheets=[],
            total_cells=0,
            total_translatable_cells=0,
            estimated_translation_characters=0,
            validation_result=FileValidationResult(
                is_valid=False,
                is_supported_format=False,
                is_readable=False,
                is_corrupted=False,
                has_password_protection=False,
                file_size_mb=0.0,
                estimated_processing_time=0.0,
                warnings=[],
                errors=[]
            ),
            characteristics=FileCharacteristics(
                total_size_mb=0.0,
                total_cells=0,
                total_translatable_cells=0,
                total_characters=0,
                largest_sheet_cells=0,
                complexity_score=0.0,
                recommended_batch_size=50,
                estimated_api_calls=0,
                estimated_processing_time=0.0,
                memory_requirements_mb=0.0
            ),
            analyzed_at=datetime.now(),
            analysis_time=0.0
        )
    
    def add_sheet_info(self, sheet_info: SheetInfo) -> None:
        """Add sheet information."""
        self.sheets.append(sheet_info)
        self.total_sheets = len(self.sheets)
        self.total_cells += sheet_info.total_cells
        self.total_translatable_cells += sheet_info.translatable_cells
    
    def get_sheet_by_name(self, name: str) -> Optional[SheetInfo]:
        """Get sheet information by name."""
        for sheet in self.sheets:
            if sheet.name == name:
                return sheet
        return None
    
    def get_sheet_names(self) -> List[str]:
        """Get list of sheet names."""
        return [sheet.name for sheet in self.sheets]
    
    def get_translatable_sheets(self) -> List[SheetInfo]:
        """Get list of sheets that have translatable content."""
        return [sheet for sheet in self.sheets if sheet.translatable_cells > 0]
    
    def calculate_complexity_score(self) -> float:
        """Calculate file complexity score (0-100)."""
        score = 0.0
        
        # Size factor (0-30 points)
        size_mb = self.file_size / (1024 * 1024)
        if size_mb > 100:
            score += 30
        elif size_mb > 50:
            score += 20
        elif size_mb > 10:
            score += 10
        elif size_mb > 1:
            score += 5
        
        # Cell count factor (0-25 points)
        if self.total_cells > 100000:
            score += 25
        elif self.total_cells > 50000:
            score += 20
        elif self.total_cells > 10000:
            score += 15
        elif self.total_cells > 1000:
            score += 10
        
        # Sheet count factor (0-15 points)
        if self.total_sheets > 20:
            score += 15
        elif self.total_sheets > 10:
            score += 10
        elif self.total_sheets > 5:
            score += 5
        
        # Formatting complexity (0-15 points)
        sheets_with_formatting = sum(1 for sheet in self.sheets if sheet.has_formatting)
        if sheets_with_formatting > self.total_sheets * 0.8:
            score += 15
        elif sheets_with_formatting > self.total_sheets * 0.5:
            score += 10
        elif sheets_with_formatting > 0:
            score += 5
        
        # Protected/complex features (0-15 points)
        protected_sheets = sum(1 for sheet in self.sheets if sheet.is_protected)
        sheets_with_images = sum(1 for sheet in self.sheets if sheet.has_images)
        
        if protected_sheets > 0 or sheets_with_images > 0:
            score += min(15, (protected_sheets + sheets_with_images) * 3)
        
        return min(100.0, score)
    
    def estimate_processing_time(self, words_per_minute: float = 1000) -> float:
        """Estimate processing time in seconds."""
        # Rough estimation: assume average 5 characters per word
        estimated_words = self.estimated_translation_characters / 5
        processing_minutes = estimated_words / words_per_minute
        
        # Add overhead for file operations and API calls
        overhead_factor = 1.5 if self.characteristics.complexity_score > 50 else 1.2
        
        return processing_minutes * 60 * overhead_factor
    
    def get_file_size_mb(self) -> float:
        """Get file size in megabytes."""
        return self.file_size / (1024 * 1024)
    
    def is_large_file(self) -> bool:
        """Check if this is considered a large file."""
        return self.get_file_size_mb() > 10 or self.total_translatable_cells > 10000
