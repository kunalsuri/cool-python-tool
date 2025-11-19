"""
EPUB Utilities Module
Contains core functions for EPUB conversion to various formats.
"""
import os
import ebooklib
from ebooklib import epub
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.units import inch
from io import BytesIO
from bs4 import BeautifulSoup
import textwrap
from docx import Document


def epub_to_html(epub_file_path):
    """
    Convert EPUB to HTML content.
    
    Args:
        epub_file_path: Path to EPUB file
        
    Returns:
        HTML content as string
    """
    if not epub_file_path or not os.path.exists(epub_file_path):
        raise FileNotFoundError(f"EPUB file not found: {epub_file_path}")
    
    try:
        book = epub.read_epub(epub_file_path)
        html_content = []
        for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
            content = item.get_body_content().decode('utf-8')
            html_content.append(content)
        return "\n".join(html_content)
    except (IOError, OSError, UnicodeDecodeError) as e:
        raise IOError(f"EPUB to HTML conversion error: {str(e)}") from e


def epub_to_clean_text(epub_file_path):
    """
    Extract and clean text from EPUB file.
    
    Args:
        epub_file_path: Path to EPUB file
        
    Returns:
        Clean text content as string
    """
    if not epub_file_path or not os.path.exists(epub_file_path):
        raise FileNotFoundError(f"EPUB file not found: {epub_file_path}")
    
    try:
        book = epub.read_epub(epub_file_path)
        text = []
        for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
            content = item.get_body_content().decode('utf-8')
            soup = BeautifulSoup(content, 'html.parser')
            text.append(soup.get_text())
        return "\n".join(text)
    except (IOError, OSError, UnicodeDecodeError) as e:
        raise IOError(f"EPUB to text conversion error: {str(e)}") from e


def text_to_styled_pdf(text, font_path='DejaVuSerif.ttf'):
    """
    Convert text to styled PDF with text wrapping and Unicode support.
    
    Args:
        text: Text content to convert
        font_path: Path to Unicode font file
        
    Returns:
        BytesIO buffer containing PDF
    """
    try:
        buffer = BytesIO()
        
        # Try to register font, use Helvetica as fallback
        try:
            pdfmetrics.registerFont(TTFont('DejaVu', font_path))
            font_name = 'DejaVu'
        except (OSError, IOError, RuntimeError):
            font_name = 'Helvetica'
        
        p = canvas.Canvas(buffer, pagesize=letter)
        _, height = letter
        margin = inch
        y = height - margin

        p.setFont(font_name, 12)

        # Split text into paragraphs
        paragraphs = text.split("\n")

        for paragraph in paragraphs:
            lines = textwrap.wrap(paragraph, width=85)
            for line in lines:
                if y < margin + 20:
                    p.showPage()
                    p.setFont(font_name, 12)
                    y = height - margin
                p.drawString(margin, y, line)
                y -= 15
            y -= 15

        p.save()
        buffer.seek(0)
        return buffer
    except (IOError, OSError, RuntimeError) as e:
        raise RuntimeError(f"Text to PDF conversion error: {str(e)}") from e


def text_to_word_doc(text):
    """
    Convert text to Word document (.docx).
    
    Args:
        text: Text content to convert
        
    Returns:
        BytesIO buffer containing Word document
    """
    try:
        doc = Document()
        paragraphs = text.split("\n")

        for paragraph in paragraphs:
            if paragraph.strip():
                doc.add_paragraph(paragraph.strip())
        
        buffer = BytesIO()
        doc.save(buffer)
        buffer.seek(0)
        return buffer
    except (IOError, OSError) as e:
        raise IOError(f"Text to Word conversion error: {str(e)}") from e
