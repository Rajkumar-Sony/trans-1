"""
Check Box Component Styles

CSS styles for all check box components.
"""

CHECK_BOX_STYLES = """
/* Base Check Box Styles */
QCheckBox {
    font-family: 'Segoe UI', 'SF Pro Display', system-ui, sans-serif;
    font-size: 13px;
    color: #495057;
    spacing: 8px;
    outline: none;
}

QCheckBox::indicator {
    width: 16px;
    height: 16px;
    border: 2px solid #ced4da;
    border-radius: 3px;
    background-color: #ffffff;
}

QCheckBox::indicator:hover {
    border-color: #80bdff;
    background-color: #f8f9fa;
}

QCheckBox::indicator:checked {
    border-color: #007bff;
    background-color: #007bff;
    image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTAiIGhlaWdodD0iOCIgdmlld0JveD0iMCAwIDEwIDgiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxwYXRoIGQ9Ik04LjUgMUwzLjUgNkwxIDMuNSIgc3Ryb2tlPSJ3aGl0ZSIgc3Ryb2tlLXdpZHRoPSIxLjUiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIvPgo8L3N2Zz4K);
}

QCheckBox::indicator:checked:hover {
    border-color: #0056b3;
    background-color: #0056b3;
}

QCheckBox::indicator:disabled {
    border-color: #dee2e6;
    background-color: #e9ecef;
}

QCheckBox::indicator:checked:disabled {
    border-color: #6c757d;
    background-color: #6c757d;
}

QCheckBox:disabled {
    color: #6c757d;
}

/* Focus State */
QCheckBox:focus::indicator {
    outline: 2px solid #80bdff;
    outline-offset: 2px;
}

/* Options Check Box Specific Styles */
QCheckBox[objectName^="option_"] {
    padding: 4px 0;
    margin: 2px 0;
}

QCheckBox[objectName^="option_"]::indicator {
    width: 18px;
    height: 18px;
}

/* Large Check Box Variant */
QCheckBox.large {
    font-size: 15px;
    spacing: 10px;
}

QCheckBox.large::indicator {
    width: 20px;
    height: 20px;
    border-radius: 4px;
}

/* Small Check Box Variant */
QCheckBox.small {
    font-size: 11px;
    spacing: 6px;
}

QCheckBox.small::indicator {
    width: 14px;
    height: 14px;
    border-radius: 2px;
}

/* Toggle Switch Style Check Box */
QCheckBox.toggle {
    spacing: 12px;
}

QCheckBox.toggle::indicator {
    width: 40px;
    height: 20px;
    border-radius: 10px;
    border: 2px solid #ced4da;
    background-color: #e9ecef;
}

QCheckBox.toggle::indicator:hover {
    border-color: #80bdff;
}

QCheckBox.toggle::indicator:checked {
    border-color: #007bff;
    background-color: #007bff;
    image: none;
}

QCheckBox.toggle::indicator:checked:hover {
    border-color: #0056b3;
    background-color: #0056b3;
}

/* Round Check Box */
QCheckBox.round::indicator {
    border-radius: 8px;
}

QCheckBox.round.large::indicator {
    border-radius: 10px;
}

QCheckBox.round.small::indicator {
    border-radius: 7px;
}

/* Group Box for Check Box Groups */
QGroupBox {
    font-size: 14px;
    font-weight: 600;
    color: #495057;
    border: 1px solid #dee2e6;
    border-radius: 6px;
    margin-top: 8px;
    padding-top: 16px;
    background-color: #ffffff;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 8px;
    top: -8px;
    padding: 0 4px;
    background-color: #ffffff;
}

QGroupBox:hover {
    border-color: #80bdff;
}

QGroupBox:focus {
    border-color: #007bff;
}

/* Translation Options Group */
QGroupBox#translationOptionsGroup {
    padding: 16px;
    margin: 8px 0;
}

QGroupBox#translationOptionsGroup::title {
    color: #007bff;
    font-weight: 700;
}

/* Advanced Options Group */
QGroupBox#advancedOptionsGroup {
    padding: 12px;
    margin: 4px 0;
}

QGroupBox#advancedOptionsGroup::title {
    color: #6c757d;
    font-weight: 600;
    font-size: 12px;
}

/* Checkable Group Box */
QGroupBox::indicator {
    width: 16px;
    height: 16px;
    border: 2px solid #ced4da;
    border-radius: 3px;
    background-color: #ffffff;
    margin-right: 8px;
}

QGroupBox::indicator:hover {
    border-color: #80bdff;
}

QGroupBox::indicator:checked {
    border-color: #007bff;
    background-color: #007bff;
    image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTAiIGhlaWdodD0iOCIgdmlld0JveD0iMCAwIDEwIDgiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxwYXRoIGQ9Ik04LjUgMUwzLjUgNkwxIDMuNSIgc3Ryb2tlPSJ3aGl0ZSIgc3Ryb2tlLXdpZHRoPSIxLjUiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIvPgo8L3N2Zz4K);
}

/* Error State Check Box */
QCheckBox.error {
    color: #dc3545;
}

QCheckBox.error::indicator {
    border-color: #dc3545;
}

QCheckBox.error::indicator:checked {
    background-color: #dc3545;
    border-color: #dc3545;
}

/* Success State Check Box */
QCheckBox.success {
    color: #28a745;
}

QCheckBox.success::indicator {
    border-color: #28a745;
}

QCheckBox.success::indicator:checked {
    background-color: #28a745;
    border-color: #28a745;
}

/* Warning State Check Box */
QCheckBox.warning {
    color: #ffc107;
}

QCheckBox.warning::indicator {
    border-color: #ffc107;
}

QCheckBox.warning::indicator:checked {
    background-color: #ffc107;
    border-color: #ffc107;
}

/* Indeterminate State */
QCheckBox::indicator:indeterminate {
    border-color: #6c757d;
    background-color: #6c757d;
    image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iOCIgaGVpZ2h0PSIyIiB2aWV3Qm94PSIwIDAgOCAyIiBmaWxsPSJub25lIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPgo8cGF0aCBkPSJNMSAxSDciIHN0cm9rZT0id2hpdGUiIHN0cm9rZS13aWR0aD0iMS41IiBzdHJva2UtbGluZWNhcD0icm91bmQiLz4KPC9zdmc+Cg==);
}

/* Flat Check Box Variant */
QCheckBox.flat::indicator {
    border: none;
    background-color: transparent;
}

QCheckBox.flat::indicator:checked {
    background-color: #007bff;
    border-radius: 3px;
}

QCheckBox.flat::indicator:hover {
    background-color: #f8f9fa;
    border-radius: 3px;
}

/* Animated Check Box */
QCheckBox.animated::indicator {
    transition: all 0.2s ease-in-out;
}

QCheckBox.animated::indicator:checked {
    transform: scale(1.1);
}

/* Dark Theme Support */
QCheckBox[darkTheme="true"] {
    color: #f8f9fa;
}

QCheckBox[darkTheme="true"]::indicator {
    border-color: #495057;
    background-color: #343a40;
}

QCheckBox[darkTheme="true"]::indicator:hover {
    border-color: #0d6efd;
    background-color: #495057;
}

QCheckBox[darkTheme="true"]::indicator:checked {
    border-color: #0d6efd;
    background-color: #0d6efd;
}

QGroupBox[darkTheme="true"] {
    color: #f8f9fa;
    border-color: #495057;
    background-color: #343a40;
}

QGroupBox[darkTheme="true"]::title {
    background-color: #343a40;
}

/* Checkbox List Styles */
QWidget#checkboxContainer {
    background-color: #ffffff;
    border: 1px solid #dee2e6;
    border-radius: 6px;
    padding: 8px;
}

QWidget#checkboxContainer QCheckBox {
    margin: 4px 0;
    padding: 2px 0;
}

/* Responsive Checkbox Layout */
@media (max-width: 768px) {
    QCheckBox {
        font-size: 14px;
        spacing: 10px;
    }
    
    QCheckBox::indicator {
        width: 18px;
        height: 18px;
    }
}
"""
