"""
Cancel Button Component

Custom button for canceling operations.
"""

from PyQt6.QtWidgets import QPushButton, QWidget
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QIcon
from typing import Optional


class CancelButton(QPushButton):
    """Custom cancel button with enhanced functionality."""
    
    cancel_requested = pyqtSignal()
    
    def __init__(self, parent: Optional[QWidget] = None):
        """Initialize cancel button."""
        super().__init__("Cancel", parent)
        
        self._setup_button()
        self._connect_signals()
    
    def _setup_button(self) -> None:
        """Setup button appearance and properties."""
        self.setMinimumHeight(40)
        self.setMinimumWidth(100)
        
        # Apply styling
        self.setStyleSheet("""
            CancelButton {
                background-color: #d13438;
                color: white;
                border: none;
                border-radius: 4px;
                font-size: 14px;
                font-weight: bold;
                padding: 8px 16px;
            }
            
            CancelButton:hover {
                background-color: #b02a2f;
            }
            
            CancelButton:pressed {
                background-color: #8e2025;
            }
            
            CancelButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
        """)
    
    def _connect_signals(self) -> None:
        """Connect button signals."""
        self.clicked.connect(self._on_clicked)
    
    def _on_clicked(self) -> None:
        """Handle button click."""
        self.cancel_requested.emit()
    
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
