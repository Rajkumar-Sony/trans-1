"""
File Drop Zone Component

Modern drag and drop widget for file selection.
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame
from PyQt6.QtCore import pyqtSignal, Qt, QMimeData, QUrl
from PyQt6.QtGui import QDragEnterEvent, QDropEvent, QPainter, QPen, QBrush, QColor
from typing import List, Optional
import os


class FileDropZone(QFrame):
    """Custom widget for drag and drop file selection with modern styling."""
    
    # Signals
    files_dropped = pyqtSignal(list)  # Emits list of file paths
    file_hovered = pyqtSignal(bool)   # Emits True when file is hovered over zone
    
    def __init__(self, parent=None):
        """Initialize the file drop zone."""
        super().__init__(parent)
        self._accepted_extensions = ['.xlsx', '.xlsm', '.xls', '.csv']
        self._is_hovering = False
        self._is_active = True
        self._setup_ui()
    
    def _setup_ui(self):
        """Set up the UI components."""
        self.setObjectName("fileDropZone")
        self.setFrameStyle(QFrame.Shape.Box)
        self.setLineWidth(2)
        self.setAcceptDrops(True)
        self.setMinimumHeight(120)
        
        # Create layout
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(10)
        
        # Icon label (could be replaced with actual icon)
        self.icon_label = QLabel("📁")
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.icon_label.setStyleSheet("font-size: 32px;")
        
        # Main text label
        self.main_label = QLabel("Drop Excel files here")
        self.main_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_label.setObjectName("dropMainLabel")
        
        # Subtitle label
        self.subtitle_label = QLabel("or click to browse")
        self.subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.subtitle_label.setObjectName("dropSubtitleLabel")
        
        # Supported formats label
        formats_text = f"Supported: {', '.join(self._accepted_extensions)}"
        self.formats_label = QLabel(formats_text)
        self.formats_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.formats_label.setObjectName("dropFormatsLabel")
        
        layout.addWidget(self.icon_label)
        layout.addWidget(self.main_label)
        layout.addWidget(self.subtitle_label)
        layout.addWidget(self.formats_label)
        
        self._update_appearance()
    
    def _update_appearance(self):
        """Update visual appearance based on state."""
        if not self._is_active:
            self.setStyleSheet("""
                QFrame#fileDropZone {
                    border: 2px dashed #cccccc;
                    border-radius: 8px;
                    background-color: #f8f9fa;
                }
            """)
            return
            
        if self._is_hovering:
            self.setStyleSheet("""
                QFrame#fileDropZone {
                    border: 2px dashed #007bff;
                    border-radius: 8px;
                    background-color: #e7f3ff;
                }
                QLabel#dropMainLabel {
                    color: #007bff;
                    font-weight: bold;
                }
            """)
        else:
            self.setStyleSheet("""
                QFrame#fileDropZone {
                    border: 2px dashed #6c757d;
                    border-radius: 8px;
                    background-color: #ffffff;
                }
                QFrame#fileDropZone:hover {
                    border-color: #007bff;
                    background-color: #f8f9fa;
                }
                QLabel#dropMainLabel {
                    color: #495057;
                    font-size: 14px;
                    font-weight: bold;
                }
                QLabel#dropSubtitleLabel {
                    color: #6c757d;
                    font-size: 12px;
                }
                QLabel#dropFormatsLabel {
                    color: #868e96;
                    font-size: 10px;
                }
            """)
    
    def dragEnterEvent(self, event: QDragEnterEvent):
        """Handle drag enter event."""
        if not self._is_active:
            event.ignore()
            return
            
        if self._has_valid_files(event.mimeData()):
            event.acceptProposedAction()
            self._is_hovering = True
            self._update_appearance()
            self.file_hovered.emit(True)
        else:
            event.ignore()
    
    def dragLeaveEvent(self, event):
        """Handle drag leave event."""
        self._is_hovering = False
        self._update_appearance()
        self.file_hovered.emit(False)
        super().dragLeaveEvent(event)
    
    def dropEvent(self, event: QDropEvent):
        """Handle drop event."""
        if not self._is_active:
            event.ignore()
            return
            
        files = self._extract_file_paths(event.mimeData())
        valid_files = [f for f in files if self._is_valid_file(f)]
        
        if valid_files:
            event.acceptProposedAction()
            self.files_dropped.emit(valid_files)
        else:
            event.ignore()
        
        self._is_hovering = False
        self._update_appearance()
        self.file_hovered.emit(False)
    
    def mousePressEvent(self, event):
        """Handle mouse press for click-to-browse functionality."""
        if self._is_active and event.button() == Qt.MouseButton.LeftButton:
            self.files_dropped.emit([])  # Emit empty list to trigger file dialog
        super().mousePressEvent(event)
    
    def _has_valid_files(self, mime_data: QMimeData) -> bool:
        """
        Check if mime data contains valid files.
        
        Args:
            mime_data: The mime data to check
            
        Returns:
            True if contains valid files
        """
        if not mime_data.hasUrls():
            return False
            
        files = self._extract_file_paths(mime_data)
        return any(self._is_valid_file(f) for f in files)
    
    def _extract_file_paths(self, mime_data: QMimeData) -> List[str]:
        """
        Extract file paths from mime data.
        
        Args:
            mime_data: The mime data containing URLs
            
        Returns:
            List of file paths
        """
        files = []
        for url in mime_data.urls():
            if url.isLocalFile():
                file_path = url.toLocalFile()
                if os.path.isfile(file_path):
                    files.append(file_path)
        return files
    
    def _is_valid_file(self, file_path: str) -> bool:
        """
        Check if file is valid for processing.
        
        Args:
            file_path: Path to the file
            
        Returns:
            True if file is valid
        """
        if not os.path.isfile(file_path):
            return False
            
        file_ext = os.path.splitext(file_path)[1].lower()
        return file_ext in self._accepted_extensions
    
    def set_accepted_extensions(self, extensions: List[str]):
        """
        Set accepted file extensions.
        
        Args:
            extensions: List of accepted extensions (with dots)
        """
        self._accepted_extensions = extensions
        formats_text = f"Supported: {', '.join(extensions)}"
        self.formats_label.setText(formats_text)
    
    def set_active(self, active: bool):
        """
        Set whether the drop zone is active.
        
        Args:
            active: Whether to activate the drop zone
        """
        self._is_active = active
        self.setAcceptDrops(active)
        
        if active:
            self.main_label.setText("Drop Excel files here")
            self.subtitle_label.setText("or click to browse")
        else:
            self.main_label.setText("File processing in progress")
            self.subtitle_label.setText("Please wait...")
        
        self._update_appearance()
    
    def set_custom_message(self, main_text: str, subtitle_text: str = ""):
        """
        Set custom message in the drop zone.
        
        Args:
            main_text: Main message text
            subtitle_text: Subtitle text
        """
        self.main_label.setText(main_text)
        self.subtitle_label.setText(subtitle_text)
    
    def reset_to_default(self):
        """Reset drop zone to default state."""
        self.set_active(True)
        self.main_label.setText("Drop Excel files here")
        self.subtitle_label.setText("or click to browse")
    
    def show_error(self, error_message: str):
        """
        Show error state in drop zone.
        
        Args:
            error_message: Error message to display
        """
        self.main_label.setText("❌ Error")
        self.subtitle_label.setText(error_message)
        self.setStyleSheet("""
            QFrame#fileDropZone {
                border: 2px dashed #dc3545;
                border-radius: 8px;
                background-color: #f8d7da;
            }
            QLabel#dropMainLabel {
                color: #721c24;
            }
            QLabel#dropSubtitleLabel {
                color: #721c24;
            }
        """)
    
    def show_success(self, file_name: str):
        """
        Show success state in drop zone.
        
        Args:
            file_name: Name of the successfully loaded file
        """
        self.main_label.setText("✅ File loaded")
        self.subtitle_label.setText(f"{os.path.basename(file_name)}")
        self.setStyleSheet("""
            QFrame#fileDropZone {
                border: 2px dashed #28a745;
                border-radius: 8px;
                background-color: #d1eddd;
            }
            QLabel#dropMainLabel {
                color: #155724;
            }
            QLabel#dropSubtitleLabel {
                color: #155724;
            }
        """)
    
    def get_accepted_extensions(self) -> List[str]:
        """
        Get list of accepted file extensions.
        
        Returns:
            List of accepted extensions
        """
        return self._accepted_extensions.copy()
    
    def is_active(self) -> bool:
        """
        Check if drop zone is active.
        
        Returns:
            True if active
        """
        return self._is_active
