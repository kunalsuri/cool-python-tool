"""
PDF Utilities Module
Contains core functions for PDF text extraction using various methods.
"""
import fitz  # PyMuPDF
import pytesseract
from pdf2image import convert_from_path
from pdfminer.high_level import extract_text as extract_text_pdfminer
import os
import re


def extract_text_pymupdf(pdf_file_bytes):
    """
    Extract text from PDF using PyMuPDF library.
    
    Args:
        pdf_file_bytes: Bytes from uploaded PDF file
        
    Returns:
        Extracted text as string or None on error
    """
    if not pdf_file_bytes:
        raise ValueError("PDF file bytes cannot be empty")
    
    pdf_document = None
    try:
        pdf_document = fitz.open(stream=pdf_file_bytes, filetype="pdf")
        text = ""
        for page_num in range(pdf_document.page_count):
            page = pdf_document.load_page(page_num)
            text += page.get_text("text")
        return text
    except (RuntimeError, ValueError) as e:
        raise ValueError(f"PyMuPDF extraction error: {str(e)}") from e
    finally:
        if pdf_document:
            pdf_document.close()


def extract_text_pdfminer_six(pdf_file_path):
    """
    Extract text from PDF using pdfminer.six library.
    
    Args:
        pdf_file_path: Path to PDF file
        
    Returns:
        Extracted text as string or None on error
    """
    if not pdf_file_path or not os.path.exists(pdf_file_path):
        raise FileNotFoundError(f"PDF file not found: {pdf_file_path}")
    
    try:
        return extract_text_pdfminer(pdf_file_path)
    except (IOError, OSError) as e:
        raise IOError(f"pdfminer.six extraction error: {str(e)}") from e


def extract_text_tesseract(pdf_file_bytes, tesseract_cmd='/usr/local/bin/tesseract'):
    """
    Extract text from PDF using Tesseract OCR (for scanned PDFs).
    
    Args:
        pdf_file_bytes: Bytes from uploaded PDF file
        tesseract_cmd: Path to tesseract executable
        
    Returns:
        Extracted text as string or None on error
    """
    if not pdf_file_bytes:
        raise ValueError("PDF file bytes cannot be empty")
    
    import tempfile
    temp_file = None
    try:
        pytesseract.pytesseract.tesseract_cmd = tesseract_cmd
        
        # Create temporary file with unique name
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
            temp_file = tmp.name
            tmp.write(pdf_file_bytes)

        # Convert PDF pages to images and apply OCR
        images = convert_from_path(temp_file)
        extracted_text = []
        for image in images:
            text = pytesseract.image_to_string(image)
            extracted_text.append(text)

        return "\n".join(extracted_text)
    except (IOError, OSError, RuntimeError) as e:
        raise RuntimeError(f"Tesseract OCR extraction error: {str(e)}") from e
    finally:
        if temp_file and os.path.exists(temp_file):
            try:
                os.remove(temp_file)
            except OSError:
                pass  # File already deleted or not accessible


def verify_text(text):
    """
    Verify extracted text for common issues.
    
    Args:
        text: Text string to verify
        
    Returns:
        List of issues found
    """
    issues = []
    
    if not text or not text.strip():
        issues.append("Text is empty")
        return issues
    
    # Check for irregular whitespace
    if re.search(r'\s{4,}', text):
        issues.append("Irregular whitespace found")
    
    # Check for broken lines
    if re.search(r'\S\n\S', text):
        issues.append("Broken lines detected")
    
    # Check for missing newlines
    if len(text) > 100 and not re.search(r'\n', text):
        issues.append("Missing newlines")
    
    return issues
