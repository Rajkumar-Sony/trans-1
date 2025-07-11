"""
Translate Text Use Case

Business logic for translating text content.
"""

import logging
from typing import List, Optional, Dict, Any
from datetime import datetime

from application.dto.translation_request import TranslationRequest, CellTranslationRequest
from application.dto.translation_response import (
    TranslationResponse, CellTranslationResult, SheetTranslationResult, 
    TranslationMetrics, TranslationStatus
)
from interfaces.services.translation_service_interface import TranslationServiceInterface
from domain.entities.translation import Translation, TranslationProvider


class TranslateTextUseCase:
    """Use case for translating text content."""
    
    def __init__(self, translation_service: TranslationServiceInterface):
        """Initialize the use case with translation service."""
        self.translation_service = translation_service
        self.logger = logging.getLogger(__name__)
    
    async def execute(self, request: TranslationRequest) -> TranslationResponse:
        """Execute the translation use case."""
        self.logger.info(f"Starting translation for {len(request.cells)} cells")
        start_time = datetime.now()
        request_id = self._generate_request_id()
        
        try:
            # Group cells by sheet
            sheets_data = self._group_cells_by_sheet(request.cells)
            
            # Process each sheet
            sheet_results = []
            total_successful = 0
            total_failed = 0
            total_skipped = 0
            total_api_calls = 0
            
            for sheet_name, cells in sheets_data.items():
                self.logger.info(f"Processing sheet: {sheet_name} ({len(cells)} cells)")
                
                sheet_result = await self._translate_sheet(
                    sheet_name, cells, request.language_settings, 
                    request.batch_settings, request.content_filters
                )
                
                sheet_results.append(sheet_result)
                total_successful += sheet_result.successful_translations
                total_failed += sheet_result.failed_translations
                total_skipped += sheet_result.skipped_cells
                
                # Estimate API calls (rough approximation)
                total_api_calls += (len(cells) // request.batch_settings.batch_size) + 1
            
            # Calculate metrics
            end_time = datetime.now()
            total_processing_time = (end_time - start_time).total_seconds()
            total_cells = len(request.cells)
            total_characters = request.get_total_characters()
            
            metrics = TranslationMetrics(
                total_files=1,
                total_sheets=len(sheets_data),
                total_cells=total_cells,
                total_characters=total_characters,
                successful_translations=total_successful,
                failed_translations=total_failed,
                skipped_cells=total_skipped,
                api_calls_made=total_api_calls,
                total_processing_time=total_processing_time,
                average_time_per_cell=total_processing_time / max(total_cells, 1),
                characters_per_second=total_characters / max(total_processing_time, 0.1)
            )
            
            # Determine overall status
            if total_failed == 0 and total_successful > 0:
                status = TranslationStatus.SUCCESS
            elif total_successful > 0:
                status = TranslationStatus.PARTIAL_SUCCESS
            else:
                status = TranslationStatus.FAILED
            
            response = TranslationResponse(
                request_id=request_id,
                status=status,
                file_path=request.file_path,
                output_file_path=None,  # Will be set when file is saved
                sheet_results=sheet_results,
                metrics=metrics,
                errors=[],
                warnings=[],
                started_at=start_time,
                completed_at=end_time
            )
            
            self.logger.info(f"Translation completed. Success rate: {metrics.overall_success_rate:.1f}%")
            return response
            
        except Exception as e:
            self.logger.error(f"Translation failed: {str(e)}", exc_info=True)
            end_time = datetime.now()
            
            # Return failed response
            return TranslationResponse(
                request_id=request_id,
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
                completed_at=end_time
            )
    
    def _group_cells_by_sheet(self, cells: List[CellTranslationRequest]) -> Dict[str, List[CellTranslationRequest]]:
        """Group cells by sheet name."""
        sheets = {}
        for cell in cells:
            sheet_name = cell.metadata.get('sheet_name', 'Sheet1') if hasattr(cell, 'metadata') else 'Sheet1'
            if sheet_name not in sheets:
                sheets[sheet_name] = []
            sheets[sheet_name].append(cell)
        return sheets
    
    async def _translate_sheet(self, sheet_name: str, cells: List[CellTranslationRequest],
                              language_settings, batch_settings, content_filters) -> SheetTranslationResult:
        """Translate all cells in a sheet."""
        start_time = datetime.now()
        results = []
        successful = 0
        failed = 0
        skipped = 0
        
        try:
            # Process cells in batches
            for i in range(0, len(cells), batch_settings.batch_size):
                batch = cells[i:i + batch_settings.batch_size]
                batch_results = await self._translate_batch(
                    batch, language_settings, content_filters
                )
                
                for result in batch_results:
                    results.append(result)
                    if result.is_successful:
                        successful += 1
                    elif result.error_message:
                        failed += 1
                    else:
                        skipped += 1
        
        except Exception as e:
            self.logger.error(f"Error translating sheet {sheet_name}: {str(e)}")
            failed = len(cells)
        
        end_time = datetime.now()
        processing_time = (end_time - start_time).total_seconds()
        
        return SheetTranslationResult(
            sheet_name=sheet_name,
            total_cells=len(cells),
            successful_translations=successful,
            failed_translations=failed,
            skipped_cells=skipped,
            cell_results=results,
            processing_time=processing_time
        )
    
    async def _translate_batch(self, batch: List[CellTranslationRequest],
                              language_settings, content_filters) -> List[CellTranslationResult]:
        """Translate a batch of cells."""
        results = []
        
        # Extract texts for batch translation
        texts_to_translate = []
        cell_mapping = []
        
        for cell in batch:
            # Check if text should be ignored
            if self._should_skip_text(cell.text, content_filters):
                result = CellTranslationResult(
                    original_text=cell.text,
                    translated_text=cell.text,  # Keep original
                    row=cell.row,
                    column=cell.column,
                    source_language_detected=None,
                    confidence_score=None,
                    processing_time=0.0
                )
                results.append(result)
                continue
            
            texts_to_translate.append(cell.text)
            cell_mapping.append(cell)
        
        if not texts_to_translate:
            return results
        
        try:
            # Call translation service
            start_time = datetime.now()
            translated_texts = await self.translation_service.translate_batch(
                texts=texts_to_translate,
                source_language=language_settings.source_language,
                target_language=language_settings.target_language
            )
            end_time = datetime.now()
            processing_time = (end_time - start_time).total_seconds()
            
            # Create results
            for i, (cell, translated_text) in enumerate(zip(cell_mapping, translated_texts)):
                result = CellTranslationResult(
                    original_text=cell.text,
                    translated_text=translated_text,
                    row=cell.row,
                    column=cell.column,
                    source_language_detected=language_settings.source_language,
                    confidence_score=1.0,  # Default confidence
                    processing_time=processing_time / len(translated_texts)
                )
                results.append(result)
        
        except Exception as e:
            self.logger.error(f"Batch translation failed: {str(e)}")
            
            # Create error results
            for cell in cell_mapping:
                result = CellTranslationResult(
                    original_text=cell.text,
                    translated_text="",
                    row=cell.row,
                    column=cell.column,
                    source_language_detected=None,
                    confidence_score=None,
                    processing_time=0.0,
                    error_message=str(e)
                )
                results.append(result)
        
        return results
    
    def _should_skip_text(self, text: str, content_filters) -> bool:
        """Check if text should be skipped based on filters."""
        import re
        
        if not text or not text.strip():
            return True
        
        # Check square brackets
        if content_filters.ignore_square_brackets and '[' in text and ']' in text:
            if re.search(r'\[.*\]', text):
                return True
        
        # Check Japanese quotes
        if content_filters.ignore_japanese_quotes and '「' in text and '」' in text:
            if re.search(r'「.*」', text):
                return True
        
        # Check URLs
        if content_filters.ignore_urls:
            url_pattern = r'https?://[^\s]+'
            if re.search(url_pattern, text):
                return True
        
        # Check emails
        if content_filters.ignore_emails:
            email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            if re.search(email_pattern, text):
                return True
        
        # Check numbers only
        if content_filters.ignore_numbers_only:
            if re.match(r'^[\d\s\.,\-\+\(\)%$€¥£]+$', text.strip()):
                return True
        
        return False
    
    def _generate_request_id(self) -> str:
        """Generate unique request ID."""
        import uuid
        return str(uuid.uuid4())
