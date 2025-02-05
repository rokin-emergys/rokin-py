import re
import os
import time
import asyncio
import aiohttp
from PyPDF2 import PdfReader
from concurrent.futures import ProcessPoolExecutor

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
download_dir = os.path.join(project_root, 'downloads')
os.makedirs(download_dir, exist_ok=True)

def extract_data(pdf_path):
    patterns = {
        'cin': r'[A-Z]\d{5}[A-Z]{2}\d{4}[A-Z]{3}\d{6}',
        'email': r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}',
        'phone': r'(\+91[-\s]?[6-9]\d{9}|[6-9]\d{9}|\d{2,5}[-\s]?\d{5,8})',
        'pan': r'\b[A-Z]{5}[0-9]{4}[A-Z]\b',
        'date': r'\b(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/\d{4}\b',
        'website': r'\bhttps?://[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(?:/\S*)?\b|\bwww\.[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(?:/\S*)?\b'
    }
    results = {key: set() for key in patterns}
    
    try:
        reader = PdfReader(pdf_path)
        for page in reader.pages[:3]:
            text = page.extract_text() or ''
            for key, pattern in patterns.items():
                results[key].update(re.findall(pattern, text))
    except Exception as e:
        print(f"Error processing PDF {pdf_path}: {e}")
    
    return results

def print_results(data, company):
    print(f"\n{'='*40}\nResults for {company}\n{'='*40}")
    for key, values in data.items():
        print(f"\n{key.upper()} ({len(values)} found):")
        for v in values:
            print(f"- {v}")

async def download_pdf(session, url, filename):
    async with session.get(url, timeout=30) as resp:
        if resp.status == 200:
            content = await resp.read()
            with open(filename, 'wb') as f:
                f.write(content)
            return filename
        else:
            raise Exception(f"Failed to download {url}: status {resp.status}")

async def process_company(session, company, url, executor):
    filename = os.path.join(download_dir, f"{company}_MGT-7-async.pdf")
    try:
        await download_pdf(session, url, filename)
        loop = asyncio.get_event_loop()
        data = await loop.run_in_executor(executor, extract_data, filename)
        print_results(data, company)
    except Exception as e:
        print(f"Error processing {company}: {e}")

async def main():
    pdf_urls = {
        'Airtel': 'https://assets.airtel.in/teams/simplycms/web/docs/Draft-Annual-Return-FY-2021-22.pdf',
        'Tata': 'https://www.tatamotors.com/wp-content/uploads/2023/10/Form-MGT-7.pdf'
    }

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
