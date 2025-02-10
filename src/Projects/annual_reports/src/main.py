import os
import time
import asyncio
from concurrent.futures import ProcessPoolExecutor
import aiohttp

# Import helper functions from the utils package
from utils.downloader import download_pdf
from utils.extractor import extract_data
from utils.printer import print_results

# Determine the project root and create the downloads directory if needed
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
download_dir = os.path.join(project_root, 'downloads')
os.makedirs(download_dir, exist_ok=True)

def get_pdf_urls(default_pdf_urls: dict) -> dict:
    """
    Prompts the user to update or provide dynamic PDF URLs.

    Args:
        default_pdf_urls (dict): A dictionary containing default company names and their PDF URLs.

    Returns:
        dict: Updated dictionary with company names as keys and PDF URLs as values.
    """
    print("Default PDF URLs:")
    for company, url in default_pdf_urls.items():
        print(f"  {company}: {url}")
        
    answer = input("Do you want to update the PDF URLs? (y/n): ").strip().lower()
    if answer == "y":
        new_urls = {}
        try:
            n = int(input("Enter the number of companies to provide URLs for: ").strip())
        except ValueError:
            print("Invalid number entered; using default PDF URLs.")
            return default_pdf_urls
        
        for i in range(n):
            company = input("Enter company name: ").strip()
            url = input("Enter PDF URL for that company: ").strip()
            new_urls[company] = url
        return new_urls
    else:
        return default_pdf_urls

async def process_company(session: aiohttp.ClientSession, company: str, url: str, executor: ProcessPoolExecutor) -> None:
    """
    Downloads the PDF for a company, extracts data, and prints the results.

    Args:
        session (aiohttp.ClientSession): The aiohttp session used for downloading.
        company (str): The company name.
        url (str): The URL of the company's PDF.
        executor (ProcessPoolExecutor): Executor for parallel data extraction.
    """
    filename = os.path.join(download_dir, f"{company}_MGT-7-async.pdf")
    try:
        # Download the PDF asynchronously
        await download_pdf(session, url, filename)
        # Run extract_data in a separate process
        loop = asyncio.get_event_loop()
        data = await loop.run_in_executor(executor, extract_data, filename)
        # Print the extracted results
        print_results(data, company)
    except Exception as e:
        print(f"Error processing {company}: {e}")

async def main():
    # Define default PDF URLs
    default_pdf_urls = {
        'Airtel': 'https://assets.airtel.in/teams/simplycms/web/docs/Draft-Annual-Return-FY-2021-22.pdf',
        'Tata': 'https://www.tatamotors.com/wp-content/uploads/2023/10/Form-MGT-7.pdf'
    }
    
    # Dynamically update PDF URLs if the user wishes
    pdf_urls = get_pdf_urls(default_pdf_urls)
    
    async with aiohttp.ClientSession() as session:
        with ProcessPoolExecutor() as executor:
            tasks = [
                process_company(session, company, url, executor)
                for company, url in pdf_urls.items()
            ]
            await asyncio.gather(*tasks)

if __name__ == '__main__':
    start_time = time.time()
    asyncio.run(main())
    end_time = time.time()
    print(f"\nTotal execution time: {end_time - start_time:.2f} seconds")
