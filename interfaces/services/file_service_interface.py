"""
File Service Interface

Abstract interface for file service operations.
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any, BinaryIO
from pathlib import Path

from ...application.dto.file_info import FileInfo, FileValidationResult, FileCharacteristics


class FileServiceInterface(ABC):
    """Interface for file service operations."""
    
    @abstractmethod
    async def analyze_file(self, file_path: str) -> FileInfo:
        """Analyze file and return complete file information."""
        pass
    
    @abstractmethod
    async def validate_file(self, file_path: str) -> FileValidationResult:
        """Validate if file can be processed."""
        pass
    
    @abstractmethod
    async def calculate_characteristics(self, file_path: str) -> FileCharacteristics:
        """Calculate file characteristics for optimization."""
        pass
    
    @abstractmethod
    async def extract_content(self, file_path: str, 
                            sheet_names: Optional[List[str]] = None) -> Dict[str, List[tuple]]:
        """Extract translatable content from file."""
        pass
    
    @abstractmethod
    async def create_backup(self, file_path: str) -> str:
        """Create backup of file and return backup path."""
        pass
    
    @abstractmethod
    async def restore_from_backup(self, backup_path: str, original_path: str) -> bool:
        """Restore file from backup."""
        pass
    
    @abstractmethod
    async def cleanup_backups(self, max_age_days: int = 7) -> int:
        """Clean up old backup files and return number of files deleted."""
        pass
    
    @abstractmethod
    async def get_file_hash(self, file_path: str) -> str:
        """Get file hash for integrity checking."""
        pass
    
    @abstractmethod
    async def verify_file_integrity(self, file_path: str, expected_hash: str) -> bool:
        """Verify file integrity using hash."""
        pass
    
    @abstractmethod
    async def get_temporary_directory(self) -> Path:
        """Get temporary directory for file operations."""
        pass
    
    @abstractmethod
    async def cleanup_temporary_files(self) -> int:
        """Clean up temporary files and return number of files deleted."""
        pass
    
    @abstractmethod
    def get_supported_formats(self) -> List[str]:
        """Get list of supported file formats."""
        pass
    
    @abstractmethod
    async def convert_format(self, input_path: str, output_path: str, 
                           target_format: str) -> bool:
        """Convert file to different format."""
        pass
    
    @abstractmethod
    async def optimize_file_size(self, file_path: str, output_path: str) -> bool:
        """Optimize file size while preserving content."""
        pass
