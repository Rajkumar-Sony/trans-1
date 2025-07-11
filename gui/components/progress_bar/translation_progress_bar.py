"""
Translation Progress Bar Component

Modern QProgressBar implementation for translation progress tracking.
"""

from PyQt6.QtWidgets import QProgressBar, QWidget, QVBoxLayout, QLabel, QHBoxLayout
from PyQt6.QtCore import pyqtSignal, QTimer, Qt, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QPalette
from typing import Optional


class TranslationProgressBar(QProgressBar):
    """Custom progress bar for translation operations with modern styling."""
    
    # Signals
    progress_updated = pyqtSignal(int)  # Current progress value
    operation_completed = pyqtSignal()  # Operation finished
    operation_cancelled = pyqtSignal()  # Operation cancelled
    
    def __init__(self, parent=None):
        """Initialize the translation progress bar."""
        super().__init__(parent)
        self._setup_ui()
        self._setup_animation()
        self._current_operation = ""
        self._is_indeterminate = False
    
    def _setup_ui(self):
        """Set up the UI components."""
        self.setObjectName("translationProgressBar")
        self.setMinimum(0)
        self.setMaximum(100)
        self.setValue(0)
        self.setTextVisible(True)
        
        # Set initial state
        self.setVisible(False)
        
        # Format string for progress text
        self.setFormat("%p% - %v/%m items")
    
    def _setup_animation(self):
        """Set up progress animation."""
        self._pulse_timer = QTimer()
        self._pulse_timer.timeout.connect(self._pulse_animation)
        self._pulse_direction = 1
        self._pulse_value = 0
        
        # Smooth progress animation
        self._animation = QPropertyAnimation(self, b"value")
        self._animation.setDuration(300)
        self._animation.setEasingCurve(QEasingCurve.Type.OutCubic)
    
    def start_operation(self, operation_name: str, total_items: int = 100, indeterminate: bool = False):
        """
        Start a new operation.
        
        Args:
            operation_name: Name of the operation
            total_items: Total number of items to process
            indeterminate: Whether progress is indeterminate
        """
        self._current_operation = operation_name
        self._is_indeterminate = indeterminate
        
        if indeterminate:
            self.setMinimum(0)
            self.setMaximum(0)
            self.setFormat(f"{operation_name}...")
            self._start_pulse_animation()
        else:
            self.setMinimum(0)
            self.setMaximum(total_items)
            self.setValue(0)
            self.setFormat(f"{operation_name} - %p% (%v/%m)")
            self._stop_pulse_animation()
        
        self.setVisible(True)
    
    def update_progress(self, current: int, message: str = ""):
        """
        Update progress value.
        
        Args:
            current: Current progress value
            message: Optional status message
        """
        if self._is_indeterminate:
            return
            
        # Animate to new value
        self._animation.setStartValue(self.value())
        self._animation.setEndValue(current)
        self._animation.start()
        
        # Update format with message
        if message:
            self.setFormat(f"{self._current_operation} - {message} (%p%)")
        else:
            self.setFormat(f"{self._current_operation} - %p% (%v/%m)")
        
        self.progress_updated.emit(current)
        
        # Check if completed
        if current >= self.maximum():
            QTimer.singleShot(500, self._complete_operation)
    
    def set_error_state(self, error_message: str):
        """
        Set progress bar to error state.
        
        Args:
            error_message: Error message to display
        """
        self._stop_pulse_animation()
        self.setFormat(f"Error: {error_message}")
        self.setStyleSheet("""
            QProgressBar::chunk {
                background-color: #dc3545;
            }
        """)
    
    def set_warning_state(self, warning_message: str):
        """
        Set progress bar to warning state.
        
        Args:
            warning_message: Warning message to display
        """
        self.setFormat(f"Warning: {warning_message}")
        self.setStyleSheet("""
            QProgressBar::chunk {
                background-color: #ffc107;
            }
        """)
    
    def set_success_state(self, success_message: str = ""):
        """
        Set progress bar to success state.
        
        Args:
            success_message: Success message to display
        """
        self._stop_pulse_animation()
        message = success_message or f"{self._current_operation} completed"
        self.setFormat(message)
        self.setStyleSheet("""
            QProgressBar::chunk {
                background-color: #28a745;
            }
        """)
        
        QTimer.singleShot(2000, self.hide_progress)
    
    def _complete_operation(self):
        """Handle operation completion."""
        self.set_success_state()
        self.operation_completed.emit()
    
    def cancel_operation(self):
        """Cancel the current operation."""
        self._stop_pulse_animation()
        self.setFormat("Operation cancelled")
        self.operation_cancelled.emit()
        QTimer.singleShot(1000, self.hide_progress)
    
    def hide_progress(self):
        """Hide the progress bar."""
        self.setVisible(False)
        self.reset()
        self._current_operation = ""
        self._reset_style()
    
    def _reset_style(self):
        """Reset to default style."""
        self.setStyleSheet("")
    
    def _start_pulse_animation(self):
        """Start pulse animation for indeterminate progress."""
        self._pulse_timer.start(50)  # 50ms intervals
    
    def _stop_pulse_animation(self):
        """Stop pulse animation."""
        self._pulse_timer.stop()
    
    def _pulse_animation(self):
        """Animate pulse effect for indeterminate progress."""
        self._pulse_value += self._pulse_direction * 2
        
        if self._pulse_value >= 100:
            self._pulse_direction = -1
        elif self._pulse_value <= 0:
            self._pulse_direction = 1
        
        # Apply pulse effect through style
        opacity = 0.3 + (self._pulse_value / 100.0) * 0.7
        self.setStyleSheet(f"""
            QProgressBar::chunk {{
                background-color: rgba(0, 123, 255, {opacity});
            }}
        """)
    
    def get_current_operation(self) -> str:
        """
        Get the current operation name.
        
        Returns:
            Current operation name
        """
        return self._current_operation
    
    def is_running(self) -> bool:
        """
        Check if an operation is currently running.
        
        Returns:
            True if operation is running
        """
        return self.isVisible() and self._current_operation
    
    def get_progress_percentage(self) -> float:
        """
        Get current progress as percentage.
        
        Returns:
            Progress percentage (0-100)
        """
        if self.maximum() == 0:
            return 0.0
        return (self.value() / self.maximum()) * 100
    
    def set_detailed_format(self, processed: int, total: int, rate: float = 0):
        """
        Set detailed progress format with processing rate.
        
        Args:
            processed: Number of items processed
            total: Total number of items
            rate: Processing rate (items per second)
        """
        if rate > 0:
            eta_seconds = (total - processed) / rate
            eta_minutes = int(eta_seconds // 60)
            eta_seconds = int(eta_seconds % 60)
            
            self.setFormat(
                f"{self._current_operation} - {processed}/{total} "
                f"({rate:.1f}/s, ETA: {eta_minutes:02d}:{eta_seconds:02d})"
            )
        else:
            self.setFormat(f"{self._current_operation} - {processed}/{total}")


class ProgressBarContainer(QWidget):
    """Container widget for progress bar with labels."""
    
    def __init__(self, parent=None):
        """Initialize the progress bar container."""
        super().__init__(parent)
        self._setup_ui()
    
    def _setup_ui(self):
        """Set up the UI layout."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)
        
        # Status label
        self.status_label = QLabel()
        self.status_label.setObjectName("statusLabel")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        # Progress bar
        self.progress_bar = TranslationProgressBar()
        
        # Details layout
        details_layout = QHBoxLayout()
        details_layout.setContentsMargins(0, 0, 0, 0)
        
        self.time_label = QLabel()
        self.time_label.setObjectName("timeLabel")
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        self.rate_label = QLabel()
        self.rate_label.setObjectName("rateLabel")
        self.rate_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        
        details_layout.addWidget(self.time_label)
        details_layout.addStretch()
        details_layout.addWidget(self.rate_label)
        
        layout.addWidget(self.status_label)
        layout.addWidget(self.progress_bar)
        layout.addLayout(details_layout)
        
        # Initially hidden
        self.setVisible(False)
    
    def start_operation(self, operation_name: str, status: str = "", total_items: int = 100):
        """Start operation with status."""
        self.status_label.setText(status or f"Starting {operation_name}...")
        self.time_label.setText("")
        self.rate_label.setText("")
        self.progress_bar.start_operation(operation_name, total_items)
        self.setVisible(True)
    
    def update_progress(self, current: int, status: str = "", elapsed_time: str = "", rate: str = ""):
        """Update progress with additional information."""
        if status:
            self.status_label.setText(status)
        if elapsed_time:
            self.time_label.setText(f"Elapsed: {elapsed_time}")
        if rate:
            self.rate_label.setText(f"Rate: {rate}")
        
        self.progress_bar.update_progress(current)
    
    def hide_progress(self):
        """Hide the entire progress container."""
        self.progress_bar.hide_progress()
        self.setVisible(False)
