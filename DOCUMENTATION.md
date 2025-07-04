# Excel Translator App Documentation

## Overview

Excel Translator App is a professional desktop application built with PyQt6 that enables users to translate Excel files using the DeepL API while preserving all original formatting, styles, and formulas.

## Features

### 🎨 Modern UI/UX
- **Dark Theme**: Professional midnight dark theme inspired by VS Code
- **Responsive Design**: Clean, modern interface that adapts to different screen sizes
- **Multi-language Support**: Interface available in English, Japanese, and Vietnamese
- **Progress Tracking**: Real-time progress indicators and detailed logging

### 📊 Excel Processing
- **Format Preservation**: Maintains all original formatting including:
  - Fonts, colors, and styles
  - Merged cells and borders
  - Column widths and row heights
  - Conditional formatting
  - Data validation rules
- **Formula Protection**: Automatically skips formulas and numeric values
- **Multi-sheet Support**: Processes all sheets in a workbook
- **Smart Detection**: Intelligently identifies translatable text content

### 🌐 Translation Features
- **DeepL Integration**: Uses official DeepL API for high-quality translations
- **Batch Processing**: Efficiently processes large files with optimized batching
- **Language Support**: Supports Japanese, Vietnamese, and English
- **Auto-detection**: Can automatically detect source language
- **Error Handling**: Robust error handling with retry mechanisms

### ⚙️ Advanced Features
- **Settings Management**: Persistent settings storage
- **API Key Management**: Secure API key storage and validation
- **Rate Limiting**: Automatic rate limit handling
- **Progress Monitoring**: Real-time progress updates and cancellation support
- **Export Options**: Export translated files with preserved structure

## Installation

### Prerequisites
- Python 3.10 or higher
- DeepL API key (free or paid)

### Quick Setup

1. **Clone or download** the project files
2. **Run the setup script**:
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```
3. **Get your DeepL API key** from [DeepL API](https://www.deepl.com/pro-api)

### Manual Setup

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Create test data** (optional):
   ```bash
   python create_test_data.py
   ```

3. **Run the application**:
   ```bash
   python main.py
   ```

## Usage

### First-time Setup

1. **Launch the application**:
   ```bash
   ./run.sh
   ```

2. **Configure API key**:
   - Click **Settings** in the menu
   - Enter your DeepL API key
   - Click **Save Settings**

3. **Test with sample data**:
   - Use the generated `test_data.xlsx` file
   - Or upload your own Excel file

### Basic Workflow

1. **Select File**:
   - Click "Select File" button
   - Choose your Excel file (.xlsx, .xlsm, .xls)

2. **Choose Languages**:
   - Select source language (Japanese, English, Vietnamese)
   - Select target language

3. **Translate**:
   - Click "Translate" to start processing
   - Monitor progress in real-time
   - Cancel if needed

4. **Export**:
   - Click "Export" when translation is complete
   - Choose output location
   - Save the translated file

### Advanced Features

#### Settings Configuration
- **API Key**: Your DeepL API key
- **App Language**: Interface language
- **Batch Size**: Number of texts processed per API call (1-100)

#### File Processing
- **Smart Text Detection**: Automatically identifies translatable content
- **Formula Preservation**: Skips formulas and numeric values
- **Style Preservation**: Maintains all original formatting

#### Error Handling
- **Retry Mechanism**: Automatic retry on API failures
- **Rate Limiting**: Handles API rate limits gracefully
- **Validation**: Validates files and API responses

## Project Structure

```
excel-translator-app/
├── main.py                 # Application entry point
├── setup.py               # Setup script
├── setup.sh               # Shell setup script
├── run.sh                 # Shell run script
├── requirements.txt       # Python dependencies
├── create_test_data.py    # Test data generator
├── README.md             # Project documentation
├── config/
│   └── settings.json     # Application settings
├── i18n/
│   ├── en.json          # English translations
│   ├── ja.json          # Japanese translations
│   └── vi.json          # Vietnamese translations
├── assets/
│   └── dark_theme.qss   # Dark theme stylesheet
├── translator/
│   ├── __init__.py
│   ├── deepl_client.py  # DeepL API client
│   └── batch_processor.py # Batch processing logic
├── excel/
│   ├── __init__.py
│   ├── excel_reader.py  # Excel file reading
│   ├── excel_writer.py  # Excel file writing
│   └── utils.py         # Excel utilities
└── ui/
    ├── __init__.py
    └── main_window.py   # Main application window
```

## API Integration

### DeepL API Setup

1. **Sign up** at [DeepL API](https://www.deepl.com/pro-api)
2. **Choose a plan**:
   - Free: 500,000 characters/month
   - Pro: Unlimited with better performance
3. **Get your API key** from the dashboard
4. **Enter the key** in the app settings

### Supported Languages

- **Japanese (JA)**: Full support for Hiragana, Katakana, Kanji
- **English (EN)**: American and British English
- **Vietnamese (VI)**: Full Unicode support

### Rate Limits

- **Free Plan**: 5 requests/second
- **Pro Plan**: Higher limits with better reliability

## Technical Details

### Architecture

- **PyQt6**: Modern UI framework
- **OpenPyXL**: Excel file processing
- **DeepL SDK**: Official API integration
- **Threading**: Non-blocking UI with background processing

### Performance Optimizations

- **Batch Processing**: Groups texts for efficient API calls
- **Smart Detection**: Filters out non-translatable content
- **Memory Management**: Efficient handling of large files
- **Progress Tracking**: Real-time updates without blocking

### Error Handling

- **API Errors**: Automatic retry with exponential backoff
- **File Errors**: Comprehensive validation and error messages
- **Network Issues**: Graceful handling of connectivity problems
- **Memory Issues**: Efficient processing of large files

## Troubleshooting

### Common Issues

1. **Import Errors**:
   - Ensure all dependencies are installed: `pip install -r requirements.txt`
   - Check Python version: `python --version` (3.10+ required)

2. **API Errors**:
   - Verify your API key is correct
   - Check your DeepL account usage limits
   - Ensure stable internet connection

3. **File Issues**:
   - Verify Excel file is not corrupted
   - Check file permissions
   - Ensure file is not open in another application

4. **Performance Issues**:
   - Reduce batch size in settings
   - Close other applications to free memory
   - Use smaller files for testing

### Error Messages

- **"Invalid API key"**: Check your DeepL API key
- **"No file selected"**: Select an Excel file first
- **"Translation failed"**: Check API limits and network connection
- **"File export failed"**: Check output directory permissions

## Development

### Adding New Languages

1. **Create translation file**:
   ```json
   // i18n/new_lang.json
   {
     "app_title": "Your Translation",
     // ... other translations
   }
   ```

2. **Update language list**:
   ```python
   # In main_window.py
   self.app_language_combo.addItems(["en", "ja", "vi", "new_lang"])
   ```

### Customizing Themes

1. **Edit stylesheet**:
   ```css
   /* assets/dark_theme.qss */
   QMainWindow {
     background-color: #your-color;
   }
   ```

2. **Create new theme**:
   - Copy `dark_theme.qss` to `new_theme.qss`
   - Update colors and styles
   - Add theme selection in settings

### Contributing

1. **Fork the repository**
2. **Create a feature branch**
3. **Make your changes**
4. **Test thoroughly**
5. **Submit a pull request**

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Create an issue on GitHub
3. Check DeepL API documentation
4. Verify your Python and dependency versions

## Version History

- **v1.0.0**: Initial release with core translation functionality
- **v1.1.0**: Added batch processing and progress tracking
- **v1.2.0**: Enhanced UI and error handling
- **v1.3.0**: Added multi-language support and themes
