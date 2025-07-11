"""
Translate Button Component

Custom button for initiating translation operations.
"""

from PyQt6.QtWidgets import QPushButton, QWidget
from PyQt6.QtCore import pyqtSignal, QTimer
from PyQt6.QtGui import QIcon
from typing import Optional, Callable


class TranslateButton(QPushButton):
    """Custom translate button with enhanced functionality."""
    
    translation_requested = pyqtSignal()
    
    def __init__(self, parent: Optional[QWidget] = None):
        """Initialize translate button."""
        super().__init__("Translate", parent)
        
        self.original_text = "Translate"
        self.processing_text = "Translating..."
        self.is_processing = False
        
        # Animation timer for processing state
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self._update_processing_animation)
        self.animation_dots = 0
        
        self._setup_button()
        self._connect_signals()
    
    def _setup_button(self) -> None:
        """Setup button appearance and properties."""
        self.setMinimumHeight(40)
        self.setMinimumWidth(120)
        
        # Apply styling
        self.setStyleSheet("""
            TranslateButton {
                background-color: #0078d4;
                color: white;
                border: none;
                border-radius: 4px;
                font-size: 14px;
                font-weight: bold;
                padding: 8px 16px;
            }
            
            TranslateButton:hover {
                background-color: #106ebe;
            }
            
            TranslateButton:pressed {
                background-color: #005a9e;
            }
            
            TranslateButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
            
            TranslateButton[processing="true"] {
                background-color: #ffa500;
                color: white;
            }
        """)
    
    def _connect_signals(self) -> None:
        """Connect button signals."""
        self.clicked.connect(self._on_clicked)
    
    def _on_clicked(self) -> None:
        """Handle button click."""
        if not self.is_processing:
            self.translation_requested.emit()
    
    def start_processing(self) -> None:
        """Set button to processing state."""
        self.is_processing = True
        self.setEnabled(False)
        self.setProperty("processing", True)
        self.style().polish(self)
        
        # Start animation
        self.animation_dots = 0
        self.animation_timer.start(500)  # Update every 500ms
        self._update_processing_animation()
    
    def stop_processing(self) -> None:
        """Stop processing state and return to normal."""
        self.is_processing = False
        self.setEnabled(True)
        self.setProperty("processing", False)
        self.style().polish(self)
        
        # Stop animation
        self.animation_timer.stop()
        self.setText(self.original_text)
    
    def _update_processing_animation(self) -> None:
        """Update processing animation."""
        if self.is_processing:
            dots = "." * (self.animation_dots % 4)
            self.setText(f"{self.processing_text}{dots}")
            self.animation_dots += 1
    
    def set_text(self, text: str) -> None:
        """Set button text."""
        self.original_text = text
        if not self.is_processing:
            self.setText(text)
    
    def set_processing_text(self, text: str) -> None:
        """Set text displayed during processing."""
        self.processing_text = text
    
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
    
    def reset_state(self) -> None:
        """Reset button to initial state."""
        self.stop_processing()
        self.setEnabled(True)
        self.setToolTip("")
