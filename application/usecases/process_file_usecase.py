"""
Process File Use Case

Business logic for processing Excel files end-to-end.
"""

import logging
from typing import Optional, Dict, Any, List
from datetime import datetime
from pathlib import Path

from application.dto.translation_request import TranslationRequest
from application.dto.translation_response import TranslationResponse, TranslationStatus
from application.dto.file_info import FileInfo
from application.usecases.translate_text_usecase import TranslateTextUseCase
from application.usecases.validate_request_usecase import ValidateRequestUseCase
from application.usecases.detect_language_usecase import DetectLanguageUseCase
from interfaces.repositories.file_repository_interface import FileRepositoryInterface
from interfaces.services.file_service_interface import FileServiceInterface


class ProcessFileUseCase:
    """Use case for processing Excel files end-to-end."""
    
    def __init__(self, 
                 file_repository: FileRepositoryInterface,
                 file_service: FileServiceInterface,
                 translate_usecase: TranslateTextUseCase,
                 validate_usecase: ValidateRequestUseCase,
                 detect_language_usecase: DetectLanguageUseCase):
        """Initialize the use case with dependencies."""
        self.file_repository = file_repository
        self.file_service = file_service
        self.translate_usecase = translate_usecase
        self.validate_usecase = validate_usecase
        self.detect_language_usecase = detect_language_usecase
        self.logger = logging.getLogger(__name__)
    
    async def execute(self, request: TranslationRequest, 
                     output_path: Optional[str] = None) -> TranslationResponse:
        """Execute the complete file processing workflow."""
        self.logger.info(f"Starting file processing for: {request.file_path}")
        start_time = datetime.now()
        
        try:
            # Step 1: Validate request
            self.logger.info("Step 1: Validating request...")
            validation_report = await self.validate_usecase.execute(request)
            
            if not validation_report.is_valid or validation_report.has_errors:
                self.logger.error("Request validation failed")
                return self._create_failed_response(
                    request, start_time, "Request validation failed", 
                    [error.message for error in validation_report.get_errors()]
                )
            
            # Step 2: Analyze file
            self.logger.info("Step 2: Analyzing file...")
            file_info = await self.file_service.analyze_file(request.file_path)
            
            if not file_info.validation_result.can_process:
                self.logger.error("File cannot be processed")
                return self._create_failed_response(
                    request, start_time, "File cannot be processed", 
                    file_info.validation_result.errors
                )
            
            # Step 3: Create backup
            self.logger.info("Step 3: Creating backup...")
            try:
                backup_path = await self.file_service.create_backup(request.file_path)
                self.logger.info(f"Backup created: {backup_path}")
            except Exception as e:
                self.logger.warning(f"Failed to create backup: {str(e)}")
                # Continue processing without backup
            
            # Step 4: Extract content
            self.logger.info("Step 4: Extracting content...")
            sheet_names = request.sheet_names if request.sheet_names else file_info.get_sheet_names()
            content = await self.file_service.extract_content(request.file_path, sheet_names)
            
            # Step 5: Prepare translation request
            self.logger.info("Step 5: Preparing translation data...")
            await self._populate_translation_cells(request, content, file_info)
            
            # Step 6: Auto-detect source language if needed
            if request.language_settings.auto_detect_source:
                self.logger.info("Step 6: Auto-detecting source language...")
                await self._auto_detect_source_language(request)
            
            # Step 7: Execute translation
            self.logger.info("Step 7: Executing translation...")
            translation_response = await self.translate_usecase.execute(request)
            
            # Step 8: Apply translations to file
            if translation_response.is_successful and output_path:
                self.logger.info("Step 8: Applying translations to file...")
                success = await self._apply_translations_to_file(
                    request.file_path, translation_response, output_path
                )
                
                if success:
                    translation_response.output_file_path = output_path
                    self.logger.info(f"Translations applied successfully: {output_path}")
                else:
                    translation_response.add_warning("Failed to save translated file")
            
            # Step 9: Cleanup
            self.logger.info("Step 9: Cleanup...")
            await self._cleanup_resources()
            
            end_time = datetime.now()
            total_time = (end_time - start_time).total_seconds()
            self.logger.info(f"File processing completed in {total_time:.2f} seconds")
            
            return translation_response
            
        except Exception as e:
            self.logger.error(f"File processing failed: {str(e)}", exc_info=True)
            return self._create_failed_response(
                request, start_time, f"Processing failed: {str(e)}"
            )
    
    async def _populate_translation_cells(self, request: TranslationRequest, 
                                        content: Dict[str, List[tuple]], 
                                        file_info: FileInfo) -> None:
        """Populate the request with cells to translate."""
        request.cells.clear()
        
        for sheet_name, cells in content.items():
            for text, row, col in cells:
                # Apply content filters
                if not request.should_ignore_text(text):
                    # Add metadata to help with grouping
                    cell_request = request.__class__.__dict__['cells'].__class__(
                        text=text, row=row, column=col, preserve_formatting=True
                    )
                    # Add sheet name to metadata for grouping
                    if not hasattr(cell_request, 'metadata'):
                        cell_request.metadata = {}
                    cell_request.metadata['sheet_name'] = sheet_name
                    request.cells.append(cell_request)
        
        self.logger.info(f"Prepared {len(request.cells)} cells for translation across "
                        f"{len(content)} sheets")
    
    async def _auto_detect_source_language(self, request: TranslationRequest) -> None:
        """Auto-detect source language from content."""
        if not request.cells:
            return
        
        # Sample up to 10 cells for language detection
        sample_texts = [cell.text for cell in request.cells[:10] if cell.text.strip()]
        
        if sample_texts:
            detected_language = await self.detect_language_usecase.detect_most_common_language(
                sample_texts, min_confidence=0.7
            )
            
            if detected_language and detected_language != "unknown":
                request.language_settings.source_language = detected_language
                self.logger.info(f"Auto-detected source language: {detected_language}")
            else:
                self.logger.warning("Could not auto-detect source language with sufficient confidence")
    
    async def _apply_translations_to_file(self, input_path: str, 
                                        response: TranslationResponse, 
                                        output_path: str) -> bool:
        """Apply translations to the original file and save as new file."""
        try:
            # Prepare translation data in the format expected by file repository
            translation_data = {}
            
            for sheet_result in response.sheet_results:
                if sheet_result.is_successful:
                    sheet_translations = []
                    for cell_result in sheet_result.cell_results:
                        if cell_result.is_successful:
                            sheet_translations.append((
                                cell_result.translated_text,
                                cell_result.row,
                                cell_result.column
                            ))
                    translation_data[sheet_result.sheet_name] = sheet_translations
            
            # Apply translations using file repository
            success = await self.file_repository.apply_translations(
                input_path, translation_data, output_path
            )
            
            return success
            
        except Exception as e:
            self.logger.error(f"Failed to apply translations to file: {str(e)}")
            return False
    
    async def _cleanup_resources(self) -> None:
        """Clean up temporary resources."""
        try:
            # Clean up temporary files
            await self.file_service.cleanup_temporary_files()
            
            # Clean up old backups (keep last 5 days)
            await self.file_service.cleanup_backups(max_age_days=5)
            
        except Exception as e:
            self.logger.warning(f"Cleanup failed: {str(e)}")
    
    def _create_failed_response(self, request: TranslationRequest, 
                              start_time: datetime, 
                              error_message: str,
                              additional_errors: Optional[List[str]] = None) -> TranslationResponse:
        """Create a failed response."""
        from ..dto.translation_response import TranslationMetrics
        
        response = TranslationResponse(
            request_id=self._generate_request_id(),
            status=TranslationStatus.FAILED,
            file_path=request.file_path,
            output_file_path=None,
            sheet_results=[],
            metrics=TranslationMetrics(
                total_files=1, total_sheets=0, total_cells=0, total_characters=0,
                successful_translations=0, failed_translations=0, skipped_cells=0,
                api_calls_made=0, total_processing_time=0, average_time_per_cell=0,
                characters_per_second=0
            ),
            errors=[],
            warnings=[],
            started_at=start_time,
            completed_at=datetime.now()
        )
        
        response.add_error("PROCESSING_FAILED", error_message)
        
        if additional_errors:
            for error in additional_errors:
                response.add_error("VALIDATION_ERROR", error)
        
        return response
    
    def _generate_request_id(self) -> str:
        """Generate unique request ID."""
        import uuid
        return str(uuid.uuid4())
    
    async def get_file_analysis(self, file_path: str) -> FileInfo:
        """Get detailed file analysis without processing."""
        self.logger.info(f"Analyzing file: {file_path}")
        
        try:
            file_info = await self.file_service.analyze_file(file_path)
            return file_info
            
        except Exception as e:
            self.logger.error(f"File analysis failed: {str(e)}", exc_info=True)
            # Return basic info with error
            file_info = FileInfo.create_from_path(file_path)
            file_info.validation_result.is_valid = False
            file_info.validation_result.errors.append(str(e))
            return file_info
    
    async def estimate_processing_cost(self, request: TranslationRequest) -> Dict[str, Any]:
        """Estimate the cost and time for processing the request."""
        try:
            # Analyze file first
            file_info = await self.file_service.analyze_file(request.file_path)
            
            # Estimate characters to translate
            estimated_chars = file_info.estimated_translation_characters
            
            # Get cost estimate from translation service
            if hasattr(self.translate_usecase.translation_service, 'estimate_cost'):
                estimated_cost = await self.translate_usecase.translation_service.estimate_cost(estimated_chars)
            else:
                estimated_cost = 0.0
            
            # Estimate processing time
            estimated_time = file_info.estimate_processing_time()
            
            return {
                'estimated_characters': estimated_chars,
                'estimated_cost': estimated_cost,
                'estimated_time_seconds': estimated_time,
                'estimated_time_minutes': estimated_time / 60,
                'file_complexity': file_info.calculate_complexity_score(),
                'recommended_batch_size': file_info.characteristics.recommended_batch_size,
                'estimated_api_calls': file_info.characteristics.estimated_api_calls
            }
            
        except Exception as e:
            self.logger.error(f"Cost estimation failed: {str(e)}")
            return {
                'estimated_characters': 0,
                'estimated_cost': 0.0,
                'estimated_time_seconds': 0.0,
                'estimated_time_minutes': 0.0,
                'file_complexity': 0.0,
                'error': str(e)
            }
