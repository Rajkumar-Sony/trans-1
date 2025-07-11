"""
Format Options Combo Box Component

Modern QComboBox implementation for Excel format selection.
"""

from PyQt6.QtWidgets import QComboBox
from PyQt6.QtCore import pyqtSignal, Qt
from typing import Dict, Optional, List
from enum import Enum


class ExcelFormat(Enum):
    """Supported Excel format types."""
    XLSX = "xlsx"
    XLSM = "xlsm"
    XLS = "xls"
    CSV = "csv"


class FormatComboBox(QComboBox):
    """Custom combo box for Excel format selection with modern styling."""
    
    # Signals
    format_changed = pyqtSignal(str)  # Emits format extension
    
    def __init__(self, parent=None):
        """Initialize the format combo box."""
        super().__init__(parent)
        self._format_data: Dict[str, str] = {}
        self._setup_ui()
        self._connect_signals()
        self._load_formats()
    
    def _setup_ui(self):
        """Set up the UI components."""
        self.setObjectName("formatComboBox")
        self.setToolTip("Select output format for translated file")
        self.setEditable(False)
        self.setMaxVisibleItems(6)
        
        # Enable wheel events only when focused
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
    
    def _connect_signals(self):
        """Connect internal signals."""
        self.currentTextChanged.connect(self._on_selection_changed)
    
    def _on_selection_changed(self, text: str):
        """Handle selection change."""
        if text and text in self._format_data:
            format_ext = self._format_data[text]
            self.format_changed.emit(format_ext)
    
    def _load_formats(self):
        """Load available Excel formats."""
        formats = {
            "Excel Workbook (*.xlsx)": ExcelFormat.XLSX.value,
            "Excel Macro-Enabled (*.xlsm)": ExcelFormat.XLSM.value,
            "Excel 97-2003 (*.xls)": ExcelFormat.XLS.value,
            "Comma Separated Values (*.csv)": ExcelFormat.CSV.value,
        }
        
        for display_name, extension in formats.items():
            self.addItem(display_name)
            self._format_data[display_name] = extension
        
        # Set default to XLSX
        self.setCurrentText("Excel Workbook (*.xlsx)")
    
    def set_format(self, format_extension: str):
        """
        Set the selected format by extension.
        
        Args:
            format_extension: The format extension to select
        """
        for display_name, ext in self._format_data.items():
            if ext == format_extension:
                self.setCurrentText(display_name)
                break
    
    def get_selected_format(self) -> Optional[str]:
        """
        Get the currently selected format extension.
        
        Returns:
            The selected format extension or None if nothing selected
        """
        current_text = self.currentText()
        return self._format_data.get(current_text)
    
    def get_display_text(self) -> str:
        """
        Get the current display text.
        
        Returns:
            The current display text
        """
        return self.currentText()
    
    def get_file_filter(self) -> str:
        """
        Get file filter string for the selected format.
        
        Returns:
            File filter string for QFileDialog
        """
        current_format = self.get_selected_format()
        
        filters = {
            ExcelFormat.XLSX.value: "Excel Workbook (*.xlsx)",
            ExcelFormat.XLSM.value: "Excel Macro-Enabled (*.xlsm)",
            ExcelFormat.XLS.value: "Excel 97-2003 (*.xls)",
            ExcelFormat.CSV.value: "CSV Files (*.csv)",
        }
        
        return filters.get(current_format, "All Files (*)")
    
    def is_excel_format(self) -> bool:
        """
        Check if selected format is an Excel format.
        
        Returns:
            True if Excel format is selected
        """
        current_format = self.get_selected_format()
        return current_format in [ExcelFormat.XLSX.value, ExcelFormat.XLSM.value, ExcelFormat.XLS.value]
    
    def is_csv_format(self) -> bool:
        """
        Check if CSV format is selected.
        
        Returns:
            True if CSV format is selected
        """
        return self.get_selected_format() == ExcelFormat.CSV.value
    
    def supports_macros(self) -> bool:
        """
        Check if selected format supports macros.
        
        Returns:
            True if format supports macros
        """
        return self.get_selected_format() == ExcelFormat.XLSM.value
    
    def get_mime_type(self) -> str:
        """
        Get MIME type for the selected format.
        
        Returns:
            MIME type string
        """
        current_format = self.get_selected_format()
        
        mime_types = {
            ExcelFormat.XLSX.value: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            ExcelFormat.XLSM.value: "application/vnd.ms-excel.sheet.macroEnabled.12",
            ExcelFormat.XLS.value: "application/vnd.ms-excel",
            ExcelFormat.CSV.value: "text/csv",
        }
        
        return mime_types.get(current_format, "application/octet-stream")
    
    def wheelEvent(self, event):
        """Override wheel event to prevent accidental changes."""
        if self.hasFocus():
            super().wheelEvent(event)
        else:
            event.ignore()
    
    def validate_selection(self) -> bool:
        """
        Validate the current selection.
        
        Returns:
            True if a valid format is selected
        """
        return bool(self.get_selected_format())
    
    def set_based_on_filename(self, filename: str):
        """
        Set format based on filename extension.
        
        Args:
            filename: The filename to analyze
        """
        if not filename:
            return
            
        filename_lower = filename.lower()
        
        if filename_lower.endswith('.xlsx'):
            self.set_format(ExcelFormat.XLSX.value)
        elif filename_lower.endswith('.xlsm'):
            self.set_format(ExcelFormat.XLSM.value)
        elif filename_lower.endswith('.xls'):
            self.set_format(ExcelFormat.XLS.value)
        elif filename_lower.endswith('.csv'):
            self.set_format(ExcelFormat.CSV.value)
        else:
            # Default to XLSX for unknown extensions
            self.set_format(ExcelFormat.XLSX.value)
    
    def get_recommended_extension(self) -> str:
        """
        Get recommended file extension including dot.
        
        Returns:
            File extension with dot (e.g., '.xlsx')
        """
        current_format = self.get_selected_format()
        return f".{current_format}" if current_format else ".xlsx"
