import os
import re
import logging
from urllib.parse import urlparse

# Ensure that the extracted_content directory exists.
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
extracted_dir = os.path.join(project_root, "extracted_content")
os.makedirs(extracted_dir, exist_ok=True)

def clean_filename(title: str) -> str:
    """
    Cleans the title to create a safe filename by removing special characters
    and trimming to 50 characters.
    """
    return re.sub(r'[^\w\s-]', '', title).strip()[:50]

def save_article(title: str, content: str, domain: str, img_url: str = None) -> bool:
    """
    Saves the article content to a Markdown file.

    Args:
        title (str): Article title.
        content (str): Article content in Markdown format.
        domain (str): Domain string (used as part of the filename).
        img_url (str, optional): URL of the article image.

    Returns:
        bool: True if saved successfully, False otherwise.
    """
    try:
        filename = f"{domain}_{clean_filename(title)}.md"
        filepath = os.path.join(extracted_dir, filename)
        # Prepare Markdown image syntax if an image URL is provided.
        img_md = f"![Image]({img_url})\n\n" if img_url and "grey-placeholder" not in img_url.lower() else ""
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"# {title}\n\n{img_md}{content}")
        logging.info(f"Saved article: {filepath}")
        return True
    except Exception as e:
        logging.error(f"Save failed: {e}")
        return False

def extract_domain(url: str) -> str:
    """
    Extracts a simple domain string (typically the second-last segment) from a URL.
    """
    try:
        # For example, for "www.bbc.com" it returns "bbc"
        parts = url.split("//")[-1].split(".")
        return parts[-2] if len(parts) >= 2 else "unknown"
    except Exception:
        return "unknown"
