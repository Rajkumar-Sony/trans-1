"""
Excel File Domain Entity

Represents an Excel file within the translation system.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Any
from pathlib import Path


@dataclass
class SheetInfo:
    """Information about an Excel sheet."""
    name: str
    text_cells: int
    total_cells: int
    has_formulas: bool
    has_merged_cells: bool
    row_count: int
    column_count: int


@dataclass
class CellPosition:
    """Position of a cell in Excel sheet."""
    row: int
    column: int
    
    def __str__(self) -> str:
        return f"({self.row}, {self.column})"


@dataclass
class ExcelFile:
    """Domain entity representing an Excel file."""
    file_path: Path
    file_name: str
    file_size: int
    format_type: str  # xlsx, xlsm, xls
    sheets: Dict[str, SheetInfo]
    total_translatable_cells: int
    total_sheets: int
    is_valid: bool
    error_message: Optional[str] = None
    
    @classmethod
    def create(cls, file_path: str) -> 'ExcelFile':
        """Create ExcelFile instance from file path."""
        path = Path(file_path)
        
        if not path.exists():
            return cls(
                file_path=path,
                file_name=path.name,
                file_size=0,
                format_type="",
                sheets={},
                total_translatable_cells=0,
                total_sheets=0,
                is_valid=False,
                error_message="File does not exist"
            )
        
        return cls(
            file_path=path,
            file_name=path.name,
            file_size=path.stat().st_size,
            format_type=path.suffix.lower().replace('.', ''),
            sheets={},
            total_translatable_cells=0,
            total_sheets=0,
            is_valid=True
        )
    
    def add_sheet_info(self, sheet_name: str, sheet_info: SheetInfo) -> None:
        """Add sheet information to the file."""
        self.sheets[sheet_name] = sheet_info
        self.total_sheets = len(self.sheets)
        self.total_translatable_cells += sheet_info.text_cells
    
    def get_sheet_names(self) -> List[str]:
        """Get list of sheet names."""
        return list(self.sheets.keys())
    
    def get_total_translatable_cells(self) -> int:
        """Get total number of translatable cells across all sheets."""
        return sum(sheet.text_cells for sheet in self.sheets.values())
    
    def is_supported_format(self) -> bool:
        """Check if file format is supported."""
        return self.format_type in ['xlsx', 'xlsm', 'xls']
