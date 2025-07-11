"""
Formatting Domain Entity

Represents Excel cell formatting information to be preserved during translation.
"""

from dataclasses import dataclass
from typing import Optional, Dict, Any, Tuple
from enum import Enum


class FontWeight(Enum):
    """Font weight enumeration."""
    NORMAL = "normal"
    BOLD = "bold"


class FontStyle(Enum):
    """Font style enumeration."""
    NORMAL = "normal"
    ITALIC = "italic"


class BorderStyle(Enum):
    """Border style enumeration."""
    NONE = "none"
    THIN = "thin"
    MEDIUM = "medium"
    THICK = "thick"
    DOUBLE = "double"
    DASHED = "dashed"
    DOTTED = "dotted"


class HorizontalAlignment(Enum):
    """Horizontal alignment enumeration."""
    LEFT = "left"
    CENTER = "center"
    RIGHT = "right"
    JUSTIFY = "justify"
    FILL = "fill"


class VerticalAlignment(Enum):
    """Vertical alignment enumeration."""
    TOP = "top"
    CENTER = "center"
    BOTTOM = "bottom"
    JUSTIFY = "justify"


@dataclass
class FontFormat:
    """Font formatting information."""
    name: Optional[str] = None
    size: Optional[float] = None
    weight: FontWeight = FontWeight.NORMAL
    style: FontStyle = FontStyle.NORMAL
    color: Optional[str] = None  # RGB hex color
    underline: bool = False
    strikethrough: bool = False


@dataclass
class BorderFormat:
    """Border formatting information."""
    top: BorderStyle = BorderStyle.NONE
    bottom: BorderStyle = BorderStyle.NONE
    left: BorderStyle = BorderStyle.NONE
    right: BorderStyle = BorderStyle.NONE
    top_color: Optional[str] = None
    bottom_color: Optional[str] = None
    left_color: Optional[str] = None
    right_color: Optional[str] = None


@dataclass
class AlignmentFormat:
    """Alignment formatting information."""
    horizontal: HorizontalAlignment = HorizontalAlignment.LEFT
    vertical: VerticalAlignment = VerticalAlignment.BOTTOM
    wrap_text: bool = False
    shrink_to_fit: bool = False
    indent: int = 0
    text_rotation: int = 0


@dataclass
class FillFormat:
    """Fill/background formatting information."""
    background_color: Optional[str] = None  # RGB hex color
    pattern_type: Optional[str] = None
    pattern_color: Optional[str] = None


@dataclass
class MergedCellInfo:
    """Information about merged cells."""
    start_row: int
    start_column: int
    end_row: int
    end_column: int
    
    def contains_cell(self, row: int, column: int) -> bool:
        """Check if given cell is within this merged range."""
        return (self.start_row <= row <= self.end_row and 
                self.start_column <= column <= self.end_column)


@dataclass
class CellFormat:
    """Complete cell formatting information."""
    font: FontFormat
    border: BorderFormat
    alignment: AlignmentFormat
    fill: FillFormat
    number_format: Optional[str] = None
    is_merged: bool = False
    merged_range: Optional[MergedCellInfo] = None


@dataclass
class RowFormat:
    """Row formatting information."""
    height: Optional[float] = None
    hidden: bool = False
    outline_level: int = 0


@dataclass
class ColumnFormat:
    """Column formatting information."""
    width: Optional[float] = None
    hidden: bool = False
    outline_level: int = 0


@dataclass
class SheetFormat:
    """Sheet-level formatting information."""
    frozen_rows: int = 0
    frozen_columns: int = 0
    zoom_scale: int = 100
    show_gridlines: bool = True
    show_row_column_headers: bool = True
    tab_color: Optional[str] = None


@dataclass
class Formatting:
    """Domain entity representing Excel formatting information."""
    sheet_name: str
    cell_formats: Dict[Tuple[int, int], CellFormat]  # (row, col) -> CellFormat
    row_formats: Dict[int, RowFormat]  # row -> RowFormat
    column_formats: Dict[int, ColumnFormat]  # column -> ColumnFormat
    sheet_format: SheetFormat
    merged_cells: list[MergedCellInfo]
    
    @classmethod
    def create_empty(cls, sheet_name: str) -> 'Formatting':
        """Create empty formatting instance."""
        return cls(
            sheet_name=sheet_name,
            cell_formats={},
            row_formats={},
            column_formats={},
            sheet_format=SheetFormat(),
            merged_cells=[]
        )
    
    def get_cell_format(self, row: int, column: int) -> Optional[CellFormat]:
        """Get formatting for specific cell."""
        return self.cell_formats.get((row, column))
    
    def set_cell_format(self, row: int, column: int, cell_format: CellFormat) -> None:
        """Set formatting for specific cell."""
        self.cell_formats[(row, column)] = cell_format
    
    def get_row_format(self, row: int) -> Optional[RowFormat]:
        """Get formatting for specific row."""
        return self.row_formats.get(row)
    
    def set_row_format(self, row: int, row_format: RowFormat) -> None:
        """Set formatting for specific row."""
        self.row_formats[row] = row_format
    
    def get_column_format(self, column: int) -> Optional[ColumnFormat]:
        """Get formatting for specific column."""
        return self.column_formats.get(column)
    
    def set_column_format(self, column: int, column_format: ColumnFormat) -> None:
        """Set formatting for specific column."""
        self.column_formats[column] = column_format
    
    def is_cell_merged(self, row: int, column: int) -> bool:
        """Check if cell is part of a merged range."""
        return any(merged.contains_cell(row, column) for merged in self.merged_cells)
    
    def get_merged_cell_info(self, row: int, column: int) -> Optional[MergedCellInfo]:
        """Get merged cell information for given cell."""
        for merged in self.merged_cells:
            if merged.contains_cell(row, column):
                return merged
        return None
    
    def add_merged_cell(self, merged_info: MergedCellInfo) -> None:
        """Add merged cell information."""
        self.merged_cells.append(merged_info)
