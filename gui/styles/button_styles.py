"""
Button Component Styles

CSS styles for all button components.
"""

BUTTON_STYLES = """
/* Base Button Styles */
QPushButton {
    border: none;
    border-radius: 6px;
    font-family: 'Segoe UI', 'SF Pro Display', system-ui, sans-serif;
    font-size: 13px;
    font-weight: 500;
    padding: 8px 16px;
    min-height: 20px;
    background-color: #f8f9fa;
    color: #495057;
    outline: none;
}

QPushButton:hover {
    background-color: #e9ecef;
    transform: translateY(-1px);
}

QPushButton:pressed {
    background-color: #dee2e6;
    transform: translateY(0px);
}

QPushButton:disabled {
    background-color: #e9ecef;
    color: #6c757d;
    border: 1px solid #dee2e6;
}

/* Primary Button Styles */
QPushButton#translateButton,
QPushButton#exportButton {
    background-color: #007bff;
    color: white;
    font-weight: 600;
}

QPushButton#translateButton:hover,
QPushButton#exportButton:hover {
    background-color: #0056b3;
}

QPushButton#translateButton:pressed,
QPushButton#exportButton:pressed {
    background-color: #004085;
}

QPushButton#translateButton:disabled,
QPushButton#exportButton:disabled {
    background-color: #6c757d;
    color: #ffffff;
}

/* Success Button Styles */
QPushButton#selectFileButton {
    background-color: #28a745;
    color: white;
}

QPushButton#selectFileButton:hover {
    background-color: #1e7e34;
}

QPushButton#selectFileButton:pressed {
    background-color: #155724;
}

/* Danger Button Styles */
QPushButton#cancelButton {
    background-color: #dc3545;
    color: white;
}

QPushButton#cancelButton:hover {
    background-color: #c82333;
}

QPushButton#cancelButton:pressed {
    background-color: #bd2130;
}

/* Secondary Button Styles */
QPushButton#swapButton {
    background-color: #6c757d;
    color: white;
    border-radius: 50%;
    min-width: 32px;
    max-width: 32px;
    min-height: 32px;
    max-height: 32px;
    padding: 4px;
}

QPushButton#swapButton:hover {
    background-color: #545b62;
}

QPushButton#swapButton:pressed {
    background-color: #495057;
}

/* Processing Animation */
QPushButton.processing {
    background-color: #ffc107;
    color: #212529;
}

QPushButton.processing:disabled {
    background-color: #ffc107;
    color: #212529;
}

/* Icon Buttons */
QPushButton.icon-button {
    border-radius: 4px;
    padding: 6px;
    min-width: 24px;
    max-width: 24px;
    min-height: 24px;
    max-height: 24px;
}

/* Flat Button Variant */
QPushButton.flat {
    background-color: transparent;
    border: 1px solid #dee2e6;
}

QPushButton.flat:hover {
    background-color: #f8f9fa;
    border-color: #adb5bd;
}

QPushButton.flat:pressed {
    background-color: #e9ecef;
    border-color: #6c757d;
}

/* Large Button Variant */
QPushButton.large {
    font-size: 15px;
    padding: 12px 24px;
    min-height: 24px;
}

/* Small Button Variant */
QPushButton.small {
    font-size: 11px;
    padding: 4px 12px;
    min-height: 16px;
}

/* Button Focus States */
QPushButton:focus {
    outline: 2px solid #80bdff;
    outline-offset: 2px;
}

/* Button Group Styles */
.button-group QPushButton {
    border-radius: 0;
    border-right: 1px solid #dee2e6;
}

.button-group QPushButton:first-child {
    border-top-left-radius: 6px;
    border-bottom-left-radius: 6px;
}

.button-group QPushButton:last-child {
    border-top-right-radius: 6px;
    border-bottom-right-radius: 6px;
    border-right: none;
}

/* Toolbar Button Styles */
QToolButton {
    border: none;
    border-radius: 4px;
    padding: 4px;
    background-color: transparent;
}

QToolButton:hover {
    background-color: #e9ecef;
}

QToolButton:pressed {
    background-color: #dee2e6;
}

QToolButton:checked {
    background-color: #007bff;
    color: white;
}
"""
