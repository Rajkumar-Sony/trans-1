"""
File Repository Interface

Abstract interface for file repository operations.
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from pathlib import Path

from ...domain.entities.excel_file import ExcelFile, SheetInfo
from ...domain.entities.formatting import Formatting


class FileRepositoryInterface(ABC):
    """Interface for file repository operations."""
    
    @abstractmethod
    async def load_file(self, file_path: str) -> ExcelFile:
        """Load an Excel file and return file entity."""
        pass
    
    @abstractmethod
    async def save_file(self, excel_file: ExcelFile, output_path: str) -> bool:
        """Save Excel file to specified path."""
        pass
    
    @abstractmethod
    async def get_sheet_names(self, file_path: str) -> List[str]:
        """Get list of sheet names from Excel file."""
        pass
    
    @abstractmethod
    async def get_sheet_info(self, file_path: str, sheet_name: str) -> SheetInfo:
        """Get detailed information about a specific sheet."""
        pass
    
    @abstractmethod
    async def extract_text_content(self, file_path: str, sheet_name: str) -> List[tuple]:
        """Extract text content from sheet as list of (text, row, column) tuples."""
        pass
    
    @abstractmethod
    async def extract_formatting(self, file_path: str, sheet_name: str) -> Formatting:
        """Extract formatting information from sheet."""
        pass
    
    @abstractmethod
    async def apply_translations(self, file_path: str, translations: Dict[str, List[tuple]], 
                                output_path: str) -> bool:
        """Apply translations to file and save as new file."""
        pass
    
    @abstractmethod
    async def validate_file(self, file_path: str) -> Dict[str, Any]:
        """Validate if file can be processed."""
        pass
    
    @abstractmethod
    async def backup_file(self, file_path: str, backup_path: str) -> bool:
        """Create backup of original file."""
        pass
    
    @abstractmethod
    async def get_file_metadata(self, file_path: str) -> Dict[str, Any]:
        """Get file metadata including size, dates, etc."""
        pass
