from typing import List, Dict, Any, Optional, Tuple
import re
import logging

def is_text_cell(value: Any) -> bool:
    """Check if a cell value contains translatable text.
    
    Args:
        value: Cell value to check
        
    Returns:
        True if the value contains translatable text
    """
    if not isinstance(value, str):
        return False
    
    # Skip empty or whitespace-only strings
    if not value.strip():
        return False
    
    # Skip if it's purely numeric
    if value.strip().replace('.', '').replace(',', '').replace('-', '').isdigit():
        return False
    
    # Skip if it's a formula (starts with =)
    if value.strip().startswith('='):
        return False
    
    return True

def detect_language(text: str) -> str:
    """Detect the language of a text string.
    
    Args:
        text: Text to analyze
        
    Returns:
        Language code (ja, en, vi, or unknown)
    """
    if not text:
        return "unknown"
    
    # Japanese detection (Hiragana, Katakana, Kanji)
    japanese_chars = re.findall(r'[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FAF]', text)
    if len(japanese_chars) > len(text) * 0.3:
        return "ja"
    
    # Vietnamese detection (Vietnamese-specific characters)
    vietnamese_chars = re.findall(r'[àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]', text.lower())
    if len(vietnamese_chars) > 0:
        return "vi"
    
    # Default to English if no specific patterns found
    return "en"

def clean_text_for_translation(text: str) -> str:
    """Clean text for better translation quality.
    
    Args:
        text: Text to clean
        
    Returns:
        Cleaned text
    """
    if not text:
        return text
    
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Strip leading/trailing whitespace
    text = text.strip()
    
    return text

def split_long_text(text: str, max_length: int = 1000) -> List[str]:
    """Split long text into smaller chunks for translation.
    
    Args:
        text: Text to split
        max_length: Maximum length per chunk
        
    Returns:
        List of text chunks
    """
    if len(text) <= max_length:
        return [text]
    
    chunks = []
    current_chunk = ""
    
    # Split by sentences first
    sentences = re.split(r'[.!?]', text)
    
    for sentence in sentences:
        if len(current_chunk) + len(sentence) + 1 <= max_length:
            current_chunk += sentence + "."
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = sentence + "."
    
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    return chunks

def format_cell_address(row: int, col: int) -> str:
    """Convert row and column numbers to Excel cell address.
    
    Args:
        row: Row number (1-based)
        col: Column number (1-based)
        
    Returns:
        Excel cell address (e.g., 'A1', 'B2')
    """
    def col_to_letter(col_num):
        """Convert column number to letter."""
        result = ""
        while col_num > 0:
            col_num -= 1
            result = chr(col_num % 26 + ord('A')) + result
            col_num //= 26
        return result
    
    return f"{col_to_letter(col)}{row}"

def validate_language_code(lang_code: str) -> bool:
    """Validate if a language code is supported.
    
    Args:
        lang_code: Language code to validate
        
    Returns:
        True if the language code is supported
    """
    supported_codes = {
        'en', 'ja', 'vi', 'zh', 'ko', 'fr', 'de', 'es', 'it', 'pt', 'ru', 'ar'
    }
    return lang_code.lower() in supported_codes

def get_file_size_mb(file_path: str) -> float:
    """Get file size in megabytes.
    
    Args:
        file_path: Path to the file
        
    Returns:
        File size in MB
    """
    try:
        import os
        size_bytes = os.path.getsize(file_path)
        return size_bytes / (1024 * 1024)
    except Exception:
        return 0.0

def estimate_translation_time(text_count: int, batch_size: int = 50) -> int:
    """Estimate translation time in seconds.
    
    Args:
        text_count: Number of texts to translate
        batch_size: Batch size for processing
        
    Returns:
        Estimated time in seconds
    """
    if text_count == 0:
        return 0
    
    # Estimate based on API call time and rate limits
    batches = (text_count + batch_size - 1) // batch_size
    time_per_batch = 2  # seconds
    
    return batches * time_per_batch

def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe file operations.
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized filename
    """
    # Remove invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    
    # Remove leading/trailing dots and spaces
    filename = filename.strip('. ')
    
    # Ensure it's not empty
    if not filename:
        filename = "translated_file"
    
    return filename

def get_language_display_name(lang_code: str) -> str:
    """Get display name for language code.
    
    Args:
        lang_code: Language code
        
    Returns:
        Display name for the language
    """
    language_names = {
        'en': 'English',
        'ja': 'Japanese',
        'vi': 'Vietnamese',
        'zh': 'Chinese',
        'ko': 'Korean',
        'fr': 'French',
        'de': 'German',
        'es': 'Spanish',
        'it': 'Italian',
        'pt': 'Portuguese',
        'ru': 'Russian',
        'ar': 'Arabic'
    }
    
    return language_names.get(lang_code.lower(), lang_code.upper())

def create_progress_message(current: int, total: int, item_name: str = "items") -> str:
    """Create a progress message.
    
    Args:
        current: Current progress
        total: Total items
        item_name: Name of the items being processed
        
    Returns:
        Progress message string
    """
    if total == 0:
        return f"Processing {item_name}..."
    
    percentage = int((current / total) * 100)
    return f"Processing {item_name}: {current}/{total} ({percentage}%)"

class ExcelUtils:
    """Utility class for Excel-related operations."""
    
    @staticmethod
    def get_safe_sheet_name(name: str) -> str:
        """Get a safe sheet name for Excel.
        
        Args:
            name: Original sheet name
            
        Returns:
            Safe sheet name
        """
        # Excel sheet name restrictions
        invalid_chars = ['\\', '/', '?', '*', '[', ']', ':']
        safe_name = name
        
        for char in invalid_chars:
            safe_name = safe_name.replace(char, '_')
        
        # Limit length to 31 characters
        if len(safe_name) > 31:
            safe_name = safe_name[:31]
        
        return safe_name
    
    @staticmethod
    def is_valid_excel_file(file_path: str) -> bool:
        """Check if a file is a valid Excel file.
        
        Args:
            file_path: Path to the file
            
        Returns:
            True if the file is a valid Excel file
        """
        try:
            import os
            if not os.path.exists(file_path):
                return False
            
            # Check file extension
            valid_extensions = ['.xlsx', '.xlsm', '.xls']
            _, ext = os.path.splitext(file_path)
            
            return ext.lower() in valid_extensions
        except Exception:
            return False
    
    @staticmethod
    def calculate_optimal_batch_size(total_texts: int, avg_text_length: float = 0, file_size_mb: float = 0) -> int:
        """Calculate optimal batch size based on file characteristics.
        
        Args:
            total_texts: Total number of texts to translate
            avg_text_length: Average length of texts (characters)
            file_size_mb: File size in MB
            
        Returns:
            Optimal batch size
        """
        # Base batch size
        base_batch_size = 50
        
        # Adjust based on total number of texts
        if total_texts < 100:
            # Small files - use smaller batches for better responsiveness
            text_factor = 0.6
        elif total_texts < 500:
            # Medium files - use standard batches
            text_factor = 1.0
        elif total_texts < 1000:
            # Large files - use larger batches for efficiency
            text_factor = 1.5
        else:
            # Very large files - use large batches
            text_factor = 2.0
        
        # Adjust based on average text length
        if avg_text_length > 0:
            if avg_text_length < 50:
                # Short texts - can handle more per batch
                length_factor = 1.2
            elif avg_text_length < 200:
                # Medium texts - standard batch size
                length_factor = 1.0
            else:
                # Long texts - use smaller batches to avoid API limits
                length_factor = 0.7
        else:
            length_factor = 1.0
        
        # Adjust based on file size
        if file_size_mb > 0:
            if file_size_mb < 1:
                # Small files
                size_factor = 0.8
            elif file_size_mb < 5:
                # Medium files
                size_factor = 1.0
            else:
                # Large files
                size_factor = 1.3
        else:
            size_factor = 1.0
        
        # Calculate optimal batch size
        optimal_size = int(base_batch_size * text_factor * length_factor * size_factor)
        
        # Ensure batch size is within reasonable bounds
        optimal_size = max(10, min(optimal_size, 200))  # Between 10 and 200
        
        return optimal_size

    @staticmethod
    def analyze_file_characteristics(file_path: str, sheet_info: Dict[str, Dict]) -> Dict[str, Any]:
        """Analyze file characteristics to determine optimal processing parameters.
        
        Args:
            file_path: Path to the Excel file
            sheet_info: Sheet information dictionary
            
        Returns:
            Dictionary with file characteristics
        """
        total_texts = sum(info.get('text_cells', 0) for info in sheet_info.values())
        file_size_mb = get_file_size_mb(file_path)
        
        # Calculate average text length (estimation)
        # For now, we'll use a simple heuristic based on file size and text count
        if total_texts > 0:
            estimated_avg_length = (file_size_mb * 1024 * 1024 * 0.7) / total_texts  # Rough estimate
            estimated_avg_length = max(10, min(estimated_avg_length, 1000))  # Reasonable bounds
        else:
            estimated_avg_length = 50  # Default
        
        optimal_batch_size = ExcelUtils.calculate_optimal_batch_size(
            total_texts, 
            estimated_avg_length, 
            file_size_mb
        )
        
        return {
            'total_texts': total_texts,
            'file_size_mb': file_size_mb,
            'estimated_avg_length': estimated_avg_length,
            'optimal_batch_size': optimal_batch_size,
            'complexity': 'simple' if total_texts < 100 else 'medium' if total_texts < 500 else 'complex'
        }
