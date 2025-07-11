"""
Progress Bar Component Styles

CSS styles for all progress bar components.
"""

PROGRESS_BAR_STYLES = """
/* Base Progress Bar Styles */
QProgressBar {
    border: 1px solid #ced4da;
    border-radius: 6px;
    background-color: #e9ecef;
    font-family: 'Segoe UI', 'SF Pro Display', system-ui, sans-serif;
    font-size: 12px;
    font-weight: 500;
    text-align: center;
    height: 20px;
    color: #495057;
}

QProgressBar::chunk {
    background-color: #007bff;
    border-radius: 5px;
    margin: 1px;
}

/* Translation Progress Bar */
QProgressBar#translationProgressBar {
    border: 1px solid #007bff;
    background-color: #f8f9fa;
    height: 24px;
    font-size: 13px;
}

QProgressBar#translationProgressBar::chunk {
    background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                               stop: 0 #007bff, stop: 1 #0056b3);
    border-radius: 5px;
}

/* File Progress Bar */
QProgressBar#fileProgressBar {
    border: 1px solid #28a745;
    background-color: #f8f9fa;
    height: 20px;
    font-size: 11px;
}

QProgressBar#fileProgressBar::chunk {
    background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                               stop: 0 #28a745, stop: 1 #1e7e34);
    border-radius: 5px;
}

/* Indeterminate Progress Bar */
QProgressBar:indeterminate {
    background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                               stop: 0 #f8f9fa, stop: 0.5 #e9ecef, stop: 1 #f8f9fa);
}

QProgressBar:indeterminate::chunk {
    background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                               stop: 0 transparent, stop: 0.5 #007bff, stop: 1 transparent);
    width: 30px;
    margin: 1px;
    border-radius: 5px;
}

/* Success State Progress Bar */
QProgressBar.success {
    border-color: #28a745;
    background-color: #d1eddd;
}

QProgressBar.success::chunk {
    background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                               stop: 0 #28a745, stop: 1 #155724);
}

/* Error State Progress Bar */
QProgressBar.error {
    border-color: #dc3545;
    background-color: #f8d7da;
}

QProgressBar.error::chunk {
    background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                               stop: 0 #dc3545, stop: 1 #bd2130);
}

/* Warning State Progress Bar */
QProgressBar.warning {
    border-color: #ffc107;
    background-color: #fff3cd;
}

QProgressBar.warning::chunk {
    background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                               stop: 0 #ffc107, stop: 1 #e0a800);
}

/* Large Progress Bar Variant */
QProgressBar.large {
    height: 32px;
    font-size: 14px;
    font-weight: 600;
}

/* Small Progress Bar Variant */
QProgressBar.small {
    height: 16px;
    font-size: 10px;
}

QProgressBar.small::chunk {
    margin: 1px;
    border-radius: 3px;
}

/* Thin Progress Bar */
QProgressBar.thin {
    height: 8px;
    border-radius: 4px;
}

QProgressBar.thin::chunk {
    border-radius: 3px;
    margin: 1px;
}

/* Rounded Progress Bar */
QProgressBar.rounded {
    border-radius: 10px;
}

QProgressBar.rounded::chunk {
    border-radius: 9px;
}

/* Animated Progress Bar */
QProgressBar.animated::chunk {
    background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                               stop: 0 #007bff, stop: 0.5 #0056b3, stop: 1 #007bff);
}

/* Progress Bar with Stripes */
QProgressBar.striped::chunk {
    background: repeating-linear-gradient(
        45deg,
        #007bff,
        #007bff 10px,
        #0056b3 10px,
        #0056b3 20px
    );
}

/* Progress Container Styles */
QWidget#progressContainer {
    background-color: #ffffff;
    border: 1px solid #dee2e6;
    border-radius: 8px;
    padding: 16px;
    margin: 8px 0;
}

/* Progress Labels */
QLabel#statusLabel {
    color: #495057;
    font-size: 13px;
    font-weight: 500;
    margin-bottom: 4px;
}

QLabel#timeLabel,
QLabel#rateLabel {
    color: #6c757d;
    font-size: 11px;
    margin-top: 4px;
}

QLabel#fileStatusLabel {
    color: #495057;
    font-size: 12px;
    font-weight: 500;
    text-align: center;
    margin-bottom: 8px;
}

/* Hover Effects */
QProgressBar:hover {
    border-color: #80bdff;
}

QProgressBar.success:hover {
    border-color: #34ce57;
}

QProgressBar.error:hover {
    border-color: #e4606d;
}

QProgressBar.warning:hover {
    border-color: #ffcd39;
}

/* Focus Effects */
QProgressBar:focus {
    outline: 2px solid #80bdff;
    outline-offset: 2px;
}

/* Disabled State */
QProgressBar:disabled {
    border-color: #dee2e6;
    background-color: #f8f9fa;
    color: #6c757d;
}

QProgressBar:disabled::chunk {
    background-color: #ced4da;
}

/* Dark Theme Support */
QProgressBar[darkTheme="true"] {
    border-color: #495057;
    background-color: #343a40;
    color: #f8f9fa;
}

QProgressBar[darkTheme="true"]::chunk {
    background-color: #0d6efd;
}

/* Progress Bar Animation Keyframes */
@keyframes progress-bar-stripes {
    0% {
        background-position: 0 0;
    }
    100% {
        background-position: 40px 0;
    }
}

QProgressBar.animated-stripes::chunk {
    animation: progress-bar-stripes 1s linear infinite;
}
"""
