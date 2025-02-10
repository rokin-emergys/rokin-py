import os
import time
import asyncio
import logging
from utils.config_loader import load_config
from Projects.media_scraper.src.utils.scraper import scrape_article

# Set up project directories and logging.
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
logs_dir = os.path.join(project_root, "logs")
os.makedirs(logs_dir, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(logs_dir, 'news_scraping.log'),
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

async def main():
    # Load configuration from config.json.
    config = load_config()
    
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
            config["sources"] = [config["sources"][choice - 1]]
        except Exception:
            print("Invalid input. Processing all websites.")
    
    # For each selected source, prompt for one or more URLs (comma-separated).
    print("\nEnter URL(s) for each website (or press Enter to use the default URL):")
    for source in config["sources"]:
        default_url = source["url"]
        user_input = input(f"{source['name']} : ").strip()
        if user_input:
            urls = [u.strip() for u in user_input.split(",") if u.strip()]
            source["urls"] = urls
        else:
            source["urls"] = [default_url]
    
    # Create asynchronous scraping tasks for each URL.
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
    
    for i, result in enumerate(results, start=1):
        print(f"Scrape result {i}: {result}")
    print(f"Total execution time: {time.time() - start_time:.2f} seconds")

if __name__ == "__main__":
    asyncio.run(main())
