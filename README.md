# 📊 Excel Translator App

A **modern desktop application** built with **PyQt6** and **DeepL API** that enables users to translate Excel files while preserving all original formatting, styles, formulas, and structure.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![PyQt6](https://img.shields.io/badge/PyQt6-6.5+-green.svg)
![DeepL](https://img.shields.io/badge/DeepL-API-orange.svg)

## 🌟 Features

### 🎨 **Modern UI/UX**
- **Dark Theme**: Professional midnight dark theme inspired by VS Code
- **Responsive Design**: Clean, modern interface that adapts to different screen sizes
- **Multi-language Support**: Interface available in English, Japanese, and Vietnamese
- **Progress Tracking**: Real-time progress indicators and detailed logging

### 📊 **Excel Processing**
- **Format Preservation**: Maintains all original formatting including:
  - Fonts, colors, and styles
  - Merged cells and borders
  - Column widths and row heights
  - Conditional formatting
  - Data validation rules
- **Formula Protection**: Automatically skips formulas and numeric values
- **Multi-sheet Support**: Processes all sheets in a workbook
- **Smart Detection**: Intelligently identifies translatable text content

### 🌐 **Translation Features**
- **DeepL Integration**: Uses official DeepL API for high-quality translations
- **Batch Processing**: Efficiently processes large files with optimized batching
- **Language Support**: Supports Japanese, Vietnamese, and English
- **Auto-detection**: Can automatically detect source language
- **Error Handling**: Robust error handling with retry mechanisms

### ⚙️ **Advanced Features**
- **Settings Management**: Persistent settings storage
- **API Key Management**: Secure API key storage and validation
- **Rate Limiting**: Automatic rate limit handling
- **Progress Monitoring**: Real-time progress updates and cancellation support
- **Export Options**: Export translated files with preserved structure

## 🚀 Quick Start

### Prerequisites
- **Python 3.10+**
- **DeepL API key** (free or paid) from [DeepL API](https://www.deepl.com/pro-api)

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd excel-translator-app
   ```

2. **Run the setup script**:
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

3. **Or manually set up**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\\Scripts\\activate
   pip install -r requirements.txt
   ```

### Running the Application

**Quick start**:
```bash
./run.sh
```

**Or manually**:
```bash
source venv/bin/activate
python main.py
```

## 📖 Usage Guide

### First-time Setup

1. **Launch the application** using `./run.sh`
2. **Configure API key**:
   - Click **Settings** in the menu
   - Enter your DeepL API key
   - Choose your preferred app language
   - Click **Save Settings**
3. **Test with sample data**: Use the generated `test_data.xlsx` file

### Basic Workflow

1. **Select File**: Click "Select File" and choose your Excel file (.xlsx, .xlsm, .xls)
2. **Choose Languages**: Select source and target languages
3. **Translate**: Click "Translate" to start processing
4. **Monitor Progress**: Watch real-time progress and logs
5. **Export**: Click "Export" when translation is complete

### Advanced Usage

#### Language Support
- **Japanese (JA)**: Full support for Hiragana, Katakana, Kanji
- **English (EN)**: American and British English
- **Vietnamese (VI)**: Full Unicode support

#### File Processing
- **Smart Text Detection**: Automatically identifies translatable content
- **Formula Preservation**: Skips formulas and numeric values
- **Style Preservation**: Maintains all original formatting

## 🏗️ Architecture

### Project Structure
```
excel-translator-app/
├── main.py                 # Application entry point
├── setup.py               # Setup script
├── requirements.txt       # Python dependencies
├── config/
│   └── settings.json     # Application settings
├── i18n/
│   ├── en.json          # English translations
│   ├── ja.json          # Japanese translations
│   └── vi.json          # Vietnamese translations
├── assets/
│   └── dark_theme.qss   # Dark theme stylesheet
├── translator/
│   ├── deepl_client.py  # DeepL API integration
│   └── batch_processor.py # Batch processing logic
├── excel/
│   ├── excel_reader.py  # Excel file reading
│   ├── excel_writer.py  # Excel file writing
│   └── utils.py         # Excel utilities
└── ui/
    └── main_window.py   # Main application window
```

### Technology Stack
- **Language**: Python 3.10+
- **UI Framework**: PyQt6
- **Excel Processing**: OpenPyXL
- **Translation**: DeepL Official Python SDK
- **Styling**: Qt Style Sheets (QSS)
- **Internationalization**: JSON-based i18n

## ⚙️ Configuration

### Settings File
The application stores settings in `config/settings.json`:

```json
{
  "api_key": "your-deepl-api-key",
  "app_language": "en",
  "theme": "dark",
  "batch_size": 50,
  "max_retries": 3,
  "last_source_lang": "ja",
  "last_target_lang": "en"
}
```

### Environment Variables
You can also set the DeepL API key via environment variable:
```bash
export DEEPL_API_KEY="your-api-key"
```

## 🔧 Development

### Running Tests
```bash
source venv/bin/activate
pytest tests/
```

### Building Executable
```bash
source venv/bin/activate
pyinstaller --windowed --onefile main.py
```

### Adding New Languages

1. **Create translation file**:
   ```json
   // i18n/new_lang.json
   {
     "app_title": "Your Translation",
     // ... other translations
   }
   ```

2. **Update language list** in `main_window.py`

### Customizing Themes

1. **Edit stylesheet**: Modify `assets/dark_theme.qss`
2. **Create new theme**: Copy and customize the stylesheet
3. **Add theme selection** in settings dialog

## 🐛 Troubleshooting

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

## 📊 Performance

### Optimization Features
- **Batch Processing**: Groups texts for efficient API calls
- **Smart Detection**: Filters out non-translatable content
- **Memory Management**: Efficient handling of large files
- **Progress Tracking**: Real-time updates without blocking UI

### Benchmarks
- **Small files** (< 100 cells): ~5-10 seconds
- **Medium files** (100-1000 cells): ~30-60 seconds
- **Large files** (1000+ cells): ~2-5 minutes

## 🤝 Contributing

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/new-feature`
3. **Make your changes**
4. **Test thoroughly**
5. **Submit a pull request**

### Development Guidelines
- Follow PEP 8 style guidelines
- Add tests for new features
- Update documentation
- Test on multiple platforms

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **DeepL** for providing excellent translation API
- **Qt Company** for the PyQt6 framework
- **OpenPyXL** team for Excel file processing
- **VS Code** for UI/UX inspiration

## 📞 Support

For issues and questions:
1. Check the troubleshooting section above
2. Create an issue on GitHub
3. Check [DeepL API documentation](https://www.deepl.com/docs-api)
4. Verify your Python and dependency versions

## 🔄 Version History

- **v1.0.0**: Initial release with core translation functionality
  - Modern dark theme UI
  - Multi-language support (EN, JA, VI)
  - DeepL API integration
  - Excel format preservation
  - Batch processing with progress tracking
  - Comprehensive error handling

---

**Made with ❤️ by the Excel Translator Team**
