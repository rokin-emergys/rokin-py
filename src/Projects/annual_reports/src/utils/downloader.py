import os
import aiohttp
import asyncio

async def download_pdf(session: aiohttp.ClientSession, url: str, filename: str) -> str:
    """Downloads a PDF file from a given URL and saves it locally.

    Args:
        session (aiohttp.ClientSession): An active aiohttp session for making HTTP requests.
        url (str): The URL of the PDF file to download.
        filename (str): The file path where the downloaded PDF will be saved.

    Returns:
        str: The filename where the PDF was saved.

    Raises:
        Exception: If the request fails or returns a non-200 HTTP status code.
    """
    async with session.get(url, timeout=30) as resp:
        if resp.status == 200:
            content = await resp.read()
            with open(filename, 'wb') as f:
                f.write(content)
            return filename
        else:
            raise Exception(f"Failed to download {url}: status {resp.status}")

async def fetch_pdfs(session: aiohttp.ClientSession, download_dir: str, pdf_urls: dict) -> list:
    """Downloads multiple PDF files concurrently from a dictionary of URLs.

    Args:
        session (aiohttp.ClientSession): An active aiohttp session for making HTTP requests.
        download_dir (str): The directory where the downloaded PDFs should be saved.
        pdf_urls (dict): A dictionary mapping company names to their respective PDF URLs.

    Returns:
        list: A list of filenames where the PDFs were saved. If an error occurs, an exception is returned instead.
    """
    tasks = []
    for company, url in pdf_urls.items():
        filename = os.path.join(download_dir, f"{company}_MGT-7-async.pdf")
        tasks.append(download_pdf(session, url, filename))
    
    return await asyncio.gather(*tasks, return_exceptions=True)
