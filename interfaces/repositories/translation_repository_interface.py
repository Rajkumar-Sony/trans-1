"""
Translation Repository Interface

Abstract interface for translation repository operations.
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from datetime import datetime

from ...domain.entities.translation import Translation, TranslationStatus


class TranslationRepositoryInterface(ABC):
    """Interface for translation repository operations."""
    
    @abstractmethod
    async def save_translation(self, translation: Translation) -> bool:
        """Save translation entity."""
        pass
    
    @abstractmethod
    async def get_translation_by_id(self, translation_id: str) -> Optional[Translation]:
        """Get translation by ID."""
        pass
    
    @abstractmethod
    async def get_translations_by_file(self, file_path: str) -> List[Translation]:
        """Get all translations for a specific file."""
        pass
    
    @abstractmethod
    async def get_translations_by_status(self, status: TranslationStatus) -> List[Translation]:
        """Get translations by status."""
        pass
    
    @abstractmethod
    async def get_recent_translations(self, limit: int = 10) -> List[Translation]:
        """Get recent translations."""
        pass
    
    @abstractmethod
    async def update_translation_status(self, translation_id: str, status: TranslationStatus) -> bool:
        """Update translation status."""
        pass
    
    @abstractmethod
    async def delete_translation(self, translation_id: str) -> bool:
        """Delete translation record."""
        pass
    
    @abstractmethod
    async def get_translation_history(self, file_path: str, 
                                     start_date: Optional[datetime] = None,
                                     end_date: Optional[datetime] = None) -> List[Translation]:
        """Get translation history for a file within date range."""
        pass
    
    @abstractmethod
    async def get_translation_statistics(self) -> Dict[str, Any]:
        """Get translation statistics."""
        pass
    
    @abstractmethod
    async def cleanup_old_translations(self, days_old: int = 30) -> int:
        """Clean up old translation records and return number deleted."""
        pass
