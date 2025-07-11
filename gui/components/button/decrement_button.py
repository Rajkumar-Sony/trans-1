"""
Decrement Button Component

Custom button for decrementing numeric values.
"""

from PyQt6.QtWidgets import QPushButton, QWidget
from PyQt6.QtCore import pyqtSignal, QTimer
from PyQt6.QtGui import QIcon
from typing import Optional


class DecrementButton(QPushButton):
    """Custom decrement button with repeat functionality."""
    
    decrement_requested = pyqtSignal()
    
    def __init__(self, parent: Optional[QWidget] = None):
        """Initialize decrement button."""
        super().__init__("-", parent)
        
        # Timer for repeat functionality
        self.repeat_timer = QTimer()
        self.repeat_timer.timeout.connect(self._on_repeat)
        self.repeat_delay = 500  # Initial delay in ms
        self.repeat_interval = 100  # Repeat interval in ms
        
        self._setup_button()
        self._connect_signals()
    
    def _setup_button(self) -> None:
        """Setup button appearance and properties."""
        self.setMinimumHeight(25)
        self.setMinimumWidth(25)
        self.setMaximumHeight(25)
        self.setMaximumWidth(25)
        
        # Apply styling
        self.setStyleSheet("""
            DecrementButton {
                background-color: #d13438;
                color: white;
                border: none;
                border-radius: 3px;
                font-size: 14px;
                font-weight: bold;
            }
            
            DecrementButton:hover {
                background-color: #b02a2f;
            }
            
            DecrementButton:pressed {
                background-color: #8e2025;
            }
            
            DecrementButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
        """)
        
        # Set tooltip
        self.setToolTip("Decrement value")
    
    def _connect_signals(self) -> None:
        """Connect button signals."""
        self.clicked.connect(self._on_clicked)
        self.pressed.connect(self._on_pressed)
        self.released.connect(self._on_released)
    
    def _on_clicked(self) -> None:
        """Handle single click."""
        self.decrement_requested.emit()
    
    def _on_pressed(self) -> None:
        """Handle button press - start repeat timer."""
        self.repeat_timer.start(self.repeat_delay)
    
    def _on_released(self) -> None:
        """Handle button release - stop repeat timer."""
        self.repeat_timer.stop()
    
    def _on_repeat(self) -> None:
        """Handle repeat timer timeout."""
        self.decrement_requested.emit()
        # Change to faster repeat interval after first repeat
        if self.repeat_timer.interval() == self.repeat_delay:
            self.repeat_timer.setInterval(self.repeat_interval)
    
    def set_repeat_settings(self, initial_delay: int, repeat_interval: int) -> None:
        """Set repeat timing settings."""
        self.repeat_delay = initial_delay
        self.repeat_interval = repeat_interval
    
    def set_enabled_with_tooltip(self, enabled: bool, tooltip: str = "") -> None:
        """Set enabled state with optional tooltip."""
        self.setEnabled(enabled)
        if tooltip:
            self.setToolTip(tooltip)
        else:
            self.setToolTip("Decrement value")
    
    def set_icon_from_path(self, icon_path: str) -> None:
        """Set button icon from file path."""
        try:
            icon = QIcon(icon_path)
            self.setIcon(icon)
            self.setText("")  # Remove text when icon is set
        except Exception:
            pass  # Ignore icon loading errors
