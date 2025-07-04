from typing import List, Tuple, Optional, Callable, Dict, Any
import threading
import time
import logging
from .deepl_client import DeepLClient

class BatchProcessor:
    """Handles batch processing of translations with progress tracking."""
    
    def __init__(self, deepl_client: DeepLClient, batch_size: int = 50, max_retries: int = 3):
        """Initialize batch processor.
        
        Args:
            deepl_client: DeepL client instance
            batch_size: Default batch size (will be overridden by auto-calculation)
            max_retries: Maximum number of retry attempts
        """
        self.deepl_client = deepl_client
        self.default_batch_size = batch_size
        self.batch_size = batch_size
        self.max_retries = max_retries
        self.logger = logging.getLogger(__name__)
        self.cancel_requested = False
    
    def process_texts(self, 
                     texts: List[str], 
                     target_lang: str, 
                     source_lang: Optional[str] = None,
                     progress_callback: Optional[Callable[[int, int], None]] = None) -> List[str]:
        """Process multiple texts with batch translation.
        
        Args:
            texts: List of texts to translate
            target_lang: Target language code
            source_lang: Source language code (optional)
            progress_callback: Callback function for progress updates (current, total)
            
        Returns:
            List of translated texts
        """
        if not texts:
            return []
        
        self.cancel_requested = False
        total_texts = len(texts)
        translated_texts = [''] * total_texts
        processed_count = 0
        
        # Process in batches
        for batch_start in range(0, total_texts, self.batch_size):
            if self.cancel_requested:
                break
            
            batch_end = min(batch_start + self.batch_size, total_texts)
            batch_texts = texts[batch_start:batch_end]
            
            # Translate batch with retries
            batch_results = self._translate_batch_with_retries(
                batch_texts, target_lang, source_lang
            )
            
            # Store results
            for i, result in enumerate(batch_results):
                translated_texts[batch_start + i] = result
            
            processed_count += len(batch_texts)
            
            # Update progress
            if progress_callback:
                progress_callback(processed_count, total_texts)
            
            # Small delay to avoid overwhelming the API
            if batch_end < total_texts:
                time.sleep(0.1)
        
        return translated_texts
    
    def _translate_batch_with_retries(self, 
                                    texts: List[str], 
                                    target_lang: str, 
                                    source_lang: Optional[str] = None) -> List[str]:
        """Translate a batch of texts with retry logic.
        
        Args:
            texts: List of texts to translate
            target_lang: Target language code
            source_lang: Source language code (optional)
            
        Returns:
            List of translated texts
        """
        last_error = None
        
        for attempt in range(self.max_retries):
            try:
                if self.cancel_requested:
                    return texts  # Return original texts if cancelled
                
                return self.deepl_client.translate_batch(texts, target_lang, source_lang)
                
            except Exception as e:
                last_error = e
                self.logger.warning(f"Translation attempt {attempt + 1} failed: {str(e)}")
                
                if attempt < self.max_retries - 1:
                    # Wait before retrying (exponential backoff)
                    wait_time = (2 ** attempt) * 1.0
                    time.sleep(wait_time)
                    
                    # Check for rate limit and wait longer if needed
                    if "rate limit" in str(e).lower():
                        self.deepl_client.wait_for_rate_limit(5.0)
        
        # If all retries failed, log error and return original texts
        self.logger.error(f"All translation attempts failed: {str(last_error)}")
        return texts
    
    def cancel(self):
        """Cancel the current batch processing."""
        self.cancel_requested = True
        self.logger.info("Batch processing cancellation requested")
    
    def is_cancelled(self) -> bool:
        """Check if processing has been cancelled."""
        return self.cancel_requested
    
    def set_optimal_batch_size(self, total_texts: int, avg_text_length: float = 0, file_size_mb: float = 0):
        """Set optimal batch size based on file characteristics.
        
        Args:
            total_texts: Total number of texts to translate
            avg_text_length: Average length of texts (characters)
            file_size_mb: File size in MB
        """
        from excel.utils import calculate_optimal_batch_size
        
        optimal_size = calculate_optimal_batch_size(total_texts, avg_text_length, file_size_mb)
        self.batch_size = optimal_size
        
        self.logger.info(f"Auto-calculated optimal batch size: {optimal_size} for {total_texts} texts")
        
        return optimal_size
    
    def get_current_batch_size(self) -> int:
        """Get the current batch size being used."""
        return self.batch_size


class TranslationTask:
    """Represents a translation task with progress tracking."""
    
    def __init__(self, 
                 sheet_name: str,
                 texts: List[str],
                 cell_positions: List[Tuple[int, int]],
                 target_lang: str,
                 source_lang: Optional[str] = None):
        """Initialize translation task.
        
        Args:
            sheet_name: Name of the Excel sheet
            texts: List of texts to translate
            cell_positions: List of (row, col) positions for each text
            target_lang: Target language code
            source_lang: Source language code (optional)
        """
        self.sheet_name = sheet_name
        self.texts = texts
        self.cell_positions = cell_positions
        self.target_lang = target_lang
        self.source_lang = source_lang
        self.translated_texts = []
        self.status = "pending"  # pending, processing, completed, failed
        self.progress = 0
        self.error = None
    
    def update_progress(self, current: int, total: int):
        """Update task progress."""
        self.progress = int((current / total) * 100) if total > 0 else 0
    
    def mark_completed(self, translated_texts: List[str]):
        """Mark task as completed."""
        self.translated_texts = translated_texts
        self.status = "completed"
        self.progress = 100
    
    def mark_failed(self, error: str):
        """Mark task as failed."""
        self.error = error
        self.status = "failed"


class TranslationManager:
    """Manages multiple translation tasks with threading support."""
    
    def __init__(self, deepl_client: DeepLClient, batch_size: int = 50):
        """Initialize translation manager.
        
        Args:
            deepl_client: DeepL client instance
            batch_size: Batch size for processing
        """
        self.deepl_client = deepl_client
        self.batch_processor = BatchProcessor(deepl_client, batch_size)
        self.tasks = []
        self.current_task = None
        self.thread = None
        self.logger = logging.getLogger(__name__)
    
    def add_task(self, task: TranslationTask):
        """Add a translation task."""
        self.tasks.append(task)
    
    def start_processing(self, 
                        progress_callback: Optional[Callable[[str, int], None]] = None,
                        completion_callback: Optional[Callable[[bool], None]] = None):
        """Start processing all tasks in a separate thread.
        
        Args:
            progress_callback: Callback for progress updates (sheet_name, progress)
            completion_callback: Callback when all tasks are completed (success)
        """
        if self.thread and self.thread.is_alive():
            self.logger.warning("Translation is already in progress")
            return
        
        self.thread = threading.Thread(
            target=self._process_tasks,
            args=(progress_callback, completion_callback)
        )
        self.thread.daemon = True
        self.thread.start()
    
    def _process_tasks(self, 
                      progress_callback: Optional[Callable[[str, int], None]] = None,
                      completion_callback: Optional[Callable[[bool], None]] = None):
        """Process all tasks sequentially."""
        success = True
        
        for task in self.tasks:
            if self.batch_processor.is_cancelled():
                break
            
            self.current_task = task
            task.status = "processing"
            
            try:
                # Update progress callback
                def task_progress(current, total):
                    task.update_progress(current, total)
                    if progress_callback:
                        progress_callback(task.sheet_name, task.progress)
                
                # Process translation
                translated_texts = self.batch_processor.process_texts(
                    task.texts,
                    task.target_lang,
                    task.source_lang,
                    task_progress
                )
                
                task.mark_completed(translated_texts)
                
            except Exception as e:
                error_msg = f"Failed to translate sheet '{task.sheet_name}': {str(e)}"
                task.mark_failed(error_msg)
                self.logger.error(error_msg)
                success = False
        
        self.current_task = None
        
        if completion_callback:
            completion_callback(success and not self.batch_processor.is_cancelled())
    
    def cancel_processing(self):
        """Cancel all processing."""
        self.batch_processor.cancel()
        if self.current_task:
            self.current_task.status = "cancelled"
    
    def get_overall_progress(self) -> int:
        """Get overall progress across all tasks."""
        if not self.tasks:
            return 0
        
        total_progress = sum(task.progress for task in self.tasks)
        return int(total_progress / len(self.tasks))
    
    def clear_tasks(self):
        """Clear all tasks."""
        self.tasks.clear()
        self.current_task = None
