from urllib.parse import urlparse

def get_headers():
    """Returns headers to mimic a real browser."""
    return {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/119.0.0.0 Safari/537.36",
    }

def extract_website_name(url: str) -> str:
    """Extracts a simplified website name from a URL.

    Args:
        url (str): The URL string.

    Returns:
        str: The capitalized website name, or an empty string if extraction fails.
    """
    if not url:
        return ""
    try:
        domain = urlparse(url).netloc
        if domain.startswith("www."):
            domain = domain[4:]
        return domain.split(".")[0].capitalize()
    except Exception:
        return ""

def clean_timestamp(timestamp_text: str) -> str:
    """Cleans and formats a timestamp string.

    Args:
        timestamp_text (str): The raw timestamp text.

    Returns:
        str: The cleaned timestamp.
    """
    if not timestamp_text:
        return ""
    return timestamp_text.replace("·", "").strip()
