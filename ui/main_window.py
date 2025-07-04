import sys
import os
import json
import logging
from pathlib import Path
from typing import Optional, Dict, Any

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QPushButton, QFileDialog, QComboBox, QProgressBar, 
    QTextEdit, QGroupBox, QGridLayout, QMessageBox, QStatusBar,
    QMenuBar, QMenu, QDialog, QDialogButtonBox, QLineEdit, QSpinBox,
    QSizePolicy
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt6.QtGui import QAction, QIcon, QFont

from translator.deepl_client import DeepLClient
from translator.batch_processor import TranslationManager, TranslationTask
from excel.excel_reader import ExcelReader
from excel.excel_writer import ExcelWriter
from excel.utils import ExcelUtils

class TranslationThread(QThread):
    """Thread for handling translation operations."""
    
    progress_updated = pyqtSignal(str, int)  # sheet_name, progress
    translation_completed = pyqtSignal(bool)  # success
    error_occurred = pyqtSignal(str)  # error_message
    
    def __init__(self, translation_manager: TranslationManager):
        super().__init__()
        self.translation_manager = translation_manager
    
    def run(self):
        """Run the translation process."""
        try:
            self.translation_manager.start_processing(
                progress_callback=self.progress_updated.emit,
                completion_callback=self.translation_completed.emit
            )
        except Exception as e:
            self.error_occurred.emit(str(e))

class SettingsDialog(QDialog):
    """Settings dialog for API key and app configuration."""
    
    def __init__(self, parent=None, settings=None):
        super().__init__(parent)
        self.settings = settings or {}
        self.setWindowTitle("Settings")
        self.setFixedSize(400, 300)
        self.init_ui()
    
    def init_ui(self):
        """Initialize the settings UI."""
        # Set smaller font for the entire dialog
        dialog_font = QFont()
        dialog_font.setPointSize(9)  # Reduced font size for the dialog
        self.setFont(dialog_font)
        
        layout = QVBoxLayout()
        
        # API Key section
        api_group = QGroupBox("DeepL API Configuration")
        api_layout = QGridLayout()
        
        api_layout.addWidget(QLabel("API Key:"), 0, 0)
        self.api_key_input = QLineEdit()
        self.api_key_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.api_key_input.setText(self.settings.get('api_key', ''))
        api_layout.addWidget(self.api_key_input, 0, 1)
        
        api_group.setLayout(api_layout)
        layout.addWidget(api_group)
        
        # App Configuration section
        app_group = QGroupBox("Application Settings")
        app_layout = QGridLayout()
        
        app_layout.addWidget(QLabel("App Language:"), 0, 0)
        self.app_language_combo = QComboBox()
        
        # Use language display names for app language too
        app_languages = ["🇺🇸 English", "🇯🇵 日本語 (Japanese)", "🇻🇳 Tiếng Việt (Vietnamese)"]
        self.app_language_combo.addItems(app_languages)
        self.app_language_combo.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.app_language_combo.setFixedWidth(100)  # Very small width
        self.app_language_combo.setFixedHeight(12)  # Ultra compressed height
        
        # Set smaller font for the combo box
        combo_font = QFont()
        combo_font.setPointSize(6)  # Ultra small font size
        self.app_language_combo.setFont(combo_font)
        
        # Set current selection based on saved setting
        current_app_lang = self.settings.get('app_language', 'en')
        app_lang_mapping = {'en': '🇺🇸 English', 'ja': '🇯🇵 日本語 (Japanese)', 'vi': '🇻🇳 Tiếng Việt (Vietnamese)'}
        current_app_display = app_lang_mapping.get(current_app_lang, '🇺🇸 English')
        self.app_language_combo.setCurrentText(current_app_display)
        
        app_layout.addWidget(self.app_language_combo, 0, 1)
        
        app_group.setLayout(app_layout)
        layout.addWidget(app_group)
        
        # Buttons
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
        
        self.setLayout(layout)
    
    def get_settings(self) -> Dict[str, Any]:
        """Get the current settings from the dialog."""
        # Convert app language display name back to code
        app_lang_reverse_mapping = {'🇺🇸 English': 'en', '🇯🇵 日本語 (Japanese)': 'ja', '🇻🇳 Tiếng Việt (Vietnamese)': 'vi'}
        app_lang_display = self.app_language_combo.currentText()
        app_lang_code = app_lang_reverse_mapping.get(app_lang_display, 'en')
        
        return {
            'api_key': self.api_key_input.text(),
            'app_language': app_lang_code
        }

class ExcelTranslatorApp(QMainWindow):
    """Main application window."""
    
    def __init__(self):
        super().__init__()
        self.settings = {}
        self.translations = {}  # Stores translations for each language
        self.deepl_client = None
        self.translation_manager = None
        self.excel_reader = None
        self.current_file_path = None
        self.sheet_info = {}
        
        # Language mapping for display
        self.language_mapping = {
            'en': '🇺🇸 English',
            'ja': '🇯🇵 日本語 (Japanese)', 
            'vi': '🇻🇳 Tiếng Việt (Vietnamese)'
        }
        
        # Reverse mapping for getting codes from names
        self.language_codes = {v: k for k, v in self.language_mapping.items()}
        
        self.init_logging()
        self.load_settings()
        self.load_translations()
        self.init_ui()
        self.apply_theme()
        
        # Initialize DeepL client if API key is available
        if self.settings.get('api_key'):
            self.init_deepl_client()
    
    def init_logging(self):
        """Initialize logging."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
    
    def load_settings(self):
        """Load application settings."""
        settings_file = Path(__file__).parent.parent / 'config' / 'settings.json'
        try:
            if settings_file.exists():
                with open(settings_file, 'r', encoding='utf-8') as f:
                    self.settings = json.load(f)
        except Exception as e:
            self.logger.error(f"Failed to load settings: {e}")
            self.settings = {}
    
    def save_settings(self):
        """Save application settings."""
        settings_file = Path(__file__).parent.parent / 'config' / 'settings.json'
        try:
            settings_file.parent.mkdir(exist_ok=True)
            with open(settings_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=2)
        except Exception as e:
            self.logger.error(f"Failed to save settings: {e}")
    
    def load_translations(self):
        """Load UI translations."""
        i18n_dir = Path(__file__).parent.parent / 'i18n'
        app_lang = self.settings.get('app_language', 'en')
        
        try:
            translation_file = i18n_dir / f'{app_lang}.json'
            if translation_file.exists():
                with open(translation_file, 'r', encoding='utf-8') as f:
                    self.translations = json.load(f)
        except Exception as e:
            self.logger.error(f"Failed to load translations: {e}")
            self.translations = {}
    
    def tr(self, key: str) -> str:
        """Get translated string."""
        return self.translations.get(key, key)
    
    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle(self.tr("app_title"))
        self.setGeometry(100, 100, 900, 700)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Create menu bar
        self.create_menu_bar()
        
        # File selection section
        file_group = QGroupBox(self.tr("upload_file"))
        file_layout = QHBoxLayout()
        
        self.file_path_label = QLabel(self.tr("no_file_selected"))
        self.file_path_label.setStyleSheet("color: #808080;")
        
        self.select_file_btn = QPushButton(self.tr("select_file"))
        self.select_file_btn.clicked.connect(self.select_file)
        self.select_file_btn.setFixedWidth(243)  # Set fixed width for Select File button
        
        file_layout.addWidget(self.file_path_label)
        file_layout.addWidget(self.select_file_btn)
        file_group.setLayout(file_layout)
        main_layout.addWidget(file_group)
        
        # Sheet information section
        self.sheet_info_group = QGroupBox(self.tr("sheets_detected"))
        self.sheet_info_layout = QVBoxLayout()
        self.sheet_info_label = QLabel("")
        self.sheet_info_layout.addWidget(self.sheet_info_label)
        self.sheet_info_group.setLayout(self.sheet_info_layout)
        self.sheet_info_group.setVisible(False)
        main_layout.addWidget(self.sheet_info_group)
        
        # Language selection section
        lang_group = QGroupBox("Language Settings")
        lang_layout = QGridLayout()
        
        # Set column stretch to push ComboBoxes to the right with flexible sizing
        lang_layout.setColumnStretch(0, 0)  # Label column - no stretch
        lang_layout.setColumnStretch(1, 1)  # Spacer column - expands to push combo to right
        lang_layout.setColumnStretch(2, 0)  # ComboBox column - no stretch
        
        lang_layout.addWidget(QLabel(self.tr("source_language")), 0, 0)
        self.source_lang_combo = QComboBox()
        
        # Add language items with display names
        source_languages = ["🇯🇵 日本語 (Japanese)", "🇺🇸 English", "🇻🇳 Tiếng Việt (Vietnamese)"]
        self.source_lang_combo.addItems(source_languages)
        self.source_lang_combo.setFixedWidth(400)  # Set fixed width to match image proportions
        
        
        # Set current selection based on saved setting
        current_source_code = self.settings.get('last_source_lang', 'ja')
        current_source_display = self.get_language_display_name(current_source_code)
        self.source_lang_combo.setCurrentText(current_source_display)
        
        lang_layout.addWidget(self.source_lang_combo, 0, 2)  # Right-aligned in column 2
        
        lang_layout.addWidget(QLabel(self.tr("target_language")), 1, 0)
        self.target_lang_combo = QComboBox()
        
        # Add language items with display names
        target_languages = ["🇺🇸 English", "🇯🇵 日本語 (Japanese)", "🇻🇳 Tiếng Việt (Vietnamese)"]
        self.target_lang_combo.addItems(target_languages)
        self.target_lang_combo.setFixedWidth(400)  # Set fixed width to match image proportions
        
        
        # Set current selection based on saved setting
        current_target_code = self.settings.get('last_target_lang', 'en')
        current_target_display = self.get_language_display_name(current_target_code)
        self.target_lang_combo.setCurrentText(current_target_display)
        
        lang_layout.addWidget(self.target_lang_combo, 1, 2)  # Right-aligned in column 2
        
        lang_group.setLayout(lang_layout)
        main_layout.addWidget(lang_group)
        
        # Action buttons
        button_layout = QHBoxLayout()
        
        self.translate_btn = QPushButton(self.tr("translate"))
        self.translate_btn.clicked.connect(self.start_translation)
        self.translate_btn.setEnabled(False)
        
        self.export_btn = QPushButton(self.tr("export"))
        self.export_btn.clicked.connect(self.export_file)
        self.export_btn.setEnabled(False)
        
        self.cancel_btn = QPushButton(self.tr("cancel"))
        self.cancel_btn.clicked.connect(self.cancel_translation)
        self.cancel_btn.setEnabled(False)
        
        button_layout.addWidget(self.translate_btn)
        button_layout.addWidget(self.export_btn)
        button_layout.addWidget(self.cancel_btn)
        button_layout.addStretch()
        
        main_layout.addLayout(button_layout)
        
        # Progress section
        progress_group = QGroupBox(self.tr("progress"))
        progress_layout = QVBoxLayout()
        
        self.progress_bar = QProgressBar()
        self.progress_label = QLabel("")
        
        progress_layout.addWidget(self.progress_bar)
        progress_layout.addWidget(self.progress_label)
        progress_group.setLayout(progress_layout)
        main_layout.addWidget(progress_group)
        
        # Log section
        log_group = QGroupBox("Log")
        log_layout = QVBoxLayout()
        
        self.log_text = QTextEdit()
        self.log_text.setMaximumHeight(150)
        self.log_text.setReadOnly(True)
        
        log_layout.addWidget(self.log_text)
        log_group.setLayout(log_layout)
        main_layout.addWidget(log_group)
        
        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
    
    def create_menu_bar(self):
        """Create the application menu bar."""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu('File')
        
        open_action = QAction('Open Excel File', self)
        open_action.triggered.connect(self.select_file)
        file_menu.addAction(open_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction('Exit', self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Settings menu
        settings_menu = menubar.addMenu('Settings')
        
        settings_action = QAction('Preferences', self)
        settings_action.triggered.connect(self.open_settings)
        settings_menu.addAction(settings_action)
    
    def apply_theme(self):
        """Apply the dark theme."""
        theme_file = Path(__file__).parent.parent / 'assets' / 'dark_theme.qss'
        try:
            if theme_file.exists():
                with open(theme_file, 'r', encoding='utf-8') as f:
                    self.setStyleSheet(f.read())
        except Exception as e:
            self.logger.error(f"Failed to apply theme: {e}")
    
    def init_deepl_client(self):
        """Initialize DeepL client."""
        try:
            api_key = self.settings.get('api_key')
            if not api_key:
                return
            
            self.deepl_client = DeepLClient(api_key)
            self.translation_manager = TranslationManager(self.deepl_client)
            
            self.log_message("DeepL client initialized successfully")
            self.status_bar.showMessage("DeepL API connected")
            
        except Exception as e:
            self.log_message(f"Failed to initialize DeepL client: {str(e)}")
            self.status_bar.showMessage("DeepL API connection failed")
    
    def select_file(self):
        """Open file dialog to select Excel file."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            self.tr("select_file"),
            "",
            "Excel Files (*.xlsx *.xlsm *.xls)"
        )
        
        if file_path:
            self.load_excel_file(file_path)
    
    def load_excel_file(self, file_path: str):
        """Load and analyze Excel file."""
        try:
            self.current_file_path = file_path
            self.excel_reader = ExcelReader(file_path)
            
            # Get sheet information
            self.sheet_info = self.excel_reader.get_sheet_info()
            
            # Auto-calculate optimal batch size if translation manager is available
            if self.translation_manager:
                from excel.utils import ExcelUtils
                file_characteristics = ExcelUtils.analyze_file_characteristics(file_path, self.sheet_info)
                optimal_batch_size = self.translation_manager.set_optimal_batch_size_from_file(file_characteristics)
                
                self.log_message(f"Auto-calculated optimal batch size: {optimal_batch_size} for {file_characteristics['total_texts']} texts")
            
            # Update UI
            self.file_path_label.setText(os.path.basename(file_path))
            self.file_path_label.setStyleSheet("color: #d4d4d4;")
            
            # Show sheet information
            sheet_info_text = ""
            for sheet_name, info in self.sheet_info.items():
                sheet_info_text += f"• {sheet_name}: {info['text_cells']} translatable cells\n"
            
            self.sheet_info_label.setText(sheet_info_text.strip())
            self.sheet_info_group.setVisible(True)
            
            # Enable translate button if API is ready
            if self.deepl_client and self.deepl_client.is_valid():
                self.translate_btn.setEnabled(True)
            
            self.log_message(f"Loaded Excel file: {os.path.basename(file_path)}")
            self.status_bar.showMessage(f"File loaded: {len(self.sheet_info)} sheets")
            
        except Exception as e:
            self.show_error(f"Failed to load Excel file: {str(e)}")
    
    def start_translation(self):
        """Start the translation process."""
        if not self.deepl_client or not self.excel_reader:
            self.show_error("Please configure API key and select a file first")
            return
        
        try:
            # Clear previous tasks
            self.translation_manager.clear_tasks()
            
            source_lang = self.get_current_source_language_code()
            target_lang = self.get_current_target_language_code()
            
            # Create translation tasks for each sheet
            for sheet_name in self.excel_reader.get_sheet_names():
                texts, positions = self.excel_reader.extract_translatable_content(sheet_name)
                
                if texts:
                    task = TranslationTask(
                        sheet_name=sheet_name,
                        texts=texts,
                        cell_positions=positions,
                        target_lang=target_lang,
                        source_lang=source_lang if source_lang != "auto" else None
                    )
                    self.translation_manager.add_task(task)
            
            # Update UI state
            self.translate_btn.setEnabled(False)
            self.cancel_btn.setEnabled(True)
            self.progress_bar.setValue(0)
            self.progress_label.setText("Starting translation...")
            
            # Start translation in separate thread
            self.translation_thread = TranslationThread(self.translation_manager)
            self.translation_thread.progress_updated.connect(self.update_progress)
            self.translation_thread.translation_completed.connect(self.translation_finished)
            self.translation_thread.error_occurred.connect(self.translation_error)
            self.translation_thread.start()
            
            self.log_message("Translation started")
            self.status_bar.showMessage("Translating...")
            
        except Exception as e:
            self.show_error(f"Failed to start translation: {str(e)}")
    
    def update_progress(self, sheet_name: str, progress: int):
        """Update progress display."""
        self.progress_bar.setValue(progress)
        self.progress_label.setText(f"Translating sheet: {sheet_name} ({progress}%)")
    
    def translation_finished(self, success: bool):
        """Handle translation completion."""
        if success:
            self.log_message("Translation completed successfully")
            self.status_bar.showMessage("Translation completed")
            self.export_btn.setEnabled(True)
            self.show_info("Translation completed successfully!")
        else:
            self.log_message("Translation failed or was cancelled")
            self.status_bar.showMessage("Translation failed")
        
        # Reset UI state
        self.translate_btn.setEnabled(True)
        self.cancel_btn.setEnabled(False)
        self.progress_bar.setValue(0)
        self.progress_label.setText("")
    
    def translation_error(self, error_message: str):
        """Handle translation error."""
        self.log_message(f"Translation error: {error_message}")
        self.show_error(f"Translation failed: {error_message}")
        self.translation_finished(False)
    
    def cancel_translation(self):
        """Cancel ongoing translation."""
        if self.translation_manager:
            self.translation_manager.cancel_processing()
            self.log_message("Translation cancelled")
    
    def export_file(self):
        """Export translated Excel file."""
        if not self.translation_manager or not self.translation_manager.tasks:
            self.show_error("No translation data available")
            return
        
        try:
            # Get output file path
            output_path, _ = QFileDialog.getSaveFileName(
                self,
                "Save Translated File",
                ExcelWriter.generate_output_filename(self.current_file_path),
                "Excel Files (*.xlsx)"
            )
            
            if not output_path:
                return
            
            # Prepare translation data
            translation_data = {}
            for task in self.translation_manager.tasks:
                if task.status == "completed":
                    translation_data[task.sheet_name] = [
                        (translated_text, row, col)
                        for translated_text, (row, col) in zip(task.translated_texts, task.cell_positions)
                    ]
            
            # Create translated workbook
            excel_writer = ExcelWriter(self.current_file_path, output_path)
            excel_writer.create_translated_workbook(translation_data)
            
            self.log_message(f"File exported to: {output_path}")
            self.status_bar.showMessage("File exported successfully")
            self.show_info(f"File exported successfully to:\n{output_path}")
            
        except Exception as e:
            self.show_error(f"Failed to export file: {str(e)}")
    
    def open_settings(self):
        """Open settings dialog."""
        dialog = SettingsDialog(self, self.settings)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            new_settings = dialog.get_settings()
            self.settings.update(new_settings)
            self.save_settings()
            
            # Reinitialize DeepL client if API key changed
            if 'api_key' in new_settings:
                self.init_deepl_client()
            
            self.log_message("Settings updated")
    
    def log_message(self, message: str):
        """Add message to log display."""
        self.log_text.append(f"[{logging.Formatter().formatTime(logging.LogRecord('', 0, '', 0, '', (), None))}] {message}")
    
    def show_error(self, message: str):
        """Show error message."""
        QMessageBox.critical(self, self.tr("error"), message)
    
    def show_info(self, message: str):
        """Show information message."""
        QMessageBox.information(self, self.tr("success"), message)
    
    def closeEvent(self, event):
        """Handle application close event."""
        # Save current language settings using codes
        self.settings['last_source_lang'] = self.get_current_source_language_code()
        self.settings['last_target_lang'] = self.get_current_target_language_code()
        self.save_settings()
        
        # Cancel any ongoing translation
        if self.translation_manager:
            self.translation_manager.cancel_processing()
        
        event.accept()
    
    def get_language_display_name(self, code: str) -> str:
        """Get display name for language code."""
        return self.language_mapping.get(code, code)
    
    def get_language_code(self, display_name: str) -> str:
        """Get language code from display name."""
        return self.language_codes.get(display_name, display_name)
    
    def get_current_source_language_code(self) -> str:
        """Get current source language code."""
        if hasattr(self, 'source_lang_combo'):
            current_text = self.source_lang_combo.currentText()
            return self.get_language_code(current_text)
        return self.settings.get('last_source_lang', 'ja')
    
    def get_current_target_language_code(self) -> str:
        """Get current target language code."""
        if hasattr(self, 'target_lang_combo'):
            current_text = self.target_lang_combo.currentText()
            return self.get_language_code(current_text)
        return self.settings.get('last_target_lang', 'en')

def main():
    """Main application entry point."""
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("Excel Translator")
    app.setApplicationVersion("1.0")
    app.setOrganizationName("Excel Translator")
    
    # Create and show main window
    window = ExcelTranslatorApp()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
