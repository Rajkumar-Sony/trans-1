"""
Source Language Combo Box Component

Modern QComboBox implementation for source language selection.
"""

from PyQt6.QtWidgets import QComboBox
from PyQt6.QtCore import pyqtSignal, Qt
from typing import Dict, Optional, List


class SourceLanguageComboBox(QComboBox):
    """Custom combo box for source language selection with modern styling."""
    
    # Signals
    language_changed = pyqtSignal(str)  # Emits language code
    
    def __init__(self, parent=None):
        """Initialize the source language combo box."""
        super().__init__(parent)
        self._language_codes: Dict[str, str] = {}
        self._setup_ui()
        self._connect_signals()
    
    def _setup_ui(self):
        """Set up the UI components."""
        self.setObjectName("sourceLanguageComboBox")
        self.setToolTip("Select source language for translation")
        self.setEditable(False)
        self.setMaxVisibleItems(10)
        
        # Set initial state
        self.setCurrentIndex(-1)
        
        # Enable wheel events only when focused
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
    
    def _connect_signals(self):
        """Connect internal signals."""
        self.currentTextChanged.connect(self._on_selection_changed)
    
    def _on_selection_changed(self, text: str):
        """Handle selection change."""
        if text and text in self._language_codes:
            language_code = self._language_codes[text]
            self.language_changed.emit(language_code)
    
    def load_languages(self, languages: Dict[str, str]):
        """
        Load available languages.
        
        Args:
            languages: Dict mapping language codes to display names
        """
        self.clear()
        self._language_codes.clear()
        
        # Sort languages by display name
        sorted_languages = sorted(languages.items(), key=lambda x: x[1])
        
        for code, name in sorted_languages:
            self.addItem(name)
            self._language_codes[name] = code
    
    def set_language(self, language_code: str):
        """
        Set the selected language by code.
        
        Args:
            language_code: The language code to select
        """
        for name, code in self._language_codes.items():
            if code == language_code:
                self.setCurrentText(name)
                break
    
    def get_selected_language(self) -> Optional[str]:
        """
        Get the currently selected language code.
        
        Returns:
            The selected language code or None if nothing selected
        """
        current_text = self.currentText()
        return self._language_codes.get(current_text)
    
    def get_display_text(self) -> str:
        """
        Get the current display text.
        
        Returns:
            The current display text
        """
        return self.currentText()
    
    def add_auto_detect_option(self):
        """Add auto-detect option to the combo box."""
        self.insertItem(0, "Auto-detect")
        self._language_codes["Auto-detect"] = "auto"
        self.setCurrentIndex(0)
    
    def set_placeholder_text(self, text: str):
        """
        Set placeholder text when no selection is made.
        
        Args:
            text: The placeholder text
        """
        if self.count() == 0 or not self.currentText():
            self.addItem(text)
            self.setCurrentIndex(0)
            self.setItemData(0, False, Qt.ItemDataRole.UserRole)
    
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
            True if a valid language is selected
        """
        return bool(self.get_selected_language())
    
    def get_language_list(self) -> List[str]:
        """
        Get list of available language codes.
        
        Returns:
            List of language codes
        """
        return list(self._language_codes.values())
    
    def clear_selection(self):
        """Clear the current selection."""
        self.setCurrentIndex(-1)
    
    def is_auto_detect_selected(self) -> bool:
        """
        Check if auto-detect is selected.
        
        Returns:
            True if auto-detect is selected
        """
        return self.get_selected_language() == "auto"
