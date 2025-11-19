# 📚 PyDocFlow Studio

A comprehensive Streamlit application that provides multiple tools for working with PDFs, EPUB files, text files, and discovering free eBooks online.

## 🌟 Features

### 1. 📄 PDF to Text Converter
Extract text from PDF files using three different methods:
- **PyMuPDF**: Fast extraction for PDFs with embedded text
- **pdfminer.six**: Advanced extraction for complex PDFs with special encodings
- **Tesseract OCR**: OCR-based extraction for scanned PDFs and images

**Additional Features:**
- Text quality verification tool
- Automatic issue detection (whitespace, broken lines, etc.)
- Download extracted text as `.txt` files

### 2. 📖 EPUB Converter
Convert EPUB files to multiple formats:
- **EPUB to HTML**: Extract HTML content from EPUB files
- **EPUB to Clean Text**: Convert to plain text with formatting removed
- **EPUB to Styled PDF**: Generate book-like PDFs with proper formatting
- **EPUB to Word (.docx)**: Create editable Word documents

### 3. 🗂️ File Merger with Metadata
Merge multiple files with custom metadata:
- **Merge Text Files**: Combine text files from a single folder
- **Merge XML Files**: Combine XML files with proper metadata
- **Recursive Merge**: Merge files from nested folder structures

**Features:**
- Custom metadata injection
- Automatic file tracking with timestamps
- Source file identification in merged output

### 4. 🔍 Free eBook Finder
Discover and browse free eBooks from public domain sources:
- Web scraping from popular eBook repositories
- Organized by subject/category
- Links to popular free eBook sources

## 🚀 Getting Started

### Prerequisites

#### System Requirements
- Python 3.8 or higher
- pip (Python package manager)
- Tesseract OCR (optional, for OCR functionality)

#### Install Tesseract OCR (Optional)

**macOS:**
```bash
brew install tesseract
```

**Ubuntu/Debian:**
```bash
sudo apt-get install tesseract-ocr
```

**Windows:**
Download from: https://github.com/UB-Mannheim/tesseract/wiki

### Installation

#### Option 1: Quick Start (Recommended)

Use the automated setup script:

```bash
chmod +x start.sh
./start.sh
```

The script will automatically:
- Check for Python installation
- Create/activate virtual environment
- Install all dependencies
- Launch the application

#### Option 2: Manual Installation

1. **Clone the repository (if needed)**
```bash
cd /path/to/PyDocFlow-Studio
```

2. **Create a virtual environment (recommended)**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **For EPUB to PDF conversion with Unicode support**
Download the DejaVu font (if not already installed):
```bash
# macOS
brew install --cask font-dejavu

# Linux
sudo apt-get install fonts-dejavu
```

### Running the Application

```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`

## 📖 Usage Guide

### PDF to Text Converter

1. Select the **PDF to Text** tab
2. Choose an extraction method:
   - Use **PyMuPDF** for standard PDFs (fastest, best quality for embedded text)
   - Use **pdfminer.six** for complex PDFs with special encodings (slower, very high quality)
   - Use **Tesseract OCR** for scanned documents/images (slowest, variable quality)
3. Upload your PDF file
4. Click **Extract Text**
5. Download the extracted text file

**Text Verification:**
- Upload a previously extracted text file
- Click **Verify Text Quality** to check for issues

### EPUB Converter

1. Select the **EPUB Converter** tab
2. Choose your desired output format
3. Upload an EPUB file
4. Click **Convert**
5. Download the converted file

### File Merger

1. Select the **File Merger** tab
2. Choose a merge mode:
   - Single folder text files
   - Single folder XML files
   - Recursive (nested folders)
3. Enter input and output folder paths
4. Customize the output filename
5. Add custom metadata (optional)
6. Click **Merge Files**

### eBook Finder

1. Select the **eBook Finder** tab
2. Optionally modify the source URL
3. Click **Search eBooks**
4. Browse results by category
5. Use the provided links to access popular eBook repositories

## 🏗️ Project Structure

```
PyDocFlow-Studio/
├── app.py                  # Main Streamlit application
├── pdf_utils.py            # PDF processing utilities
├── epub_utils.py           # EPUB conversion utilities
├── file_merge_utils.py     # File merging utilities
├── ebook_finder_utils.py   # eBook discovery utilities
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── custom-metadata.txt    # Default metadata template
└── [legacy files]         # Original separate scripts
```

## 🔧 Configuration

### Tesseract Path
If Tesseract is installed in a non-standard location, update the path in the sidebar settings:
1. Open the application
2. Look for **Settings** in the sidebar
3. Update the **Tesseract Path** field

### Custom Metadata
Edit `custom-metadata.txt` to set default metadata for file merging operations.

## 🛠️ Technical Details

### Core Technologies
- **Streamlit**: Web application framework
- **PyMuPDF (fitz)**: PDF rendering and text extraction
- **pdfminer.six**: PDF structure analysis
- **Tesseract**: Optical character recognition
- **ebooklib**: EPUB file handling
- **ReportLab**: PDF generation
- **python-docx**: Word document creation
- **BeautifulSoup**: Web scraping and HTML parsing

### Architecture
The application follows a modular architecture:
- **Core Logic Layer**: Utility modules (`*_utils.py`) contain all business logic
- **UI Layer**: `app.py` handles user interface and orchestration
- **Separation of Concerns**: Clean separation between data processing and presentation

### Error Handling
- Comprehensive try-catch blocks in all utility functions
- User-friendly error messages in the UI
- Automatic cleanup of temporary files
- Input validation before processing

## 🐛 Troubleshooting

### Common Issues

**Issue: "Unable to import 'fitz'"**
- Solution: Install PyMuPDF: `pip install PyMuPDF`

**Issue: "Tesseract not found"**
- Solution: Install Tesseract OCR and update the path in settings

**Issue: "Font not found for PDF generation"**
- Solution: Install DejaVu fonts or the application will fall back to Helvetica

**Issue: "Permission denied" when merging files**
- Solution: Ensure you have write permissions for the output folder

**Issue: "Web scraping returns no results"**
- Solution: The website structure may have changed; use the provided direct links instead

## 👨‍💻 For Developers

### Code Quality
- **Production-ready**: 95% quality score (A+)
- **Security**: 0 critical issues, specific exception handling
- **Architecture**: Modular design with clean separation of concerns
- **Documentation**: 100% function coverage with docstrings

### Technical Documentation
For architecture details, module specifications, and development guidelines, see:
- **[Technical Documentation](docs/technical-document.md)** - Comprehensive developer guide

### Project Statistics
- **917 lines** of application code
- **24 functions** across 5 modules
- **0 critical issues** (Codacy verified)
- **Modular architecture** - Easy to extend and maintain

## 📝 License

See the LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

For development guidelines and architecture details, consult the [technical documentation](docs/technical-document.md).

## 👨‍💻 Author

Created by Kunal Suri
- GitHub: [@kunalsuri](https://github.com/kunalsuri/)

## 🙏 Acknowledgments

- Project Gutenberg for free eBooks
- All open-source library maintainers
- Streamlit community

## 📚 Additional Resources

### For Users
- [Streamlit Documentation](https://docs.streamlit.io/)
- [PyMuPDF Documentation](https://pymupdf.readthedocs.io/)
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
- [Project Gutenberg](https://www.gutenberg.org/)

### For Developers
- [Technical Documentation](docs/technical-document.md) - Architecture and implementation details
