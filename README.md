# cool-python-tool

A collection of Python utilities for video downloading, document processing, and AI/ML version checking.

## Features

### PyDocFlow-Studio

- **PDF to Text Extraction**: Extract text from PDF files using multiple engines
- **EPUB Converter**: Convert documents to EPUB format
- **File Merger**: Merge multiple files into a single document
- **eBook Finder**: Search and discover eBooks online

### Py-YT-Downloader

- Download YouTube videos in highest resolution
- Extract audio as MP3 from YouTube videos
- Built with Streamlit for easy web interface

### Py-Utils-Generic

- **PyTorch Version Finder**: Check installed versions of NumPy, PyTorch, TensorFlow, and CUDA availability

## Tech Stack

- **Python 3.x**
- **Streamlit**: Web UI framework
- **PyTorch**: Deep learning framework
- **TensorFlow**: Machine learning framework
- **PyMuPDF, pdfminer.six**: PDF processing
- **ebooklib**: EPUB handling
- **BeautifulSoup4**: Web scraping
- **pytube/pytubefix**: YouTube video downloading

## Installation

Clone the repository:

```bash
git clone https://github.com/kunalsuri/cool-python-tool.git
cd cool-python-tool
```

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # On macOS/Linux
# .venv\Scripts\activate   # On Windows
```

Install dependencies for specific tools:

**For PyDocFlow-Studio:**

```bash
cd PyDocFlow-Studio
pip install -r requirements.txt
```

**For Py-YT-Downloader:**

```bash
cd Py-YT-Downloader
pip install -r requirements.txt
```

**For Py-Utils-Generic:**

```bash
pip install numpy torch tensorflow
```

## Usage

### Run PyDocFlow-Studio

```bash
cd PyDocFlow-Studio
streamlit run app.py
```

Navigate to the web interface to access:

- PDF to Text conversion
- EPUB creation
- File merging
- eBook search

### Run Py-YT-Downloader

```bash
cd Py-YT-Downloader
python run_app.py
```

Enter a YouTube URL and choose to download video or extract MP3 audio.

### Run Py-Utils-Generic

```bash
cd Py-Utils-Generic
python py-torch-version-finder.py
```

Check installed versions of ML/AI libraries and CUDA availability.

## Project Structure

```plaintext
cool-python-tool/
├── LICENSE
├── README.md
├── Py-Utils-Generic/
│   ├── Emoji-Cheat-Sheet-README.md
│   └── py-torch-version-finder.py
├── Py-YT-Downloader/
│   ├── LICENSE
│   ├── README.md
│   ├── requirements.txt
│   ├── run_app.py
│   └── youtube_downloader.py
└── PyDocFlow-Studio/
    ├── app.py
    ├── custom-metadata.txt
    ├── LICENSE
    ├── README.md
    ├── requirements.txt
    ├── start.sh
    ├── template-metadata.txt
    ├── docs/
    │   ├── codebase-audit-report.md
    │   └── technical-document.md
    ├── original-scripts/
    │   ├── def_merge_files.py
    │   ├── epub_convertor.py
    │   ├── merge_file_main.py
    │   ├── online_ebook_finder_02.py
    │   └── py_pdf_to_text.py
    └── utils/
        ├── __init__.py
        ├── ebook_finder_utils.py
        ├── epub_utils.py
        ├── file_merge_utils.py
        └── pdf_utils.py
```

## License

MIT License - see LICENSE file for details.
