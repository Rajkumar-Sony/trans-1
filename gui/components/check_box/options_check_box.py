"""
Options Check Box Component

Modern QCheckBox implementation for translation options.
"""

from PyQt6.QtWidgets import QCheckBox, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGroupBox
from PyQt6.QtCore import pyqtSignal, Qt
from typing import Dict, List, Optional


class OptionsCheckBox(QCheckBox):
    """Custom checkbox for translation options with modern styling."""
    
    # Signals
    option_changed = pyqtSignal(str, bool)  # Emits option name and state
    
    def __init__(self, option_name: str, description: str = "", parent=None):
        """
        Initialize the options checkbox.
        
        Args:
            option_name: Internal name of the option
            description: User-friendly description
            parent: Parent widget
        """
        super().__init__(parent)
        self._option_name = option_name
        self._description = description
        self._setup_ui()
        self._connect_signals()
    
    def _setup_ui(self):
        """Set up the UI components."""
        self.setObjectName(f"option_{self._option_name}")
        self.setText(self._description or self._option_name.replace('_', ' ').title())
        
        # Set tooltip with additional information
        self._set_tooltip()
    
    def _connect_signals(self):
        """Connect internal signals."""
        self.stateChanged.connect(self._on_state_changed)
    
    def _on_state_changed(self, state: int):
        """Handle state change."""
        is_checked = state == Qt.CheckState.Checked.value
        self.option_changed.emit(self._option_name, is_checked)
    
    def _set_tooltip(self):
        """Set tooltip based on option type."""
        tooltips = {
            'preserve_formatting': 'Maintain cell formatting like bold, italic, colors',
            'skip_empty_cells': 'Do not translate empty or whitespace-only cells',
            'skip_formulas': 'Skip cells containing Excel formulas',
            'skip_headers': 'Skip the first row (typically headers)',
            'case_sensitive': 'Preserve original text casing in translation',
            'batch_processing': 'Process multiple cells together for better context',
            'auto_detect_language': 'Automatically detect source language',
            'preserve_hyperlinks': 'Maintain clickable links in cells',
            'backup_original': 'Create backup copy of original file',
            'show_progress': 'Display detailed progress information',
        }
        
        tooltip = tooltips.get(self._option_name, self._description)
        if tooltip:
            self.setToolTip(tooltip)
    
    def get_option_name(self) -> str:
        """
        Get the option name.
        
        Returns:
            Option name
        """
        return self._option_name
    
    def get_description(self) -> str:
        """
        Get the option description.
        
        Returns:
            Option description
        """
        return self._description
    
    def set_checked_silent(self, checked: bool):
        """
        Set checked state without emitting signals.
        
        Args:
            checked: Whether to check the box
        """
        self.blockSignals(True)
        self.setChecked(checked)
        self.blockSignals(False)


class TranslationOptionsGroup(QGroupBox):
    """Group widget containing multiple translation option checkboxes."""
    
    # Signals
    options_changed = pyqtSignal(dict)  # Emits all option states
    
    def __init__(self, title: str = "Translation Options", parent=None):
        """
        Initialize the options group.
        
        Args:
            title: Group title
            parent: Parent widget
        """
        super().__init__(title, parent)
        self._checkboxes: Dict[str, OptionsCheckBox] = {}
        self._setup_ui()
    
    def _setup_ui(self):
        """Set up the UI layout."""
        self.setObjectName("translationOptionsGroup")
        layout = QVBoxLayout(self)
        layout.setSpacing(8)
        
        # Define default options
        default_options = [
            ('preserve_formatting', 'Preserve cell formatting'),
            ('skip_empty_cells', 'Skip empty cells'),
            ('skip_formulas', 'Skip formula cells'),
            ('auto_detect_language', 'Auto-detect source language'),
            ('batch_processing', 'Enable batch processing'),
        ]
        
        for option_name, description in default_options:
            self.add_option(option_name, description)
    
    def add_option(self, option_name: str, description: str, checked: bool = False):
        """
        Add a new option checkbox.
        
        Args:
            option_name: Internal name of the option
            description: User-friendly description
            checked: Initial checked state
        """
        checkbox = OptionsCheckBox(option_name, description, self)
        checkbox.setChecked(checked)
        checkbox.option_changed.connect(self._on_option_changed)
        
        self._checkboxes[option_name] = checkbox
        self.layout().addWidget(checkbox)
    
    def remove_option(self, option_name: str):
        """
        Remove an option checkbox.
        
        Args:
            option_name: Name of the option to remove
        """
        if option_name in self._checkboxes:
            checkbox = self._checkboxes[option_name]
            self.layout().removeWidget(checkbox)
            checkbox.deleteLater()
            del self._checkboxes[option_name]
            self._emit_options_changed()
    
    def _on_option_changed(self, option_name: str, checked: bool):
        """Handle individual option change."""
        self._emit_options_changed()
    
    def _emit_options_changed(self):
        """Emit signal with all current option states."""
        options = self.get_all_options()
        self.options_changed.emit(options)
    
    def get_option_state(self, option_name: str) -> Optional[bool]:
        """
        Get the state of a specific option.
        
        Args:
            option_name: Name of the option
            
        Returns:
            Option state or None if not found
        """
        checkbox = self._checkboxes.get(option_name)
        return checkbox.isChecked() if checkbox else None
    
    def set_option_state(self, option_name: str, checked: bool, silent: bool = False):
        """
        Set the state of a specific option.
        
        Args:
            option_name: Name of the option
            checked: Whether to check the option
            silent: Whether to suppress signals
        """
        checkbox = self._checkboxes.get(option_name)
        if checkbox:
            if silent:
                checkbox.set_checked_silent(checked)
            else:
                checkbox.setChecked(checked)
    
    def get_all_options(self) -> Dict[str, bool]:
        """
        Get all option states.
        
        Returns:
            Dictionary mapping option names to their states
        """
        return {
            name: checkbox.isChecked()
            for name, checkbox in self._checkboxes.items()
        }
    
    def set_all_options(self, options: Dict[str, bool], silent: bool = False):
        """
        Set multiple option states.
        
        Args:
            options: Dictionary of option states
            silent: Whether to suppress signals
        """
        for option_name, checked in options.items():
            self.set_option_state(option_name, checked, silent)
        
        if not silent:
            self._emit_options_changed()
    
    def reset_to_defaults(self):
        """Reset all options to default states."""
        defaults = {
            'preserve_formatting': True,
            'skip_empty_cells': True,
            'skip_formulas': True,
            'auto_detect_language': False,
            'batch_processing': True,
        }
        
        self.set_all_options(defaults)
    
    def get_option_names(self) -> List[str]:
        """
        Get list of all option names.
        
        Returns:
            List of option names
        """
        return list(self._checkboxes.keys())
    
    def enable_option(self, option_name: str, enabled: bool = True):
        """
        Enable or disable a specific option.
        
        Args:
            option_name: Name of the option
            enabled: Whether to enable the option
        """
        checkbox = self._checkboxes.get(option_name)
        if checkbox:
            checkbox.setEnabled(enabled)
    
    def enable_all_options(self, enabled: bool = True):
        """
        Enable or disable all options.
        
        Args:
            enabled: Whether to enable all options
        """
        for checkbox in self._checkboxes.values():
            checkbox.setEnabled(enabled)


class AdvancedOptionsGroup(QGroupBox):
    """Group widget for advanced translation options."""
    
    # Signals
    advanced_options_changed = pyqtSignal(dict)
    
    def __init__(self, parent=None):
        """Initialize the advanced options group."""
        super().__init__("Advanced Options", parent)
        self._checkboxes: Dict[str, OptionsCheckBox] = {}
        self._setup_ui()
    
    def _setup_ui(self):
        """Set up the UI layout."""
        self.setObjectName("advancedOptionsGroup")
        self.setCheckable(True)
        self.setChecked(False)  # Collapsed by default
        
        layout = QVBoxLayout(self)
        layout.setSpacing(6)
        
        # Advanced options
        advanced_options = [
            ('preserve_hyperlinks', 'Preserve hyperlinks'),
            ('backup_original', 'Create backup copy'),
            ('case_sensitive', 'Case-sensitive translation'),
            ('show_progress', 'Show detailed progress'),
        ]
        
        for option_name, description in advanced_options:
            checkbox = OptionsCheckBox(option_name, description, self)
            checkbox.option_changed.connect(self._on_option_changed)
            self._checkboxes[option_name] = checkbox
            layout.addWidget(checkbox)
        
        # Connect group toggle
        self.toggled.connect(self._on_group_toggled)
    
    def _on_option_changed(self, option_name: str, checked: bool):
        """Handle individual option change."""
        options = {
            name: checkbox.isChecked()
            for name, checkbox in self._checkboxes.items()
        }
        self.advanced_options_changed.emit(options)
    
    def _on_group_toggled(self, checked: bool):
        """Handle group toggle."""
        # Enable/disable all child checkboxes
        for checkbox in self._checkboxes.values():
            checkbox.setVisible(checked)
    
    def get_advanced_options(self) -> Dict[str, bool]:
        """
        Get all advanced option states.
        
        Returns:
            Dictionary of advanced option states
        """
        if not self.isChecked():
            return {}  # Return empty dict if group is collapsed
            
        return {
            name: checkbox.isChecked()
            for name, checkbox in self._checkboxes.items()
        }
    
    def set_advanced_options(self, options: Dict[str, bool]):
        """
        Set advanced option states.
        
        Args:
            options: Dictionary of option states
        """
        for option_name, checked in options.items():
            checkbox = self._checkboxes.get(option_name)
            if checkbox:
                checkbox.setChecked(checked)
