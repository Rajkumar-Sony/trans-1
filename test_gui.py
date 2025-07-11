"""
Simple Main Window for Testing

A simplified version of the main window to test the GUI components without
the full architecture dependencies.
"""

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt

# Import GUI components directly
from gui.components.button.translate_button import TranslateButton
from gui.components.button.cancel_button import CancelButton
from gui.components.button.export_button import ExportButton
from gui.components.button.select_file_button import SelectFileButton
from gui.components.combo_box.source_language_combo_box import SourceLanguageComboBox
from gui.components.combo_box.target_language_combo_box import TargetLanguageComboBox
from gui.components.drag_and_drop.file_drop_zone import FileDropZone
from gui.components.progress_bar.translation_progress_bar import TranslationProgressBar
from gui.components.check_box.options_check_box import TranslationOptionsGroup

# Import styles
from gui.styles.global_style import get_application_stylesheet


class SimpleMainWindow(QMainWindow):
    """Simple main window for testing GUI components."""
    
    def __init__(self):
        """Initialize the simple main window."""
        super().__init__()
        self._setup_ui()
        self._setup_test_data()
        self._connect_signals()
    
    def _setup_ui(self):
        """Set up the UI components."""
        self.setWindowTitle("Excel Translator - Component Test")
        self.setMinimumSize(800, 600)
        
        # Apply global styles
        try:
            stylesheet = get_application_stylesheet()
            self.setStyleSheet(stylesheet)
        except Exception as e:
            print(f"Could not apply stylesheet: {e}")
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(16)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title_label = QLabel("Excel Translator - GUI Component Test")
        title_label.setObjectName("titleLabel")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)
        
        # File drop zone
        self.file_drop_zone = FileDropZone()
        main_layout.addWidget(self.file_drop_zone)
        
        # Language selection
        lang_layout = QHBoxLayout()
        
        source_lang_label = QLabel("Source Language:")
        self.source_combo = SourceLanguageComboBox()
        
        target_lang_label = QLabel("Target Language:")
        self.target_combo = TargetLanguageComboBox()
        
        lang_layout.addWidget(source_lang_label)
        lang_layout.addWidget(self.source_combo)
        lang_layout.addStretch()
        lang_layout.addWidget(target_lang_label)
        lang_layout.addWidget(self.target_combo)
        
        main_layout.addLayout(lang_layout)
        
        # Options
        self.options_group = TranslationOptionsGroup()
        main_layout.addWidget(self.options_group)
        
        # Progress bar
        self.progress_bar = TranslationProgressBar()
        main_layout.addWidget(self.progress_bar)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.select_file_btn = SelectFileButton()
        self.translate_btn = TranslateButton()
        self.cancel_btn = CancelButton()
        self.export_btn = ExportButton()
        
        button_layout.addWidget(self.select_file_btn)
        button_layout.addStretch()
        button_layout.addWidget(self.translate_btn)
        button_layout.addWidget(self.cancel_btn)
        button_layout.addWidget(self.export_btn)
        
        main_layout.addLayout(button_layout)
        
        # Status bar
        self.statusBar().showMessage("Ready")
    
    def _setup_test_data(self):
        """Set up test data for the components."""
        # Test languages
        test_languages = {
            'en': 'English',
            'es': 'Spanish', 
            'fr': 'French',
            'de': 'German',
            'it': 'Italian',
            'pt': 'Portuguese',
            'ru': 'Russian',
            'ja': 'Japanese',
            'ko': 'Korean',
            'zh': 'Chinese'
        }
        
        self.source_combo.load_languages(test_languages)
        self.source_combo.add_auto_detect_option()
        
        self.target_combo.load_languages(test_languages)
        self.target_combo.set_language('en')
    
    def _connect_signals(self):
        """Connect component signals."""
        # File selection
        self.file_drop_zone.files_dropped.connect(self._on_files_dropped)
        self.select_file_btn.clicked.connect(self._on_select_file)
        
        # Translation
        self.translate_btn.clicked.connect(self._on_translate)
        self.cancel_btn.clicked.connect(self._on_cancel)
        self.export_btn.clicked.connect(self._on_export)
        
        # Language selection
        self.source_combo.language_changed.connect(self._on_source_language_changed)
        self.target_combo.language_changed.connect(self._on_target_language_changed)
        
        # Options
        self.options_group.options_changed.connect(self._on_options_changed)
    
    def _on_files_dropped(self, files):
        """Handle files dropped."""
        if files:
            self.statusBar().showMessage(f"File selected: {files[0]}")
            self.file_drop_zone.show_success(files[0])
        else:
            # Empty list means user clicked to browse
            self._on_select_file()
    
    def _on_select_file(self):
        """Handle file selection button."""
        from PyQt6.QtWidgets import QFileDialog
        
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Excel File",
            "",
            "Excel Files (*.xlsx *.xlsm *.xls);;All Files (*)"
        )
        
        if file_path:
            self.statusBar().showMessage(f"File selected: {file_path}")
            self.file_drop_zone.show_success(file_path)
    
    def _on_translate(self):
        """Handle translate button."""
        self.progress_bar.start_operation("Translating", 100)
        self.statusBar().showMessage("Translation started...")
        
        # Simulate progress
        import random
        for i in range(0, 101, 10):
            self.progress_bar.update_progress(i, f"Processing item {i}")
    
    def _on_cancel(self):
        """Handle cancel button."""
        self.progress_bar.cancel_operation()
        self.statusBar().showMessage("Translation cancelled")
    
    def _on_export(self):
        """Handle export button."""
        self.statusBar().showMessage("Export functionality not implemented in test mode")
    
    def _on_source_language_changed(self, language_code):
        """Handle source language change."""
        self.statusBar().showMessage(f"Source language: {language_code}")
    
    def _on_target_language_changed(self, language_code):
        """Handle target language change."""
        self.statusBar().showMessage(f"Target language: {language_code}")
    
    def _on_options_changed(self, options):
        """Handle options change."""
        enabled_options = [name for name, enabled in options.items() if enabled]
        self.statusBar().showMessage(f"Options: {', '.join(enabled_options)}")


def main():
    """Main function to run the simple test application."""
    app = QApplication(sys.argv)
    app.setApplicationName("Excel Translator - Component Test")
    
    window = SimpleMainWindow()
    window.show()
    
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
