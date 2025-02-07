import os
import re
import json
import time
import asyncio
import aiohttp
import logging
from bs4 import BeautifulSoup
import html2text
from urllib.parse import urlparse

# Set up project directories and logging.
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
logs_dir = os.path.join(project_root, "logs")
extracted_dir = os.path.join(project_root, "extracted_content")
os.makedirs(logs_dir, exist_ok=True)
os.makedirs(extracted_dir, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(logs_dir, 'news_scraping.log'),
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def clean_filename(title):
    """
    Cleans the article title to create a safe filename.
    Removes special characters and trims the title to 50 characters.
    """
    return re.sub(r'[^\w\s-]', '', title).strip()[:50]

def save_article(title, content, domain, img_url=None):
    """
    Saves the article content to a Markdown file.
    
    - Generates a filename using the domain and cleaned title.
    - Prepares Markdown image syntax if a valid image URL is provided.
    - Writes the title, image (if any), and main content to the file.
    
    Returns True on success, False otherwise.
    """
    try:
        filename = f"{domain}_{clean_filename(title)}.md"
        filepath = os.path.join(extracted_dir, filename)
        img_md = f"![Image]({img_url})\n\n" if img_url and "grey-placeholder" not in img_url.lower() else ""
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"# {title}\n\n{img_md}{content}")
        logging.info(f"Saved article: {filepath}")
        return True
    except Exception as e:
        logging.error(f"Save failed: {e}")
        return False

async def fetch_page(session, url, headers):
    """
    Fetches the HTML content of the given URL using an aiohttp session.
    Raises an exception if the request fails.
    """
    async with session.get(url, headers=headers, timeout=15) as response:
        response.raise_for_status()
        return await response.text()

async def scrape_article(url, title_selector, content_selector, img_selector):
    """
    Scrapes an article from the provided URL:
    
    - Fetches the HTML content of the page.
    - Parses the HTML using BeautifulSoup.
    - Extracts the article title using the title_selector.
    - Depending on the domain (e.g., "bbc.com", "thehindu.com", etc.), extracts the main content and image URL.
    - Converts HTML content to Markdown using html2text.
    - Calls save_article to write the article to a Markdown file.
    
    Returns True if the article was saved successfully, otherwise False.
    """
    try:
        headers = {
            'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                           'AppleWebKit/537.36 (KHTML, like Gecko) '
                           'Chrome/119.0.0.0 Safari/537.36')
        }
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

        # Domain-specific parsing.
        if "bbc.com" in url:
            paragraphs = soup.select(content_selector)
            md_content = "\n".join(converter.handle(str(p)).replace('_', '') for p in paragraphs)
            img_tag = soup.select_one(img_selector) or soup.select_one(f"figure {img_selector}")
            if img_tag:
                if 'srcset' in img_tag.attrs:
                    entries = [entry.strip() for entry in img_tag['srcset'].split(',') if entry.strip()]
                    valid_entries = [entry for entry in entries if "grey-placeholder" not in entry.lower()]
                    if valid_entries:
                        img_url = valid_entries[-1].split()[0]
                if not img_url and 'src' in img_tag.attrs:
                    candidate = img_tag['src']
                    if "grey-placeholder" not in candidate.lower():
                        img_url = candidate

        elif "thehindu.com" in url:
            content_el = soup.select_one(content_selector)
            if not content_el:
                raise ValueError("Content element not found")
            md_content = converter.handle(str(content_el)).replace('_', '')
            img_tag = soup.select_one(img_selector)
            if img_tag:
                img_url = img_tag.get('src') or img_tag.get('srcset')

        else:
            content_el = soup.select_one(content_selector)
            if not content_el:
                raise ValueError("Content element not found")
            md_content = converter.handle(str(content_el)).replace('_', '')
            img_tag = soup.select_one(img_selector)
            if img_tag and 'src' in img_tag.attrs:
                img_url = img_tag['src']

        if img_url:
            logging.info(f"Image: {img_url}")

        domain = urlparse(url).netloc.split('.')[-2]
        return save_article(title, md_content, domain, img_url)
    except Exception as e:
        logging.error(f"Error scraping {url}: {e}")
        return False

async def main():
    """
    Main entry point for the scraper.
    
    - Loads the configuration from "config.json".
    - Displays available websites.
    - Prompts the user to choose to process all websites or a single website.
    - For each selected source, prompts the user to enter one or more URLs (comma-separated)
      or press Enter to use the default URL.
    - Creates and gathers asynchronous scraping tasks for each URL.
    - Prints the result of each scraping task and total execution time.
    """
    # Load configuration.
    with open("config.json", "r") as file:
        config = json.load(file)

    # Display available websites.
    print("Available websites:")
    for i, source in enumerate(config["sources"], start=1):
        print(f"{i}. {source['name']}")

    # Ask user if they want to process all or a single website.
    mode = input("\nProcess all websites? (y/n): ").lower().strip()
    if mode.startswith("n"):
        print("\nSelect a website to process:")
        for i, source in enumerate(config["sources"], start=1):
            print(f"{i}. {source['name']}")
        try:
            choice = int(input("Enter the number of the website: ").strip())
            # Keep only the selected source.
            config["sources"] = [config["sources"][choice - 1]]
        except Exception as e:
            print("Invalid input. Processing all websites.")

    # For each selected source, prompt for one or more URLs (comma-separated).
    print("\nEnter URL(s) for each website (or press Enter to use the default URL):")
    for source in config["sources"]:
        default_url = source["url"]
        user_input = input(f"{source['name']} : ").strip()
        if user_input:
            # Split the input by comma, strip each URL, and remove empty entries.
            urls = [u.strip() for u in user_input.split(",") if u.strip()]
            source["urls"] = urls
        else:
            source["urls"] = [default_url]

    # Create scraping tasks for each URL.
    tasks = []
    for source in config["sources"]:
        for url in source["urls"]:
            tasks.append(
                scrape_article(
                    url,
                    source["selectors"]["title"],
                    source["selectors"]["content"],
                    source["selectors"].get("img")
                )
            )
    start_time = time.time()
    results = await asyncio.gather(*tasks)

    # Print the results.
    for i, result in enumerate(results, start=1):
        print(f"Scrape result {i}: {result}")
    print(f"Total execution time: {time.time() - start_time:.2f} seconds")

if __name__ == "__main__":
    asyncio.run(main())
    
