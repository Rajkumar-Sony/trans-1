#!/usr/bin/env python3
"""
Excel Translator App - Main Entry Point

A modern desktop application for translating Excel files using DeepL API
while preserving formatting, styles, and formulas.

Author: Excel Translator Team
Version: 1.0.0
"""

import sys
import os
import logging
from pathlib import Path

# Add the current directory to the Python path
sys.path.insert(0, str(Path(__file__).parent))

from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import Qt, QLocale, QTranslator
from PyQt6.QtGui import QIcon, QFont

from ui.main_window import ExcelTranslatorApp


def setup_logging():
    """Setup application logging."""
    log_dir = Path(__file__).parent / "logs"
    log_dir.mkdir(exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_dir / "app.log", encoding='utf-8'),
            logging.StreamHandler()
        ]
    )


def setup_application():
    """Setup the QApplication with proper configuration."""
    # Enable high DPI support (not needed in Qt6 as it's enabled by default)
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("Excel Translator")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("Excel Translator Team")
    app.setOrganizationDomain("exceltranslator.com")
    
    # Set application icon if available
    icon_path = Path(__file__).parent / "assets" / "icon.png"
    if icon_path.exists():
        app.setWindowIcon(QIcon(str(icon_path)))
    
    # Set default font
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    return app


def check_dependencies():
    """Check if all required dependencies are installed."""
    required_modules = [
        'PyQt6',
        'openpyxl',
        'deepl',
        'requests'
    ]
    
    missing_modules = []
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            missing_modules.append(module)
    
    if missing_modules:
        error_msg = (
            "Missing required dependencies:\n" + 
            "\n".join(f"- {module}" for module in missing_modules) +
            "\n\nPlease install them using:\n" +
            f"pip install {' '.join(missing_modules)}"
        )
        
        # Try to show GUI error if possible
        try:
            app = QApplication(sys.argv)
            QMessageBox.critical(None, "Missing Dependencies", error_msg)
        except:
            print(error_msg)
        
        return False
    
    return True


def main():
    """Main application entry point."""
    try:
        # Setup logging
        setup_logging()
        logger = logging.getLogger(__name__)
        
        logger.info("Starting Excel Translator App...")
        
        # Check dependencies
        if not check_dependencies():
            sys.exit(1)
        
        # Setup application
        app = setup_application()
        
        # Create and show main window
        window = ExcelTranslatorApp()
        window.show()
        
        # Center the window on screen
        screen = app.primaryScreen()
        screen_geometry = screen.geometry()
        window_geometry = window.geometry()
        x = (screen_geometry.width() - window_geometry.width()) // 2
        y = (screen_geometry.height() - window_geometry.height()) // 2
        window.move(x, y)
        
        logger.info("Application started successfully")
        
        # Run the application
        exit_code = app.exec()
        
        logger.info(f"Application exited with code: {exit_code}")
        return exit_code
        
    except Exception as e:
        error_msg = f"Failed to start application: {str(e)}"
        
        # Try to show GUI error if possible
        try:
            app = QApplication(sys.argv)
            QMessageBox.critical(None, "Application Error", error_msg)
        except:
            print(error_msg)
        
        if 'logger' in locals():
            logger.error(error_msg, exc_info=True)
        
        return 1


if __name__ == "__main__":
    sys.exit(main())
