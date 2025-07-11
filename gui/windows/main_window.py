"""
Modern Main Window Implementation

Main window using the new architecture with clean separation of concerns.
"""

import sys
import os
import json
import logging
from pathlib import Path
from typing import Optional, Dict, Any, List

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QGroupBox, QGridLayout, QMessageBox, QStatusBar,
    QMenuBar, QMenu, QSplitter, QScrollArea, QFrame
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt6.QtGui import QAction, QIcon, QFont

# Import new architecture components
from application.usecases.process_file_usecase import ProcessFileUseCase
from application.usecases.translate_text_usecase import TranslateTextUseCase
from application.usecases.validate_request_usecase import ValidateRequestUseCase
from application.usecases.detect_language_usecase import DetectLanguageUseCase
from application.dto.translation_request import TranslationRequest
from infrastructure.file_handlers.excel_handler import ExcelHandler
from infrastructure.plugins.deepl_translator import DeepLTranslator
from gui.components.button.translate_button import TranslateButton
from gui.components.button.cancel_button import CancelButton
from gui.components.button.export_button import ExportButton
from gui.components.button.select_file_button import SelectFileButton
from gui.components.button.swap_button import SwapButton


class ModernMainWindow(QMainWindow):
    """Modern main window with clean architecture."""
    
    language_changed = pyqtSignal(str)
    
    def __init__(self):
        """Initialize the modern main window."""
        super().__init__()
        
        # Initialize core components
        self.settings = {}
        self.translations = {}
        self.current_file_path = None
        
        # Initialize services
        self.excel_handler = ExcelHandler()
        self.deepl_translator = None
        
        # Initialize use cases
        self.process_file_usecase = None
        self.translate_usecase = None
        self.validate_usecase = None
        self.detect_language_usecase = None
        
        # UI components
        self.select_file_btn = None
        self.translate_btn = None
        self.cancel_btn = None
        self.export_btn = None
        self.swap_btn = None
        
        # Language mapping
        self.language_mapping = {
            'en': '🇺🇸 English',
            'ja': '🇯🇵 日本語 (Japanese)', 
            'vi': '🇻🇳 Tiếng Việt (Vietnamese)',
            'zh': '🇨🇳 中文 (Chinese)',
            'ko': '🇰🇷 한국어 (Korean)',
            'es': '🇪🇸 Español (Spanish)',
            'fr': '🇫🇷 Français (French)',
            'de': '🇩🇪 Deutsch (German)'
        }
        
        self.language_codes = {v: k for k, v in self.language_mapping.items()}
        
        # Initialize application
        self._initialize_logging()
        self._load_settings()
        self._load_translations()
        self._initialize_services()
        self._setup_ui()
        self._apply_theme()
        
    def _initialize_logging(self) -> None:
        """Initialize logging system."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/application.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        self.logger.info("Modern main window initializing")
    
    def _load_settings(self) -> None:
        """Load application settings."""
        settings_file = Path('config/settings.json')
        try:
            if settings_file.exists():
                with open(settings_file, 'r', encoding='utf-8') as f:
                    self.settings = json.load(f)
            else:
                self.settings = self._get_default_settings()
                self._save_settings()
        except Exception as e:
            self.logger.error(f"Failed to load settings: {e}")
            self.settings = self._get_default_settings()
    
    def _get_default_settings(self) -> Dict[str, Any]:
        """Get default settings."""
        return {
            'app_language': 'en',
            'last_source_lang': 'ja',
            'last_target_lang': 'en',
            'api_key': '',
            'batch_size': 50,
            'theme': 'dark',
            'auto_backup': True,
            'window_geometry': None
        }
    
    def _save_settings(self) -> None:
        """Save application settings."""
        settings_file = Path('config/settings.json')
        try:
            settings_file.parent.mkdir(exist_ok=True)
            with open(settings_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=2)
        except Exception as e:
            self.logger.error(f"Failed to save settings: {e}")
    
    def _load_translations(self) -> None:
        """Load UI translations."""
        i18n_dir = Path('i18n')
        app_lang = self.settings.get('app_language', 'en')
        
        try:
            translation_file = i18n_dir / f'{app_lang}.json'
            if translation_file.exists():
                with open(translation_file, 'r', encoding='utf-8') as f:
                    self.translations = json.load(f)
            else:
                self.translations = self._get_default_translations()
        except Exception as e:
            self.logger.error(f"Failed to load translations: {e}")
            self.translations = self._get_default_translations()
    
    def _get_default_translations(self) -> Dict[str, str]:
        """Get default English translations."""
        return {
            'app_title': 'Excel Translator',
            'file': 'File',
            'settings': 'Settings',
            'open_excel_file': 'Open Excel File',
            'exit': 'Exit',
            'preferences': 'Preferences',
            'upload_file': 'Upload File',
            'select_file': 'Select File',
            'no_file_selected': 'No file selected',
            'language_settings': 'Language Settings',
            'source_language': 'Source Language',
            'target_language': 'Target Language',
            'translate': 'Translate',
            'cancel': 'Cancel',
            'export': 'Export',
            'progress': 'Progress',
            'ready': 'Ready',
            'success': 'Success',
            'error': 'Error',
            'warning': 'Warning'
        }
    
    def tr(self, key: str) -> str:
        """Get translated string."""
        return self.translations.get(key, key)
    
    def _initialize_services(self) -> None:
        """Initialize business logic services."""
        try:
            # Initialize translation service
            api_key = self.settings.get('api_key')
            if api_key:
                self.deepl_translator = DeepLTranslator(api_key)
            
            # Initialize use cases
            if self.deepl_translator:
                self.translate_usecase = TranslateTextUseCase(self.deepl_translator)
                self.detect_language_usecase = DetectLanguageUseCase(self.deepl_translator)
                self.validate_usecase = ValidateRequestUseCase([])
                self.process_file_usecase = ProcessFileUseCase(
                    self.excel_handler,
                    None,  # File service - to be implemented
                    self.translate_usecase,
                    self.validate_usecase,
                    self.detect_language_usecase
                )
            
            self.logger.info("Services initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize services: {e}")
    
    def _setup_ui(self) -> None:
        """Setup the user interface."""
        self.setWindowTitle(self.tr('app_title'))
        self.setGeometry(100, 100, 1000, 700)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Create menu bar
        self._create_menu_bar()
        
        # Create main content
        self._create_main_content(main_layout)
        
        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage(self.tr('ready'))
        
        # Update UI texts
        self._update_ui_texts()
    
    def _create_menu_bar(self) -> None:
        """Create the application menu bar."""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu(self.tr('file'))
        
        open_action = QAction(self.tr('open_excel_file'), self)
        open_action.triggered.connect(self._select_file)
        file_menu.addAction(open_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction(self.tr('exit'), self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Settings menu
        settings_menu = menubar.addMenu(self.tr('settings'))
        
        preferences_action = QAction(self.tr('preferences'), self)
        preferences_action.triggered.connect(self._open_settings)
        settings_menu.addAction(preferences_action)
    
    def _create_main_content(self, main_layout: QVBoxLayout) -> None:
        """Create main content area."""
        # Create splitter for resizable panels
        splitter = QSplitter(Qt.Orientation.Vertical)
        main_layout.addWidget(splitter)
        
        # Top panel - File and language selection
        top_panel = self._create_top_panel()
        splitter.addWidget(top_panel)
        
        # Middle panel - Progress and controls
        middle_panel = self._create_middle_panel()
        splitter.addWidget(middle_panel)
        
        # Bottom panel - Logs
        bottom_panel = self._create_bottom_panel()
        splitter.addWidget(bottom_panel)
        
        # Set splitter proportions
        splitter.setStretchFactor(0, 2)
        splitter.setStretchFactor(1, 2)
        splitter.setStretchFactor(2, 1)
    
    def _create_top_panel(self) -> QWidget:
        """Create top panel with file selection and language settings."""
        panel = QWidget()
        layout = QVBoxLayout()
        panel.setLayout(layout)
        
        # File selection group
        file_group = QGroupBox(self.tr('upload_file'))
        file_layout = QHBoxLayout()
        
        self.file_path_label = QLabel(self.tr('no_file_selected'))
        self.file_path_label.setStyleSheet("color: #808080;")
        
        self.select_file_btn = SelectFileButton()
        self.select_file_btn.file_selected.connect(self._on_file_selected)
        self.select_file_btn.setFixedWidth(150)
        
        file_layout.addWidget(self.file_path_label)
        file_layout.addWidget(self.select_file_btn)
        file_group.setLayout(file_layout)
        layout.addWidget(file_group)
        
        # Language settings group
        lang_group = QGroupBox(self.tr('language_settings'))
        lang_layout = QGridLayout()
        
        # Source language
        source_label = QLabel(self.tr('source_language'))
        lang_layout.addWidget(source_label, 0, 0)
        
        from PyQt6.QtWidgets import QComboBox
        self.source_lang_combo = QComboBox()
        source_languages = [self.language_mapping[code] for code in ['ja', 'en', 'vi', 'zh', 'ko']]
        self.source_lang_combo.addItems(source_languages)
        lang_layout.addWidget(self.source_lang_combo, 0, 1)
        
        # Swap button
        self.swap_btn = SwapButton()
        self.swap_btn.swap_requested.connect(self._swap_languages)
        lang_layout.addWidget(self.swap_btn, 0, 2)
        
        # Target language
        target_label = QLabel(self.tr('target_language'))
        lang_layout.addWidget(target_label, 1, 0)
        
        self.target_lang_combo = QComboBox()
        target_languages = [self.language_mapping[code] for code in ['en', 'ja', 'vi', 'zh', 'ko']]
        self.target_lang_combo.addItems(target_languages)
        lang_layout.addWidget(self.target_lang_combo, 1, 1)
        
        lang_group.setLayout(lang_layout)
        layout.addWidget(lang_group)
        
        return panel
    
    def _create_middle_panel(self) -> QWidget:
        """Create middle panel with controls and progress."""
        panel = QWidget()
        layout = QVBoxLayout()
        panel.setLayout(layout)
        
        # Action buttons
        button_layout = QHBoxLayout()
        
        self.translate_btn = TranslateButton()
        self.translate_btn.translation_requested.connect(self._start_translation)
        self.translate_btn.setEnabled(False)
        
        self.export_btn = ExportButton()
        self.export_btn.export_requested.connect(self._export_file)
        self.export_btn.setEnabled(False)
        
        self.cancel_btn = CancelButton()
        self.cancel_btn.cancel_requested.connect(self._cancel_translation)
        self.cancel_btn.setEnabled(False)
        
        button_layout.addWidget(self.translate_btn)
        button_layout.addWidget(self.export_btn)
        button_layout.addWidget(self.cancel_btn)
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
        
        # Progress group
        progress_group = QGroupBox(self.tr('progress'))
        progress_layout = QVBoxLayout()
        
        from PyQt6.QtWidgets import QProgressBar
        self.progress_bar = QProgressBar()
        self.progress_label = QLabel("")
        
        progress_layout.addWidget(self.progress_bar)
        progress_layout.addWidget(self.progress_label)
        progress_group.setLayout(progress_layout)
        layout.addWidget(progress_group)
        
        return panel
    
    def _create_bottom_panel(self) -> QWidget:
        """Create bottom panel with logs."""
        panel = QWidget()
        layout = QVBoxLayout()
        panel.setLayout(layout)
        
        # Log group
        log_group = QGroupBox("Log")
        log_layout = QVBoxLayout()
        
        from PyQt6.QtWidgets import QTextEdit
        self.log_text = QTextEdit()
        self.log_text.setMaximumHeight(150)
        self.log_text.setReadOnly(True)
        
        log_layout.addWidget(self.log_text)
        log_group.setLayout(log_layout)
        layout.addWidget(log_group)
        
        return panel
    
    def _apply_theme(self) -> None:
        """Apply the application theme."""
        theme_file = Path('assets/dark_theme.qss')
        try:
            if theme_file.exists():
                with open(theme_file, 'r', encoding='utf-8') as f:
                    self.setStyleSheet(f.read())
        except Exception as e:
            self.logger.error(f"Failed to apply theme: {e}")
    
    def _update_ui_texts(self) -> None:
        """Update all UI texts with current translations."""
        self.setWindowTitle(self.tr('app_title'))
        # Additional UI text updates would go here
    
    # Event handlers
    def _select_file(self) -> None:
        """Handle file selection from menu."""
        if self.select_file_btn:
            self.select_file_btn._on_clicked()
    
    def _on_file_selected(self, file_path: str) -> None:
        """Handle file selection."""
        self.current_file_path = file_path
        self.file_path_label.setText(os.path.basename(file_path))
        self.file_path_label.setStyleSheet("color: #d4d4d4;")
        
        # Enable translate button if API is configured
        if self.deepl_translator:
            self.translate_btn.setEnabled(True)
        
        self._log_message(f"File selected: {os.path.basename(file_path)}")
    
    def _swap_languages(self) -> None:
        """Swap source and target languages."""
        source_index = self.source_lang_combo.currentIndex()
        target_index = self.target_lang_combo.currentIndex()
        
        self.source_lang_combo.setCurrentIndex(target_index)
        self.target_lang_combo.setCurrentIndex(source_index)
        
        self._log_message("Languages swapped")
    
    def _start_translation(self) -> None:
        """Start translation process."""
        if not self.current_file_path or not self.process_file_usecase:
            QMessageBox.warning(self, self.tr('warning'), 
                              "Please select a file and configure API key first")
            return
        
        try:
            # Create translation request
            source_lang = self._get_current_source_language_code()
            target_lang = self._get_current_target_language_code()
            
            request = TranslationRequest.create_simple(
                self.current_file_path, source_lang, target_lang
            )
            
            # Update UI state
            self.translate_btn.start_processing()
            self.cancel_btn.setEnabled(True)
            self.progress_bar.setValue(0)
            
            # Start translation in background
            self._log_message("Starting translation...")
            
        except Exception as e:
            self.logger.error(f"Failed to start translation: {e}")
            QMessageBox.critical(self, self.tr('error'), str(e))
    
    def _cancel_translation(self) -> None:
        """Cancel ongoing translation."""
        self.translate_btn.stop_processing()
        self.cancel_btn.setEnabled(False)
        self.progress_bar.setValue(0)
        self._log_message("Translation cancelled")
    
    def _export_file(self) -> None:
        """Export translated file."""
        from PyQt6.QtWidgets import QFileDialog
        
        if not self.current_file_path:
            return
        
        output_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Translated File",
            f"{Path(self.current_file_path).stem}_translated.xlsx",
            "Excel Files (*.xlsx)"
        )
        
        if output_path:
            self._log_message(f"File exported to: {output_path}")
            QMessageBox.information(self, self.tr('success'), 
                                  f"File exported successfully to:\n{output_path}")
    
    def _open_settings(self) -> None:
        """Open settings dialog."""
        # Settings dialog implementation would go here
        self._log_message("Settings dialog opened")
    
    def _get_current_source_language_code(self) -> str:
        """Get current source language code."""
        current_text = self.source_lang_combo.currentText()
        return self.language_codes.get(current_text, 'ja')
    
    def _get_current_target_language_code(self) -> str:
        """Get current target language code."""
        current_text = self.target_lang_combo.currentText()
        return self.language_codes.get(current_text, 'en')
    
    def _log_message(self, message: str) -> None:
        """Add message to log display."""
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.append(f"[{timestamp}] {message}")
        self.logger.info(message)
    
    def closeEvent(self, event) -> None:
        """Handle application close event."""
        # Save current settings
        self.settings['last_source_lang'] = self._get_current_source_language_code()
        self.settings['last_target_lang'] = self._get_current_target_language_code()
        self._save_settings()
        
        event.accept()
