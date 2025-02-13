import re
from PyPDF2 import PdfReader

# Define regex patterns for extracting specific data with non-capturing groups for date
PATTERNS = {
    'cin': r'[A-Z]\d{5}[A-Z]{2}\d{4}[A-Z]{3}\d{6}',
    'email': r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}',
    'phone': r'(\+?\d{1,4}[\s-]?)?(\(?\d{1,4}\)?[\s-]?)?(\d{10})',
    'pan': r'\b[A-Z]{5}[0-9]{4}[A-Z]\b',
    'date': r'\b(?:\d{1,2}[\/\-.]\d{1,2}[\/\-.]\d{2,4}|\d{4}[\/\-.]\d{1,2}[\/\-.]\d{1,2})\b',
    'website': r'\bhttps?://[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(?:/\S*)?\b|\bwww\.[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(?:/\S*)?\b'
}

def extract_data(pdf_path: str) -> dict:
    """Extracts structured data from a PDF file using predefined regex patterns.

    The function reads the first three pages of the PDF (if available) and 
    extracts information such as CIN, email, phone, PAN, dates, and websites.

    Args:
        pdf_path (str): The file path to the PDF document.

    Returns:
        dict: A dictionary where keys correspond to data categories (e.g., "email", "phone"), 
              and values are sets containing the extracted matches.

    Raises:
        Exception: If an error occurs while reading the PDF.
    """
    results = {key: set() for key in PATTERNS}
    
    try:
        reader = PdfReader(pdf_path)
        for page in reader.pages[:3]:  # Process first 3 pages
            text = page.extract_text() or ''
            for key, pattern in PATTERNS.items():
                results[key].update(re.findall(pattern, text))
    except Exception as e:
        print(f"Error processing PDF {pdf_path}: {e}")
    
    return results
