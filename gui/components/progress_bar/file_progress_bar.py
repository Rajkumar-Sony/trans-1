"""
File Operation Progress Bar Component

Modern QProgressBar implementation for file operations.
"""

from PyQt6.QtWidgets import QProgressBar, QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import pyqtSignal, QTimer, Qt
from PyQt6.QtGui import QMovie
from typing import Optional
from enum import Enum


class FileOperationType(Enum):
    """Types of file operations."""
    LOADING = "loading"
    SAVING = "saving"
    PROCESSING = "processing"
    VALIDATING = "validating"
    EXPORTING = "exporting"


class FileProgressBar(QProgressBar):
    """Custom progress bar for file operations with modern styling."""
    
    # Signals
    operation_completed = pyqtSignal(str)  # Emits operation type
    operation_failed = pyqtSignal(str, str)  # Emits operation type and error
    
    def __init__(self, parent=None):
        """Initialize the file progress bar."""
        super().__init__(parent)
        self._setup_ui()
        self._current_operation: Optional[FileOperationType] = None
        self._file_name = ""
    
    def _setup_ui(self):
        """Set up the UI components."""
        self.setObjectName("fileProgressBar")
        self.setMinimum(0)
        self.setMaximum(100)
        self.setValue(0)
        self.setTextVisible(True)
        
        # Set initial state
        self.setVisible(False)
    
    def start_file_operation(self, operation: FileOperationType, file_name: str = "", file_size: int = 0):
        """
        Start a file operation.
        
        Args:
            operation: Type of file operation
            file_name: Name of the file being processed
            file_size: Size of the file in bytes (for progress calculation)
        """
        self._current_operation = operation
        self._file_name = file_name
        
        # Set operation-specific settings
        operation_configs = {
            FileOperationType.LOADING: {
                "format": f"Loading {file_name}... %p%",
                "style": "background-color: #007bff;"
            },
            FileOperationType.SAVING: {
                "format": f"Saving {file_name}... %p%",
                "style": "background-color: #28a745;"
            },
            FileOperationType.PROCESSING: {
                "format": f"Processing {file_name}... %p%",
                "style": "background-color: #ffc107;"
            },
            FileOperationType.VALIDATING: {
                "format": f"Validating {file_name}... %p%",
                "style": "background-color: #17a2b8;"
            },
            FileOperationType.EXPORTING: {
                "format": f"Exporting {file_name}... %p%",
                "style": "background-color: #6f42c1;"
            }
        }
        
        config = operation_configs.get(operation, operation_configs[FileOperationType.PROCESSING])
        
        self.setFormat(config["format"])
        self.setStyleSheet(f"QProgressBar::chunk {{ {config['style']} }}")
        
        if file_size > 0:
            self.setMaximum(file_size)
        else:
            self.setMaximum(100)
        
        self.setValue(0)
        self.setVisible(True)
    
    def update_file_progress(self, bytes_processed: int):
        """
        Update file operation progress.
        
        Args:
            bytes_processed: Number of bytes processed
        """
        self.setValue(bytes_processed)
        
        # Update format with file size info if available
        if self.maximum() > 100:  # Assuming byte-based progress
            mb_processed = bytes_processed / (1024 * 1024)
            mb_total = self.maximum() / (1024 * 1024)
            
            operation_name = self._current_operation.value.capitalize() if self._current_operation else "Processing"
            self.setFormat(f"{operation_name} {self._file_name}... {mb_processed:.1f}/{mb_total:.1f} MB")
    
    def set_indeterminate(self, message: str = ""):
        """
        Set progress to indeterminate mode.
        
        Args:
            message: Custom message to display
        """
        self.setMinimum(0)
        self.setMaximum(0)
        
        if message:
            self.setFormat(message)
        elif self._current_operation:
            operation_name = self._current_operation.value.capitalize()
            self.setFormat(f"{operation_name} {self._file_name}...")
    
    def complete_operation(self, success: bool = True, message: str = ""):
        """
        Complete the current file operation.
        
        Args:
            success: Whether operation was successful
            message: Custom completion message
        """
        if success:
            self._set_success_state(message)
            if self._current_operation:
                self.operation_completed.emit(self._current_operation.value)
        else:
            self._set_error_state(message)
            if self._current_operation:
                self.operation_failed.emit(self._current_operation.value, message)
        
        # Hide after delay
        QTimer.singleShot(1500, self.hide_progress)
    
    def _set_success_state(self, message: str = ""):
        """Set progress bar to success state."""
        if message:
            self.setFormat(message)
        elif self._current_operation:
            operation_name = self._current_operation.value.capitalize()
            self.setFormat(f"{operation_name} completed successfully")
        
        self.setStyleSheet("""
            QProgressBar::chunk {
                background-color: #28a745;
            }
        """)
        self.setValue(self.maximum())
    
    def _set_error_state(self, message: str = ""):
        """Set progress bar to error state."""
        if message:
            self.setFormat(f"Error: {message}")
        else:
            self.setFormat("Operation failed")
        
        self.setStyleSheet("""
            QProgressBar::chunk {
                background-color: #dc3545;
            }
        """)
    
    def hide_progress(self):
        """Hide the progress bar and reset state."""
        self.setVisible(False)
        self.setValue(0)
        self.setMinimum(0)
        self.setMaximum(100)
        self._current_operation = None
        self._file_name = ""
        self.setStyleSheet("")
    
    def get_current_operation(self) -> Optional[FileOperationType]:
        """
        Get the current operation type.
        
        Returns:
            Current operation type or None
        """
        return self._current_operation
    
    def get_file_name(self) -> str:
        """
        Get the current file name being processed.
        
        Returns:
            Current file name
        """
        return self._file_name
    
    def is_processing(self) -> bool:
        """
        Check if a file operation is in progress.
        
        Returns:
            True if operation is in progress
        """
        return self.isVisible() and self._current_operation is not None
    
    def cancel_operation(self):
        """Cancel the current operation."""
        if self._current_operation:
            operation_name = self._current_operation.value.capitalize()
            self.setFormat(f"{operation_name} cancelled")
            self.setStyleSheet("""
                QProgressBar::chunk {
                    background-color: #6c757d;
                }
            """)
            QTimer.singleShot(1000, self.hide_progress)


class FileProgressWidget(QWidget):
    """Widget containing file progress bar with status label."""
    
    def __init__(self, parent=None):
        """Initialize the file progress widget."""
        super().__init__(parent)
        self._setup_ui()
    
    def _setup_ui(self):
        """Set up the UI layout."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(3)
        
        # Status label
        self.status_label = QLabel()
        self.status_label.setObjectName("fileStatusLabel")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Progress bar
        self.progress_bar = FileProgressBar()
        
        layout.addWidget(self.status_label)
        layout.addWidget(self.progress_bar)
        
        # Connect signals
        self.progress_bar.operation_completed.connect(self._on_operation_completed)
        self.progress_bar.operation_failed.connect(self._on_operation_failed)
        
        # Initially hidden
        self.setVisible(False)
    
    def start_operation(self, operation: FileOperationType, file_name: str = "", 
                       status_message: str = "", file_size: int = 0):
        """
        Start a file operation with status message.
        
        Args:
            operation: Type of file operation
            file_name: Name of the file
            status_message: Status message to display
            file_size: Size of the file in bytes
        """
        if status_message:
            self.status_label.setText(status_message)
        else:
            operation_name = operation.value.capitalize()
            self.status_label.setText(f"{operation_name} file...")
        
        self.progress_bar.start_file_operation(operation, file_name, file_size)
        self.setVisible(True)
    
    def update_status(self, message: str):
        """Update the status message."""
        self.status_label.setText(message)
    
    def _on_operation_completed(self, operation_type: str):
        """Handle operation completion."""
        self.status_label.setText(f"{operation_type.capitalize()} completed successfully")
    
    def _on_operation_failed(self, operation_type: str, error: str):
        """Handle operation failure."""
        self.status_label.setText(f"{operation_type.capitalize()} failed: {error}")
    
    def hide_progress(self):
        """Hide the progress widget."""
        self.progress_bar.hide_progress()
        self.setVisible(False)
