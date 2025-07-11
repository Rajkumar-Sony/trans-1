"""
Select File Button Component

Custom button for file selection operations.
"""

from PyQt6.QtWidgets import QPushButton, QWidget, QFileDialog
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QIcon
from typing import Optional


class SelectFileButton(QPushButton):
    """Custom select file button with built-in file dialog."""
    
    file_selected = pyqtSignal(str)  # Emits selected file path
    
    def __init__(self, parent: Optional[QWidget] = None):
        """Initialize select file button."""
        super().__init__("Select File", parent)
        
        self.file_filter = "Excel Files (*.xlsx *.xlsm *.xls)"
        self.dialog_title = "Select Excel File"
        self.start_directory = ""
        
        self._setup_button()
        self._connect_signals()
    
    def _setup_button(self) -> None:
        """Setup button appearance and properties."""
        self.setMinimumHeight(40)
        self.setMinimumWidth(120)
        
        # Apply styling
        self.setStyleSheet("""
            SelectFileButton {
                background-color: #5c2d91;
                color: white;
                border: none;
                border-radius: 4px;
                font-size: 14px;
                font-weight: bold;
                padding: 8px 16px;
            }
            
            SelectFileButton:hover {
                background-color: #4a237a;
            }
            
            SelectFileButton:pressed {
                background-color: #3a1c63;
            }
            
            SelectFileButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
        """)
    
    def _connect_signals(self) -> None:
        """Connect button signals."""
        self.clicked.connect(self._on_clicked)
    
    def _on_clicked(self) -> None:
        """Handle button click and open file dialog."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            self.dialog_title,
            self.start_directory,
            self.file_filter
        )
        
        if file_path:
            self.file_selected.emit(file_path)
    
    def set_file_filter(self, file_filter: str) -> None:
        """Set file filter for dialog."""
        self.file_filter = file_filter
    
    def set_dialog_title(self, title: str) -> None:
        """Set dialog title."""
        self.dialog_title = title
    
    def set_start_directory(self, directory: str) -> None:
        """Set starting directory for dialog."""
        self.start_directory = directory
    
    def set_text(self, text: str) -> None:
        """Set button text."""
        self.setText(text)
    
    def set_enabled_with_tooltip(self, enabled: bool, tooltip: str = "") -> None:
        """Set enabled state with optional tooltip."""
        self.setEnabled(enabled)
        if tooltip:
            self.setToolTip(tooltip)
        else:
            self.setToolTip("")
    
    def set_icon_from_path(self, icon_path: str) -> None:
        """Set button icon from file path."""
        try:
            icon = QIcon(icon_path)
            self.setIcon(icon)
        except Exception:
            pass  # Ignore icon loading errors
