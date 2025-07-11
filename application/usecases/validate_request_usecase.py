"""
Validate Request Use Case

Business logic for validating translation requests.
"""

import logging
from typing import List, Optional, Dict, Any
from pathlib import Path

from ..dto.translation_request import TranslationRequest
from ...interfaces.validators.validation_interface import ValidationInterface, ValidationReport


class ValidateRequestUseCase:
    """Use case for validating translation requests."""
    
    def __init__(self, validators: List[ValidationInterface]):
        """Initialize the use case with validators."""
        self.validators = validators
        self.logger = logging.getLogger(__name__)
    
    async def execute(self, request: TranslationRequest) -> ValidationReport:
        """Execute validation for a translation request."""
        self.logger.info(f"Validating translation request for file: {request.file_path}")
        
        report = ValidationReport()
        
        try:
            # Basic request validation
            await self._validate_basic_request(request, report)
            
            # File validation
            await self._validate_file(request, report)
            
            # Language validation
            await self._validate_languages(request, report)
            
            # Batch settings validation
            await self._validate_batch_settings(request, report)
            
            # Content validation
            await self._validate_content(request, report)
            
            # Run custom validators
            for validator in self.validators:
                try:
                    validator_report = await validator.validate(request)
                    report.results.extend(validator_report.results)
                except Exception as e:
                    self.logger.error(f"Validator {type(validator).__name__} failed: {str(e)}")
                    report.add_error(f"Validator {type(validator).__name__} failed: {str(e)}", 
                                   "VALIDATOR_ERROR")
            
            self.logger.info(f"Validation completed. Valid: {report.is_valid}, "
                           f"Errors: {len(report.get_errors())}, "
                           f"Warnings: {len(report.get_warnings())}")
            
        except Exception as e:
            self.logger.error(f"Validation failed: {str(e)}", exc_info=True)
            report.add_error(f"Validation process failed: {str(e)}", "VALIDATION_FAILED")
        
        return report
    
    async def _validate_basic_request(self, request: TranslationRequest, report: ValidationReport) -> None:
        """Validate basic request structure."""
        # Check required fields
        if not request.file_path:
            report.add_error("File path is required", "MISSING_FILE_PATH")
        
        if not request.language_settings:
            report.add_error("Language settings are required", "MISSING_LANGUAGE_SETTINGS")
        
        if not request.language_settings.target_language:
            report.add_error("Target language is required", "MISSING_TARGET_LANGUAGE")
        
        # Check batch settings
        if not request.batch_settings:
            report.add_error("Batch settings are required", "MISSING_BATCH_SETTINGS")
        
        # Check content filters
        if not request.content_filters:
            report.add_error("Content filters are required", "MISSING_CONTENT_FILTERS")
    
    async def _validate_file(self, request: TranslationRequest, report: ValidationReport) -> None:
        """Validate file-related aspects."""
        try:
            file_path = Path(request.file_path)
            
            # Check if file exists
            if not file_path.exists():
                report.add_error(f"File does not exist: {request.file_path}", "FILE_NOT_FOUND")
                return
            
            # Check if it's a file (not directory)
            if not file_path.is_file():
                report.add_error(f"Path is not a file: {request.file_path}", "NOT_A_FILE")
                return
            
            # Check file extension
            supported_extensions = ['.xlsx', '.xlsm', '.xls']
            if file_path.suffix.lower() not in supported_extensions:
                report.add_error(f"Unsupported file format: {file_path.suffix}. "
                               f"Supported formats: {', '.join(supported_extensions)}", 
                               "UNSUPPORTED_FORMAT")
            
            # Check file size
            file_size_mb = file_path.stat().st_size / (1024 * 1024)
            if file_size_mb > 100:  # 100 MB limit
                report.add_warning(f"Large file detected ({file_size_mb:.1f} MB). "
                                 "Processing may take longer.", "LARGE_FILE")
            elif file_size_mb > 500:  # 500 MB critical
                report.add_error(f"File too large ({file_size_mb:.1f} MB). "
                               "Maximum supported size is 500 MB.", "FILE_TOO_LARGE")
            
            # Check read permissions
            if not file_path.stat().st_mode & 0o444:  # Check read permission
                report.add_error(f"No read permission for file: {request.file_path}", 
                               "NO_READ_PERMISSION")
            
        except Exception as e:
            report.add_error(f"File validation failed: {str(e)}", "FILE_VALIDATION_ERROR")
    
    async def _validate_languages(self, request: TranslationRequest, report: ValidationReport) -> None:
        """Validate language settings."""
        lang_settings = request.language_settings
        
        # Common language codes
        common_languages = {
            'en', 'ja', 'vi', 'zh', 'ko', 'es', 'fr', 'de', 'it', 'pt', 'ru', 
            'ar', 'hi', 'th', 'id', 'ms', 'tl', 'auto'
        }
        
        # Validate target language
        if lang_settings.target_language not in common_languages:
            report.add_warning(f"Uncommon target language: {lang_settings.target_language}. "
                             "Please verify this is correct.", "UNCOMMON_TARGET_LANGUAGE")
        
        # Validate source language if provided
        if (lang_settings.source_language and 
            lang_settings.source_language not in common_languages):
            report.add_warning(f"Uncommon source language: {lang_settings.source_language}. "
                             "Please verify this is correct.", "UNCOMMON_SOURCE_LANGUAGE")
        
        # Check for same source and target language
        if (lang_settings.source_language and 
            lang_settings.source_language == lang_settings.target_language):
            report.add_error("Source and target languages cannot be the same", 
                           "SAME_SOURCE_TARGET_LANGUAGE")
        
        # Validate auto-detection settings
        if lang_settings.auto_detect_source and lang_settings.source_language:
            report.add_warning("Auto-detect is enabled but source language is specified. "
                             "Source language will be ignored.", "CONFLICTING_LANGUAGE_SETTINGS")
    
    async def _validate_batch_settings(self, request: TranslationRequest, report: ValidationReport) -> None:
        """Validate batch processing settings."""
        batch_settings = request.batch_settings
        
        # Validate batch size
        if batch_settings.batch_size <= 0:
            report.add_error("Batch size must be greater than 0", "INVALID_BATCH_SIZE")
        elif batch_settings.batch_size > 100:
            report.add_warning(f"Large batch size ({batch_settings.batch_size}). "
                             "Consider using smaller batches for better performance.", 
                             "LARGE_BATCH_SIZE")
        
        # Validate concurrent requests
        if batch_settings.max_concurrent_requests <= 0:
            report.add_error("Max concurrent requests must be greater than 0", 
                           "INVALID_CONCURRENT_REQUESTS")
        elif batch_settings.max_concurrent_requests > 10:
            report.add_warning(f"High concurrent requests ({batch_settings.max_concurrent_requests}). "
                             "This may trigger rate limits.", "HIGH_CONCURRENT_REQUESTS")
        
        # Validate retry settings
        if batch_settings.retry_attempts < 0:
            report.add_error("Retry attempts cannot be negative", "INVALID_RETRY_ATTEMPTS")
        elif batch_settings.retry_attempts > 5:
            report.add_warning(f"High retry attempts ({batch_settings.retry_attempts}). "
                             "This may slow down processing.", "HIGH_RETRY_ATTEMPTS")
        
        if batch_settings.retry_delay < 0:
            report.add_error("Retry delay cannot be negative", "INVALID_RETRY_DELAY")
        elif batch_settings.retry_delay > 10:
            report.add_warning(f"Long retry delay ({batch_settings.retry_delay}s). "
                             "This may slow down processing.", "LONG_RETRY_DELAY")
    
    async def _validate_content(self, request: TranslationRequest, report: ValidationReport) -> None:
        """Validate content to be translated."""
        # Check if there are cells to translate
        if not request.cells:
            report.add_warning("No cells specified for translation", "NO_CELLS_TO_TRANSLATE")
            return
        
        # Validate cell count
        cell_count = len(request.cells)
        if cell_count > 50000:
            report.add_error(f"Too many cells to translate ({cell_count}). "
                           "Maximum supported is 50,000 cells.", "TOO_MANY_CELLS")
        elif cell_count > 10000:
            report.add_warning(f"Large number of cells to translate ({cell_count}). "
                             "Processing may take significant time.", "MANY_CELLS")
        
        # Check total characters
        total_chars = request.get_total_characters()
        if total_chars > 1000000:  # 1M characters
            report.add_error(f"Too much text to translate ({total_chars:,} characters). "
                           "Maximum supported is 1,000,000 characters.", "TOO_MUCH_TEXT")
        elif total_chars > 100000:  # 100K characters
            report.add_warning(f"Large amount of text to translate ({total_chars:,} characters). "
                             "Processing may take significant time.", "MUCH_TEXT")
        
        # Check for empty cells
        empty_cells = sum(1 for cell in request.cells if not cell.text.strip())
        if empty_cells > 0:
            report.add_info(f"Found {empty_cells} empty cells that will be skipped", 
                          "EMPTY_CELLS_FOUND")
        
        # Validate cell positions
        invalid_positions = []
        for i, cell in enumerate(request.cells):
            if cell.row < 1 or cell.column < 1:
                invalid_positions.append(i)
        
        if invalid_positions:
            report.add_error(f"Invalid cell positions found at indices: {invalid_positions[:10]}...", 
                           "INVALID_CELL_POSITIONS")
    
    def get_validation_summary(self, report: ValidationReport) -> Dict[str, Any]:
        """Get a summary of validation results."""
        return {
            'is_valid': report.is_valid,
            'total_checks': len(report.results),
            'errors': len(report.get_errors()),
            'warnings': len(report.get_warnings()),
            'error_messages': [r.message for r in report.get_errors()],
            'warning_messages': [r.message for r in report.get_warnings()],
            'can_proceed': report.is_valid and not report.has_errors
        }
