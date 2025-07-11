"""
Drag and Drop Component Styles

CSS styles for drag and drop components.
"""

DRAG_DROP_STYLES = """
/* File Drop Zone Base Styles */
QFrame#fileDropZone {
    border: 2px dashed #6c757d;
    border-radius: 8px;
    background-color: #ffffff;
    padding: 20px;
    min-height: 120px;
}

QFrame#fileDropZone:hover {
    border-color: #007bff;
    background-color: #f8f9fa;
}

/* Drop Zone Active State (when file is being dragged over) */
QFrame#fileDropZone[dragActive="true"] {
    border: 2px dashed #007bff;
    border-radius: 8px;
    background-color: #e7f3ff;
    animation: pulse 1s ease-in-out infinite alternate;
}

/* Drop Zone Disabled State */
QFrame#fileDropZone[disabled="true"] {
    border: 2px dashed #cccccc;
    border-radius: 8px;
    background-color: #f8f9fa;
    color: #6c757d;
}

/* Drop Zone Success State */
QFrame#fileDropZone[state="success"] {
    border: 2px dashed #28a745;
    border-radius: 8px;
    background-color: #d1eddd;
}

/* Drop Zone Error State */
QFrame#fileDropZone[state="error"] {
    border: 2px dashed #dc3545;
    border-radius: 8px;
    background-color: #f8d7da;
}

/* Drop Zone Warning State */
QFrame#fileDropZone[state="warning"] {
    border: 2px dashed #ffc107;
    border-radius: 8px;
    background-color: #fff3cd;
}

/* Drop Zone Labels */
QLabel#dropMainLabel {
    color: #495057;
    font-size: 16px;
    font-weight: 600;
    font-family: 'Segoe UI', 'SF Pro Display', system-ui, sans-serif;
    text-align: center;
    margin: 8px 0;
}

QLabel#dropSubtitleLabel {
    color: #6c757d;
    font-size: 13px;
    font-weight: 400;
    text-align: center;
    margin: 4px 0;
}

QLabel#dropFormatsLabel {
    color: #868e96;
    font-size: 11px;
    font-weight: 400;
    text-align: center;
    margin: 4px 0;
    font-style: italic;
}

/* Drop Zone in Active Drag State Labels */
QFrame#fileDropZone[dragActive="true"] QLabel#dropMainLabel {
    color: #007bff;
    font-weight: 700;
}

QFrame#fileDropZone[dragActive="true"] QLabel#dropSubtitleLabel {
    color: #0056b3;
}

/* Drop Zone Success State Labels */
QFrame#fileDropZone[state="success"] QLabel#dropMainLabel {
    color: #155724;
    font-weight: 700;
}

QFrame#fileDropZone[state="success"] QLabel#dropSubtitleLabel {
    color: #155724;
}

/* Drop Zone Error State Labels */
QFrame#fileDropZone[state="error"] QLabel#dropMainLabel {
    color: #721c24;
    font-weight: 700;
}

QFrame#fileDropZone[state="error"] QLabel#dropSubtitleLabel {
    color: #721c24;
}

/* Drop Zone Warning State Labels */
QFrame#fileDropZone[state="warning"] QLabel#dropMainLabel {
    color: #856404;
    font-weight: 700;
}

QFrame#fileDropZone[state="warning"] QLabel#dropSubtitleLabel {
    color: #856404;
}

/* Drop Zone Icon Styling */
QLabel#dropIconLabel {
    font-size: 32px;
    text-align: center;
    margin: 8px 0;
    min-height: 40px;
    max-height: 40px;
}

/* Drop Zone Large Variant */
QFrame#fileDropZone.large {
    min-height: 160px;
    padding: 32px;
}

QFrame#fileDropZone.large QLabel#dropMainLabel {
    font-size: 18px;
}

QFrame#fileDropZone.large QLabel#dropSubtitleLabel {
    font-size: 14px;
}

QFrame#fileDropZone.large QLabel#dropIconLabel {
    font-size: 48px;
    min-height: 60px;
    max-height: 60px;
}

/* Drop Zone Small Variant */
QFrame#fileDropZone.small {
    min-height: 80px;
    padding: 12px;
}

QFrame#fileDropZone.small QLabel#dropMainLabel {
    font-size: 14px;
}

QFrame#fileDropZone.small QLabel#dropSubtitleLabel {
    font-size: 11px;
}

QFrame#fileDropZone.small QLabel#dropIconLabel {
    font-size: 24px;
    min-height: 30px;
    max-height: 30px;
}

/* Drop Zone Compact Variant */
QFrame#fileDropZone.compact {
    min-height: 60px;
    padding: 8px;
    border-radius: 4px;
}

QFrame#fileDropZone.compact QLabel#dropMainLabel {
    font-size: 12px;
    margin: 2px 0;
}

QFrame#fileDropZone.compact QLabel#dropSubtitleLabel {
    font-size: 10px;
    margin: 1px 0;
}

QFrame#fileDropZone.compact QLabel#dropFormatsLabel {
    font-size: 9px;
}

QFrame#fileDropZone.compact QLabel#dropIconLabel {
    font-size: 18px;
    min-height: 20px;
    max-height: 20px;
}

/* Drop Zone with Shadow */
QFrame#fileDropZone.shadow {
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

QFrame#fileDropZone.shadow:hover {
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

/* Drop Zone Rounded Variant */
QFrame#fileDropZone.rounded {
    border-radius: 16px;
}

/* Animation for Drag Active State */
@keyframes pulse {
    0% {
        background-color: #e7f3ff;
    }
    100% {
        background-color: #cce7ff;
    }
}

/* Drop Zone Focus State */
QFrame#fileDropZone:focus {
    outline: 2px solid #80bdff;
    outline-offset: 2px;
}

/* Drop Zone with Border Animation */
QFrame#fileDropZone.animated-border {
    border-style: dashed;
    border-width: 2px;
    animation: border-dance 2s linear infinite;
}

@keyframes border-dance {
    0% {
        border-color: #6c757d;
    }
    25% {
        border-color: #007bff;
    }
    50% {
        border-color: #28a745;
    }
    75% {
        border-color: #ffc107;
    }
    100% {
        border-color: #6c757d;
    }
}

/* Drag Overlay Styles */
QWidget#dragOverlay {
    background-color: rgba(0, 123, 255, 0.1);
    border: 2px solid #007bff;
    border-radius: 8px;
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    pointer-events: none;
}

/* File List in Drop Zone */
QListWidget#droppedFilesList {
    border: none;
    background-color: transparent;
    alternate-background-color: #f8f9fa;
    selection-background-color: #e7f3ff;
    font-size: 12px;
    padding: 4px;
}

QListWidget#droppedFilesList::item {
    padding: 4px 8px;
    border-radius: 4px;
    margin: 1px 0;
}

QListWidget#droppedFilesList::item:hover {
    background-color: #e9ecef;
}

QListWidget#droppedFilesList::item:selected {
    background-color: #007bff;
    color: white;
}

/* Dark Theme Support */
QFrame#fileDropZone[darkTheme="true"] {
    border-color: #495057;
    background-color: #343a40;
}

QFrame#fileDropZone[darkTheme="true"]:hover {
    border-color: #0d6efd;
    background-color: #495057;
}

QFrame#fileDropZone[darkTheme="true"] QLabel#dropMainLabel {
    color: #f8f9fa;
}

QFrame#fileDropZone[darkTheme="true"] QLabel#dropSubtitleLabel,
QFrame#fileDropZone[darkTheme="true"] QLabel#dropFormatsLabel {
    color: #ced4da;
}
"""
