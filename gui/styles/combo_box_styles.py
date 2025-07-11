"""
Combo Box Component Styles

CSS styles for all combo box components.
"""

COMBO_BOX_STYLES = """
/* Base Combo Box Styles */
QComboBox {
    border: 1px solid #ced4da;
    border-radius: 6px;
    padding: 6px 12px;
    background-color: #ffffff;
    color: #495057;
    font-family: 'Segoe UI', 'SF Pro Display', system-ui, sans-serif;
    font-size: 13px;
    min-height: 20px;
    selection-background-color: #007bff;
    selection-color: white;
}

QComboBox:hover {
    border-color: #80bdff;
    background-color: #f8f9fa;
}

QComboBox:focus {
    border-color: #80bdff;
    outline: none;
    box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
}

QComboBox:disabled {
    background-color: #e9ecef;
    color: #6c757d;
    border-color: #dee2e6;
}

/* Drop-down Arrow */
QComboBox::drop-down {
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 20px;
    border-left-width: 1px;
    border-left-color: #ced4da;
    border-left-style: solid;
    border-top-right-radius: 6px;
    border-bottom-right-radius: 6px;
    background-color: #f8f9fa;
}

QComboBox::drop-down:hover {
    background-color: #e9ecef;
}

QComboBox::down-arrow {
    image: url(assets/icons/dropdown_arrow.png);
    width: 12px;
    height: 12px;
}

QComboBox::down-arrow:hover {
    image: url(assets/icons/dropdown_arrow_hover.png);
}

QComboBox::down-arrow:on {
    image: url(assets/icons/dropdown_arrow_up.png);
}

QComboBox::down-arrow:on:hover {
    image: url(assets/icons/dropdown_arrow_up_hover.png);
}

/* Drop-down List */
QComboBox QAbstractItemView {
    border: 1px solid #ced4da;
    border-radius: 6px;
    background-color: #ffffff;
    selection-background-color: #007bff;
    selection-color: white;
    outline: none;
    padding: 4px;
}

QComboBox QAbstractItemView::item {
    padding: 6px 12px;
    border-radius: 4px;
    min-height: 16px;
}

QComboBox QAbstractItemView::item:hover {
    background-color: #f8f9fa;
    color: #495057;
}

QComboBox QAbstractItemView::item:selected {
    background-color: #007bff;
    color: white;
}

/* Language Combo Box Specific Styles */
QComboBox#sourceLanguageComboBox,
QComboBox#targetLanguageComboBox {
    min-width: 150px;
}

QComboBox#sourceLanguageComboBox QAbstractItemView::item,
QComboBox#targetLanguageComboBox QAbstractItemView::item {
    padding: 8px 12px;
}

/* Format Combo Box Specific Styles */
QComboBox#formatComboBox {
    min-width: 200px;
}

QComboBox#formatComboBox QAbstractItemView::item {
    padding: 6px 12px;
    font-size: 12px;
}

/* Editable Combo Box Styles */
QComboBox:editable {
    background-color: #ffffff;
}

QComboBox:editable:hover {
    background-color: #ffffff;
}

QComboBox:editable:focus {
    background-color: #ffffff;
}

QComboBox QLineEdit {
    border: none;
    background-color: transparent;
    color: #495057;
    padding: 0;
    margin: 0;
}

QComboBox QLineEdit:focus {
    outline: none;
}

/* Large Combo Box Variant */
QComboBox.large {
    font-size: 15px;
    padding: 10px 16px;
    min-height: 24px;
}

QComboBox.large::drop-down {
    width: 24px;
}

QComboBox.large QAbstractItemView::item {
    padding: 8px 16px;
    min-height: 20px;
}

/* Small Combo Box Variant */
QComboBox.small {
    font-size: 11px;
    padding: 4px 8px;
    min-height: 16px;
}

QComboBox.small::drop-down {
    width: 16px;
}

QComboBox.small QAbstractItemView::item {
    padding: 4px 8px;
    min-height: 12px;
}

/* Error State */
QComboBox.error {
    border-color: #dc3545;
    background-color: #f8d7da;
}

QComboBox.error:focus {
    border-color: #dc3545;
    box-shadow: 0 0 0 0.2rem rgba(220, 53, 69, 0.25);
}

/* Success State */
QComboBox.success {
    border-color: #28a745;
    background-color: #d1eddd;
}

QComboBox.success:focus {
    border-color: #28a745;
    box-shadow: 0 0 0 0.2rem rgba(40, 167, 69, 0.25);
}

/* Warning State */
QComboBox.warning {
    border-color: #ffc107;
    background-color: #fff3cd;
}

QComboBox.warning:focus {
    border-color: #ffc107;
    box-shadow: 0 0 0 0.2rem rgba(255, 193, 7, 0.25);
}

/* Scrollbar in Dropdown */
QComboBox QAbstractItemView QScrollBar:vertical {
    background-color: #f8f9fa;
    width: 12px;
    border-radius: 6px;
    margin: 0;
}

QComboBox QAbstractItemView QScrollBar::handle:vertical {
    background-color: #ced4da;
    border-radius: 6px;
    min-height: 20px;
    margin: 2px;
}

QComboBox QAbstractItemView QScrollBar::handle:vertical:hover {
    background-color: #adb5bd;
}

QComboBox QAbstractItemView QScrollBar::add-line:vertical,
QComboBox QAbstractItemView QScrollBar::sub-line:vertical {
    height: 0;
    width: 0;
}

QComboBox QAbstractItemView QScrollBar::add-page:vertical,
QComboBox QAbstractItemView QScrollBar::sub-page:vertical {
    background: none;
}
"""
