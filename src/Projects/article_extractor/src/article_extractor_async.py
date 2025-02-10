import os
import time
import asyncio
import aiohttp
import pandas as pd
from utils.config_loader import load_config
from utils.async_scraper import fetch_query

def get_dynamic_config():
    """
    Loads the configuration from config.json and then prompts the user
    to update companies, keywords, and num_pages dynamically.
    
    Returns:
        tuple: (companies, keywords, pages)
    """
    # Load current configuration from the file.
    companies, keywords, pages = load_config()
    
    print("Current configuration:")
    print(f"Companies: {companies}")
    print(f"Keywords: {keywords}")
    print(f"Number of pages: {pages}")
    
    # Ask the user if they want to update the companies list.
    if input("Do you want to update the companies? (y/n): ").strip().lower() == "y":
        new_companies = input("Enter companies separated by commas: ").strip()
        # Split the input into a list, removing extra whitespace.
        companies = [comp.strip() for comp in new_companies.split(",") if comp.strip()]
    
    # Ask the user if they want to update the keywords list.
    if input("Do you want to update the keywords? (y/n): ").strip().lower() == "y":
        new_keywords = input("Enter keywords separated by commas: ").strip()
        keywords = [kw.strip() for kw in new_keywords.split(",") if kw.strip()]
    
    # Ask the user if they want to update the number of pages.
    if input("Do you want to update the number of pages? (y/n): ").strip().lower() == "y":
        new_pages = input("Enter the number of pages: ").strip()
        if new_pages.isdigit():
            pages = int(new_pages)
        else:
            print("Invalid input for number of pages; keeping the current value.")
    
    print("\nFinal configuration:")
    print(f"Companies: {companies}")
    print(f"Keywords: {keywords}")
    print(f"Number of pages: {pages}\n")
    
    return companies, keywords, pages

async def main(companies, keywords, pages):
    engines = ["google", "bing", "yahoo"]
    start_time = time.time()
    all_results = []
    
    async with aiohttp.ClientSession() as session:
        tasks = []
        for company in companies:
            for keyword in keywords:
                query = f"{company} {keyword}"
                tasks.append(fetch_query(session, query, pages, engines))
        results = await asyncio.gather(*tasks)
        for result in results:
            all_results.extend(result)
    
    end_time = time.time()
    
    if all_results:
        df = pd.DataFrame(all_results)
        df = df[["search_engine", "search_string", "title", "media", "timestamp", "link"]]
        
        # Define output directory relative to the project root.
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        output_dir = os.path.join(project_root, "extracted_content")
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, "news_results_async.csv")
        df.to_csv(output_file, index=False)
        
        print(f"Saved {len(df)} results to {output_file} in {end_time - start_time:.2f} secs")
    else:
        print("No results found")

if __name__ == "__main__":
    # Get the dynamic configuration from the user.
    companies, keywords, pages = get_dynamic_config()
    asyncio.run(main(companies, keywords, pages))
