"""
PyDocFlow-Studio
A comprehensive Streamlit application for PDF text extraction, EPUB conversion,
file merging, and eBook discovery.
"""
import streamlit as st
import os
import tempfile

# Import utility modules
from utils import pdf_utils
from utils import epub_utils
from utils import file_merge_utils
from utils import ebook_finder_utils


def main():
    """Main application entry point."""
    st.set_page_config(
        page_title="PyDocFlow-Studio",
        page_icon="📚",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Main title
    st.title("📚 PyDocFlow-Studio")
    st.markdown("---")
    
    # Create tabs for different functionalities
    tab1, tab2, tab3, tab4 = st.tabs([
        "📄 PDF to Text",
        "📖 EPUB Converter", 
        "🗂️ File Merger",
        "🔍 eBook Finder"
    ])
    
    with tab1:
        pdf_to_text_ui()
    
    with tab2:
        epub_converter_ui()
    
    with tab3:
        file_merger_ui()
    
    with tab4:
        ebook_finder_ui()
    
    # Sidebar
    render_sidebar()


def render_sidebar():
    """Render application sidebar with information."""
    st.sidebar.title("ℹ️ About")
    st.sidebar.markdown("""
    **PyDocFlow-Studio** provides:
    
    - 📄 **PDF to Text**: Extract text using multiple methods
    - 📖 **EPUB Converter**: Convert EPUB to various formats
    - 🗂️ **File Merger**: Merge multiple files with metadata
    - 🔍 **eBook Finder**: Discover free eBooks online
    """)
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### ⚙️ Settings")
    
    # Tesseract path configuration
    tesseract_path = st.sidebar.text_input(
        "Tesseract Path",
        value="/usr/local/bin/tesseract",
        help="Path to tesseract executable for OCR"
    )
    st.session_state['tesseract_path'] = tesseract_path
    
    st.sidebar.markdown("---")
    st.sidebar.markdown('📖 [GitHub Repository](https://github.com/kunalsuri/)')
    st.sidebar.markdown('Made with ❤️ using Streamlit')


def pdf_to_text_ui():
    """PDF to Text extraction interface."""
    st.header("📄 PDF to Text Converter")
    st.markdown("Extract text from PDF files using different methods")
    
    # Method selection
    col1, col2 = st.columns([2, 1])
    
    with col1:
        method = st.selectbox(
            "Select Extraction Method",
            ["PyMuPDF", "pdfminer.six", "Tesseract OCR"],
            help="Choose the best method based on your PDF type"
        )
    
    with col2:
        st.markdown("### Method Info")
        method_descriptions = {
            "PyMuPDF": "Fast extraction for PDFs with embedded text",
            "pdfminer.six": "Advanced extraction for complex PDFs",
            "Tesseract OCR": "OCR for scanned PDFs and images"
        }
        st.info(method_descriptions[method])
    
    # File upload
    uploaded_file = st.file_uploader("Upload PDF file", type=["pdf"], key="pdf_upload")
    
    if uploaded_file:
        st.success(f"File '{uploaded_file.name}' uploaded successfully")
        
        col1, col2 = st.columns(2)
        
        with col1:
            extract_button = st.button("🚀 Extract Text", type="primary")
        
        if extract_button:
            with st.spinner(f"Extracting text using {method}..."):
                try:
                    extracted_text = None
                    
                    if method == "PyMuPDF":
                        pdf_bytes = uploaded_file.read()
                        extracted_text = pdf_utils.extract_text_pymupdf(pdf_bytes)
                        uploaded_file.seek(0)  # Reset file pointer
                    
                    elif method == "pdfminer.six":
                        # Save temporarily for pdfminer
                        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                            tmp_file.write(uploaded_file.read())
                            tmp_path = tmp_file.name
                        
                        extracted_text = pdf_utils.extract_text_pdfminer_six(tmp_path)
                        os.unlink(tmp_path)
                        uploaded_file.seek(0)
                    
                    elif method == "Tesseract OCR":
                        pdf_bytes = uploaded_file.read()
                        tesseract_path = st.session_state.get('tesseract_path', '/usr/local/bin/tesseract')
                        extracted_text = pdf_utils.extract_text_tesseract(pdf_bytes, tesseract_path)
                        uploaded_file.seek(0)
                    
                    if extracted_text:
                        st.success("✅ Text extraction successful!")
                        
                        # Display extracted text
                        st.subheader("Extracted Text")
                        st.text_area("", extracted_text, height=300, key="extracted_text")
                        
                        # Text verification
                        issues = pdf_utils.verify_text(extracted_text)
                        if issues:
                            with st.expander("⚠️ Text Quality Issues Detected"):
                                for issue in issues:
                                    st.warning(f"• {issue}")
                        else:
                            st.success("✅ No quality issues detected")
                        
                        # Download button
                        pdf_name = os.path.splitext(uploaded_file.name)[0]
                        text_filename = f"{pdf_name}.txt"
                        st.download_button(
                            label=f"💾 Download as {text_filename}",
                            data=extracted_text,
                            file_name=text_filename,
                            mime="text/plain"
                        )
                    else:
                        st.error("❌ No text could be extracted")
                
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
    
    # Text verification tool
    st.markdown("---")
    st.subheader("🔍 Text Verification Tool")
    st.markdown("Upload a text file to check for extraction issues")
    
    text_file = st.file_uploader("Upload text file for verification", type=["txt"], key="text_verify")
    
    if text_file:
        if st.button("Verify Text Quality"):
            try:
                file_text = text_file.read().decode("utf-8")
                issues = pdf_utils.verify_text(file_text)
                
                if issues:
                    st.warning("Issues found:")
                    for issue in issues:
                        st.write(f"• {issue}")
                else:
                    st.success("✅ No issues found in the text!")
            except Exception as e:
                st.error(f"Error verifying text: {str(e)}")


def epub_converter_ui():
    """EPUB conversion interface."""
    st.header("📖 EPUB Converter")
    st.markdown("Convert EPUB files to various formats")
    
    # Conversion type selection
    conversion_type = st.selectbox(
        "Select Conversion Type",
        [
            "EPUB to HTML",
            "EPUB to Clean Text",
            "EPUB to Styled PDF",
            "EPUB to Word (.docx)"
        ]
    )
    
    # File upload
    uploaded_file = st.file_uploader("Upload EPUB file", type=["epub"], key="epub_upload")
    
    if uploaded_file:
        st.success(f"File '{uploaded_file.name}' uploaded successfully")
        
        convert_button = st.button("🔄 Convert", type="primary")
        
        if convert_button:
            with st.spinner("Converting EPUB..."):
                tmp_path = None
                try:
                    # Save temporarily
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.epub') as tmp_file:
                        tmp_file.write(uploaded_file.read())
                        tmp_path = tmp_file.name
                    
                    base_name = os.path.splitext(uploaded_file.name)[0]
                    
                    if conversion_type == "EPUB to HTML":
                        html_content = epub_utils.epub_to_html(tmp_path)
                        st.success("✅ Conversion successful!")
                        st.text_area("HTML Content (preview)", html_content[:1000] + "...", height=200)
                        st.download_button(
                            label="💾 Download HTML",
                            data=html_content,
                            file_name=f"{base_name}.html",
                            mime="text/html"
                        )
                    
                    elif conversion_type == "EPUB to Clean Text":
                        text_content = epub_utils.epub_to_clean_text(tmp_path)
                        st.success("✅ Conversion successful!")
                        st.text_area("Text Content (preview)", text_content[:1000] + "...", height=200)
                        st.download_button(
                            label="💾 Download Text",
                            data=text_content,
                            file_name=f"{base_name}.txt",
                            mime="text/plain"
                        )
                    
                    elif conversion_type == "EPUB to Styled PDF":
                        text_content = epub_utils.epub_to_clean_text(tmp_path)
                        pdf_buffer = epub_utils.text_to_styled_pdf(text_content)
                        st.success("✅ Conversion successful!")
                        st.download_button(
                            label="💾 Download PDF",
                            data=pdf_buffer,
                            file_name=f"{base_name}.pdf",
                            mime="application/pdf"
                        )
                    
                    elif conversion_type == "EPUB to Word (.docx)":
                        text_content = epub_utils.epub_to_clean_text(tmp_path)
                        word_buffer = epub_utils.text_to_word_doc(text_content)
                        st.success("✅ Conversion successful!")
                        st.download_button(
                            label="💾 Download Word Document",
                            data=word_buffer,
                            file_name=f"{base_name}.docx",
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                        )
                    
                except (IOError, OSError, ValueError, RuntimeError) as e:
                    st.error(f"❌ Error: {str(e)}")
                finally:
                    # Cleanup temporary file
                    if tmp_path and os.path.exists(tmp_path):
                        try:
                            os.unlink(tmp_path)
                        except OSError:
                            pass  # File already deleted


def file_merger_ui():
    """File merging interface."""
    st.header("🗂️ File Merger with Metadata")
    st.markdown("Merge multiple files into one with custom metadata")
    
    # Merge mode selection
    merge_mode = st.radio(
        "Select Merge Mode",
        [
            "Merge Text Files (Single Folder)",
            "Merge XML Files (Single Folder)",
            "Merge Files Recursively (Nested Folders)"
        ],
        horizontal=True
    )
    
    st.markdown("---")
    
    # Input fields
    col1, col2 = st.columns(2)
    
    with col1:
        input_folder = st.text_input(
            "Input Folder Path",
            placeholder="/path/to/input/folder",
            help="Folder containing files to merge"
        )
    
    with col2:
        output_folder = st.text_input(
            "Output Folder Path",
            placeholder="/path/to/output/folder",
            help="Folder where merged file will be saved"
        )
    
    # Output filename
    if "Text Files (Single Folder)" in merge_mode:
        default_name = "merged_text_files.txt"
    elif "XML Files" in merge_mode:
        default_name = "merged_xml_files.xml"
    else:
        default_name = "merged_files_recursive.txt"
    
    output_filename = st.text_input("Output Filename", value=default_name)
    
    # Custom metadata
    st.subheader("Custom Metadata")
    default_metadata = file_merge_utils.load_default_metadata()
    custom_metadata = st.text_area(
        "Add custom metadata (optional)",
        value=default_metadata,
        height=150,
        help="This metadata will be added to each merged file"
    )
    
    # Merge button
    if st.button("🔀 Merge Files", type="primary"):
        # Validation
        if not input_folder or not output_folder:
            st.error("❌ Please provide both input and output folder paths")
        elif not os.path.exists(input_folder):
            st.error("❌ Input folder does not exist")
        elif not os.path.exists(output_folder):
            st.error("❌ Output folder does not exist")
        else:
            with st.spinner("Merging files..."):
                try:
                    output_path = os.path.join(output_folder, output_filename)
                    
                    if "Text Files (Single Folder)" in merge_mode:
                        result = file_merge_utils.merge_text_files(
                            input_folder,
                            output_path,
                            custom_metadata
                        )
                    elif "XML Files" in merge_mode:
                        result = file_merge_utils.merge_xml_files(
                            input_folder,
                            output_path,
                            custom_metadata
                        )
                    else:  # Recursive
                        result = file_merge_utils.merge_files_recursive(
                            input_folder,
                            output_path,
                            custom_metadata
                        )
                    
                    st.success(f"✅ {result}")
                    st.balloons()
                    st.info(f"📁 Output file: {output_path}")
                
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")


def ebook_finder_ui():
    """eBook finder interface."""
    st.header("🔍 Free eBook Finder")
    st.markdown("Discover free eBooks organized by subject")
    
    st.info("📚 This tool fetches free eBooks from public domain sources")
    
    url = st.text_input(
        "eBook Source URL",
        value="https://www.gutenberg.org/ebooks/",
        help="URL to fetch eBook listings from"
    )
    
    if st.button("🔍 Search eBooks", type="primary"):
        with st.spinner("Fetching eBooks..."):
            try:
                # Note: The original implementation may need adjustment based on actual site structure
                st.warning("⚠️ Note: Web scraping functionality depends on the target website's structure. The site may have changed since this tool was created.")
                
                books_data = ebook_finder_utils.get_books_by_subject(url)
                
                if books_data:
                    st.success(f"✅ Found {len(books_data)} categories")
                    
                    # Display in expandable sections
                    for subject, books in books_data.items():
                        with st.expander(f"📖 {subject} ({len(books)} books)"):
                            for i, book in enumerate(books, 1):
                                st.write(f"{i}. {book}")
                else:
                    st.warning("No books found. The website structure may have changed.")
                    st.info("💡 Try visiting the URL directly to browse available eBooks.")
            
            except (IOError, OSError, ValueError, RuntimeError) as e:
                st.error(f"❌ Error: {str(e)}")
                st.info("💡 Try visiting the URL directly in your browser to verify it's accessible.")
    
    # Alternative: Manual category browser
    st.markdown("---")
    st.subheader("📚 Popular eBook Sources")
    st.markdown("""
    - [Project Gutenberg](https://www.gutenberg.org/) - Over 70,000 free eBooks
    - [Open Library](https://openlibrary.org/) - Millions of free books
    - [Internet Archive](https://archive.org/details/books) - Digital library of books
    - [ManyBooks](https://manybooks.net/) - Free eBooks in various formats
    - [Feedbooks](https://www.feedbooks.com/publicdomain) - Public domain books
    """)


if __name__ == "__main__":
    main()
