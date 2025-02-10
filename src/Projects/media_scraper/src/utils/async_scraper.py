import asyncio
import aiohttp
import logging
from bs4 import BeautifulSoup
import html2text
from urllib.parse import urlparse
from utils.helper import save_article

def get_headers() -> dict:
    """Returns headers to mimic a real browser."""
    return {
        'User-Agent': (
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/119.0.0.0 Safari/537.36'
        )
    }

async def fetch_page(session: aiohttp.ClientSession, url: str, headers: dict) -> str:
    """
    Fetches HTML content of the given URL using aiohttp.
    
    Raises an exception if the HTTP request fails.
    """
    async with session.get(url, headers=headers, timeout=15) as response:
        response.raise_for_status()
        return await response.text()

async def scrape_article(url: str, title_selector: str, content_selector: str, img_selector: str = None) -> bool:
    """
    Scrapes an article from the given URL using the provided CSS selectors.
    
    - Fetches the HTML content.
    - Parses the content using BeautifulSoup.
    - Extracts title, content, and (optionally) image URL.
    - Converts HTML to Markdown using html2text.
    - Saves the article using save_article().
    
    Args:
        url (str): URL of the article.
        title_selector (str): CSS selector to locate the title.
        content_selector (str): CSS selector to locate the article content.
        img_selector (str, optional): CSS selector to locate an image.
    
    Returns:
        bool: True if the article was saved successfully, False otherwise.
    """
    try:
        headers = get_headers()
        # Use a temporary aiohttp session to fetch the page.
        async with aiohttp.ClientSession() as session:
            html_text = await fetch_page(session, url, headers)
        
        converter = html2text.HTML2Text()
        converter.ignore_links = True
        converter.ignore_images = True
        soup = BeautifulSoup(html_text, 'lxml')
        
        title_el = soup.select_one(title_selector)
        if not title_el:
            raise ValueError("Title element not found")
        title = title_el.get_text(strip=True)
        
        md_content = ""
        img_url = None

        # Domain-specific parsing:
        if "bbc.com" in url:
            paragraphs = soup.select(content_selector)
            md_content = "\n".join(converter.handle(str(p)).replace('_', '') for p in paragraphs)
            img_tag = soup.select_one(img_selector) if img_selector else None
            if img_tag:
                if 'srcset' in img_tag.attrs:
                    entries = [entry.strip() for entry in img_tag['srcset'].split(',') if entry.strip()]
                    valid_entries = [entry for entry in entries if "grey-placeholder" not in entry.lower()]
                    if valid_entries:
                        img_url = valid_entries[-1].split()[0]
                elif 'src' in img_tag.attrs:
                    candidate = img_tag['src']
                    if "grey-placeholder" not in candidate.lower():
                        img_url = candidate
        elif "thehindu.com" in url:
            content_el = soup.select_one(content_selector)
            if not content_el:
                raise ValueError("Content element not found")
            md_content = converter.handle(str(content_el)).replace('_', '')
            img_tag = soup.select_one(img_selector) if img_selector else None
            if img_tag:
                img_url = img_tag.get('src') or img_tag.get('srcset')
        else:
            content_el = soup.select_one(content_selector)
            if not content_el:
                raise ValueError("Content element not found")
            md_content = converter.handle(str(content_el)).replace('_', '')
            if img_selector:
                img_tag = soup.select_one(img_selector)
                if img_tag and 'src' in img_tag.attrs:
                    img_url = img_tag['src']
        
        if img_url:
            logging.info(f"Found image URL: {img_url}")
        
        # Extract domain from URL (using simple method here)
        domain = urlparse(url).netloc.split('.')[-2]
        return save_article(title, md_content, domain, img_url)
    except Exception as e:
        logging.error(f"Error scraping {url}: {e}")
        return False
