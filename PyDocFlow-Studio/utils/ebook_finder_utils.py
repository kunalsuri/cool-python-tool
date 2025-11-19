"""
eBook Finder Utilities Module
Contains functions for fetching and parsing eBook data from online sources.
"""
import requests
from bs4 import BeautifulSoup


def get_books_by_subject(url='https://www.epubbooks.com/subjects'):
    """
    Fetch and parse books organized by subjects from a website.
    
    Args:
        url: URL to fetch books from
        
    Returns:
        Dictionary with subjects as keys and lists of books as values
    """
    try:
        page = requests.get(url, timeout=10)
        page.raise_for_status()
        soup = BeautifulSoup(page.content, 'html.parser')
        
        books_data = {}
        
        # Try to parse the structure - this is a simplified parser
        # The actual structure may vary and need adjustment
        subjects_section = soup.find_all('div', class_='subject')
        
        if not subjects_section:
            # Alternative parsing if structure is different
            subjects_section = soup.find_all(['div', 'section'])
        
        for subject in subjects_section:
            # Try to find subject name
            subject_name_tag = subject.find(['h2', 'h3', 'h4'])
            if not subject_name_tag:
                continue
                
            subject_name = subject_name_tag.text.strip()
            books = subject.find_all('a')
            
            if books:
                books_data[subject_name] = []
                for book in books:
                    book_title = book.text.strip()
                    if book_title:
                        books_data[subject_name].append(book_title)
        
        return books_data
    except requests.RequestException as e:
        raise Exception(f"Error fetching books: {str(e)}")
    except Exception as e:
        raise Exception(f"Error parsing books data: {str(e)}")


def prepare_tree_data(books_by_subject):
    """
    Convert books data to tree structure format.
    
    Args:
        books_by_subject: Dictionary with subjects and books
        
    Returns:
        List of tree node dictionaries
    """
    tree_data = []
    for subject, books in books_by_subject.items():
        subject_node = {
            "label": subject,
            "children": [{"label": book} for book in books]
        }
        tree_data.append(subject_node)
    return tree_data
