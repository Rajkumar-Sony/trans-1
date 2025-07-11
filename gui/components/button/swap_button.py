"""
Swap Button Component

Custom button for swapping source and target languages.
"""

from PyQt6.QtWidgets import QPushButton, QWidget
from PyQt6.QtCore import pyqtSignal, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QIcon, QTransform, QPainter
from typing import Optional


class SwapButton(QPushButton):
    """Custom swap button with rotation animation."""
    
    swap_requested = pyqtSignal()
    
    def __init__(self, parent: Optional[QWidget] = None):
        """Initialize swap button."""
        super().__init__("⇄", parent)
        
        self.rotation_animation = None
        
        self._setup_button()
        self._connect_signals()
    
    def _setup_button(self) -> None:
        """Setup button appearance and properties."""
        self.setMinimumHeight(35)
        self.setMinimumWidth(35)
        self.setMaximumHeight(35)
        self.setMaximumWidth(35)
        
        # Apply styling
        self.setStyleSheet("""
            SwapButton {
                background-color: #666666;
                color: white;
                border: none;
                border-radius: 17px;
                font-size: 16px;
                font-weight: bold;
            }
            
            SwapButton:hover {
                background-color: #777777;
            }
            
            SwapButton:pressed {
                background-color: #555555;
            }
            
            SwapButton:disabled {
                background-color: #cccccc;
                color: #888888;
            }
        """)
        
        # Set tooltip
        self.setToolTip("Swap source and target languages")
    
    def _connect_signals(self) -> None:
        """Connect button signals."""
        self.clicked.connect(self._on_clicked)
    
    def _on_clicked(self) -> None:
        """Handle button click with animation."""
        self._animate_rotation()
        self.swap_requested.emit()
    
    def _animate_rotation(self) -> None:
        """Animate button rotation."""
        # Simple visual feedback - change text temporarily
        original_text = self.text()
        self.setText("↻")
        
        # Use QTimer for simple animation
        from PyQt6.QtCore import QTimer
        timer = QTimer()
        timer.singleShot(200, lambda: self.setText(original_text))
    
    def set_enabled_with_tooltip(self, enabled: bool, tooltip: str = "") -> None:
        """Set enabled state with optional tooltip."""
        self.setEnabled(enabled)
        if tooltip:
            self.setToolTip(tooltip)
        else:
            self.setToolTip("Swap source and target languages")
    
    def set_icon_from_path(self, icon_path: str) -> None:
        """Set button icon from file path."""
        try:
            icon = QIcon(icon_path)
            self.setIcon(icon)
            self.setText("")  # Remove text when icon is set
        except Exception:
            pass  # Ignore icon loading errors
