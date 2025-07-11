"""
Main Window Component Styles

CSS styles for main window layout and containers.
"""

MAIN_WINDOW_STYLES = """
/* Main Window Styles */
QMainWindow {
    background-color: #f8f9fa;
    color: #495057;
    font-family: 'Segoe UI', 'SF Pro Display', system-ui, sans-serif;
}

QMainWindow::separator {
    background-color: #dee2e6;
    width: 1px;
    height: 1px;
}

/* Central Widget */
QWidget#centralWidget {
    background-color: #ffffff;
    border: none;
}

/* Main Container */
QWidget#mainContainer {
    background-color: #ffffff;
    border: 1px solid #e9ecef;
    border-radius: 8px;
    margin: 8px;
    padding: 0;
}

/* Header Section */
QWidget#headerSection {
    background-color: #ffffff;
    border-bottom: 1px solid #e9ecef;
    padding: 16px 20px;
    min-height: 60px;
}

QLabel#titleLabel {
    font-size: 24px;
    font-weight: 700;
    color: #212529;
    margin: 0;
    padding: 0;
}

QLabel#subtitleLabel {
    font-size: 14px;
    font-weight: 400;
    color: #6c757d;
    margin: 4px 0 0 0;
    padding: 0;
}

/* Content Area */
QWidget#contentArea {
    background-color: #ffffff;
    padding: 20px;
}

/* File Selection Panel */
QWidget#fileSelectionPanel {
    background-color: #f8f9fa;
    border: 1px solid #e9ecef;
    border-radius: 8px;
    padding: 16px;
    margin: 8px 0;
}

QLabel#filePanelTitle {
    font-size: 16px;
    font-weight: 600;
    color: #495057;
    margin-bottom: 12px;
}

/* Language Selection Panel */
QWidget#languageSelectionPanel {
    background-color: #ffffff;
    border: 1px solid #e9ecef;
    border-radius: 8px;
    padding: 16px;
    margin: 8px 0;
}

QLabel#languagePanelTitle {
    font-size: 16px;
    font-weight: 600;
    color: #495057;
    margin-bottom: 12px;
}

/* Options Panel */
QWidget#optionsPanel {
    background-color: #ffffff;
    border: 1px solid #e9ecef;
    border-radius: 8px;
    padding: 16px;
    margin: 8px 0;
}

QLabel#optionsPanelTitle {
    font-size: 16px;
    font-weight: 600;
    color: #495057;
    margin-bottom: 12px;
}

/* Progress Panel */
QWidget#progressPanel {
    background-color: #f8f9fa;
    border: 1px solid #e9ecef;
    border-radius: 8px;
    padding: 16px;
    margin: 8px 0;
}

/* Action Panel */
QWidget#actionPanel {
    background-color: #ffffff;
    border-top: 1px solid #e9ecef;
    padding: 16px 20px;
    min-height: 60px;
}

/* Language Selection Layout */
QWidget#languageSelectionLayout {
    background-color: transparent;
}

QLabel#sourceLanguageLabel,
QLabel#targetLanguageLabel {
    font-size: 13px;
    font-weight: 500;
    color: #495057;
    margin-bottom: 4px;
}

QWidget#languageComboContainer {
    margin: 8px 0;
}

/* Swap Button Container */
QWidget#swapButtonContainer {
    background-color: transparent;
    padding: 0;
    margin: 0 8px;
    min-width: 40px;
    max-width: 40px;
}

/* File Info Display */
QWidget#fileInfoWidget {
    background-color: #e9ecef;
    border: 1px solid #ced4da;
    border-radius: 6px;
    padding: 12px;
    margin: 8px 0;
}

QLabel#fileNameLabel {
    font-size: 14px;
    font-weight: 600;
    color: #495057;
    margin-bottom: 4px;
}

QLabel#fileSizeLabel,
QLabel#fileTypeLabel {
    font-size: 12px;
    font-weight: 400;
    color: #6c757d;
    margin: 2px 0;
}

/* Status Bar */
QStatusBar {
    background-color: #f8f9fa;
    border-top: 1px solid #dee2e6;
    color: #6c757d;
    font-size: 12px;
    padding: 4px 8px;
}

QStatusBar::item {
    border: none;
}

QLabel#statusMessage {
    color: #6c757d;
    font-size: 12px;
    padding: 2px 4px;
}

/* Toolbar */
QToolBar {
    background-color: #ffffff;
    border: none;
    border-bottom: 1px solid #e9ecef;
    padding: 8px;
    spacing: 4px;
}

QToolBar::separator {
    background-color: #dee2e6;
    width: 1px;
    margin: 4px 8px;
}

/* Menu Bar */
QMenuBar {
    background-color: #ffffff;
    border-bottom: 1px solid #e9ecef;
    color: #495057;
    font-size: 13px;
    padding: 4px;
}

QMenuBar::item {
    background-color: transparent;
    padding: 6px 12px;
    border-radius: 4px;
}

QMenuBar::item:selected {
    background-color: #e9ecef;
}

QMenuBar::item:pressed {
    background-color: #007bff;
    color: white;
}

QMenu {
    background-color: #ffffff;
    border: 1px solid #ced4da;
    border-radius: 6px;
    padding: 4px;
    color: #495057;
}

QMenu::item {
    padding: 6px 12px;
    border-radius: 4px;
    margin: 1px;
}

QMenu::item:selected {
    background-color: #007bff;
    color: white;
}

QMenu::separator {
    height: 1px;
    background-color: #dee2e6;
    margin: 4px 8px;
}

/* Scroll Areas */
QScrollArea {
    border: none;
    background-color: transparent;
}

QScrollArea > QWidget > QWidget {
    background-color: transparent;
}

QScrollBar:vertical {
    background-color: #f8f9fa;
    width: 12px;
    border-radius: 6px;
    margin: 0;
}

QScrollBar::handle:vertical {
    background-color: #ced4da;
    border-radius: 6px;
    min-height: 20px;
    margin: 2px;
}

QScrollBar::handle:vertical:hover {
    background-color: #adb5bd;
}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {
    height: 0;
    width: 0;
}

QScrollBar::add-page:vertical,
QScrollBar::sub-page:vertical {
    background: none;
}

QScrollBar:horizontal {
    background-color: #f8f9fa;
    height: 12px;
    border-radius: 6px;
    margin: 0;
}

QScrollBar::handle:horizontal {
    background-color: #ced4da;
    border-radius: 6px;
    min-width: 20px;
    margin: 2px;
}

QScrollBar::handle:horizontal:hover {
    background-color: #adb5bd;
}

QScrollBar::add-line:horizontal,
QScrollBar::sub-line:horizontal {
    height: 0;
    width: 0;
}

QScrollBar::add-page:horizontal,
QScrollBar::sub-page:horizontal {
    background: none;
}

/* Splitter */
QSplitter {
    background-color: transparent;
}

QSplitter::handle {
    background-color: #dee2e6;
    margin: 2px;
}

QSplitter::handle:horizontal {
    width: 1px;
}

QSplitter::handle:vertical {
    height: 1px;
}

QSplitter::handle:hover {
    background-color: #adb5bd;
}

/* Tab Widget */
QTabWidget {
    background-color: #ffffff;
    border: 1px solid #dee2e6;
    border-radius: 6px;
}

QTabWidget::pane {
    border: none;
    background-color: #ffffff;
    border-radius: 0 0 6px 6px;
}

QTabBar {
    background-color: transparent;
}

QTabBar::tab {
    background-color: #f8f9fa;
    border: 1px solid #dee2e6;
    border-bottom: none;
    border-radius: 6px 6px 0 0;
    padding: 8px 16px;
    margin-right: 2px;
    color: #6c757d;
    font-size: 13px;
}

QTabBar::tab:selected {
    background-color: #ffffff;
    color: #495057;
    font-weight: 500;
}

QTabBar::tab:hover {
    background-color: #e9ecef;
    color: #495057;
}

/* Panel Shadows */
QWidget#fileSelectionPanel,
QWidget#languageSelectionPanel,
QWidget#optionsPanel,
QWidget#progressPanel {
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.12), 0 1px 2px rgba(0, 0, 0, 0.24);
}

/* Responsive Layout */
@media (max-width: 768px) {
    QWidget#mainContainer {
        margin: 4px;
    }
    
    QWidget#headerSection,
    QWidget#actionPanel {
        padding: 12px 16px;
    }
    
    QWidget#contentArea {
        padding: 16px;
    }
    
    QWidget#fileSelectionPanel,
    QWidget#languageSelectionPanel,
    QWidget#optionsPanel,
    QWidget#progressPanel {
        padding: 12px;
        margin: 4px 0;
    }
}

/* Dark Theme Support */
QMainWindow[darkTheme="true"] {
    background-color: #212529;
    color: #f8f9fa;
}

QWidget[darkTheme="true"]#centralWidget,
QWidget[darkTheme="true"]#mainContainer,
QWidget[darkTheme="true"]#contentArea,
QWidget[darkTheme="true"]#languageSelectionPanel,
QWidget[darkTheme="true"]#optionsPanel {
    background-color: #343a40;
    border-color: #495057;
}

QWidget[darkTheme="true"]#fileSelectionPanel,
QWidget[darkTheme="true"]#progressPanel {
    background-color: #495057;
    border-color: #6c757d;
}

QLabel[darkTheme="true"] {
    color: #f8f9fa;
}

QStatusBar[darkTheme="true"] {
    background-color: #212529;
    border-color: #495057;
    color: #ced4da;
}
"""
