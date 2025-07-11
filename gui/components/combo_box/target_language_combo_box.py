"""
Target Language Combo Box Component

Modern QComboBox implementation for target language selection.
"""

from PyQt6.QtWidgets import QComboBox
from PyQt6.QtCore import pyqtSignal, Qt
from typing import Dict, Optional, List


class TargetLanguageComboBox(QComboBox):
    """Custom combo box for target language selection with modern styling."""
    
    # Signals
    language_changed = pyqtSignal(str)  # Emits language code
    
    def __init__(self, parent=None):
        """Initialize the target language combo box."""
        super().__init__(parent)
        self._language_codes: Dict[str, str] = {}
        self._excluded_codes: List[str] = []
        self._setup_ui()
        self._connect_signals()
    
    def _setup_ui(self):
        """Set up the UI components."""
        self.setObjectName("targetLanguageComboBox")
        self.setToolTip("Select target language for translation")
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
        
        # Filter out excluded languages
        filtered_languages = {
            code: name for code, name in languages.items()
            if code not in self._excluded_codes
        }
        
        # Sort languages by display name
        sorted_languages = sorted(filtered_languages.items(), key=lambda x: x[1])
        
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
    
    def exclude_languages(self, language_codes: List[str]):
        """
        Exclude specific languages from selection.
        
        Args:
            language_codes: List of language codes to exclude
        """
        self._excluded_codes = language_codes
        
        # Remove excluded languages from current items
        for i in range(self.count() - 1, -1, -1):
            item_text = self.itemText(i)
            if item_text in self._language_codes:
                code = self._language_codes[item_text]
                if code in self._excluded_codes:
                    self.removeItem(i)
                    del self._language_codes[item_text]
    
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
    
    def is_same_as_source(self, source_code: str) -> bool:
        """
        Check if selected language is same as source.
        
        Args:
            source_code: Source language code to compare
            
        Returns:
            True if same as source
        """
        selected = self.get_selected_language()
        return selected == source_code if selected else False
    
    def get_popular_languages(self) -> List[str]:
        """
        Get list of popular language codes for quick access.
        
        Returns:
            List of popular language codes
        """
        popular = ['en', 'es', 'fr', 'de', 'it', 'pt', 'ru', 'ja', 'ko', 'zh']
        return [code for code in popular if code in self.get_language_list()]
    
    def set_recommended_language(self, language_code: str):
        """
        Set a recommended language with visual indication.
        
        Args:
            language_code: The recommended language code
        """
        for name, code in self._language_codes.items():
            if code == language_code:
                # Find the item index
                index = self.findText(name)
                if index >= 0:
                    # Add visual indication (could be styled with CSS)
                    self.setItemData(index, "recommended", Qt.ItemDataRole.UserRole + 1)
                    self.setCurrentIndex(index)
                break
