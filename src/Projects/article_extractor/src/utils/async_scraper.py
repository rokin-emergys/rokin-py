import asyncio
import random
from bs4 import BeautifulSoup
from utils.helper import get_headers, extract_website_name, clean_timestamp

def random_delay(min_delay: float, max_delay: float):
    """Decorator to introduce a random delay before executing an async function."""
    def decorator(func):
        async def wrapper(*args, **kwargs):
            await asyncio.sleep(random.uniform(min_delay, max_delay))
            return await func(*args, **kwargs)
        return wrapper
    return decorator

@random_delay(1, 3)
async def fetch_page(session, url: str, headers: dict) -> str:
    async with session.get(url, headers=headers) as response:
        if response.status == 200:
            return await response.text()
        else:
            raise Exception(f"HTTP Error {response.status}")

async def process_google(session, query: str, page: int) -> list:
    start = page * 10
    url = f"https://www.google.com/search?q={query}&tbm=nws&start={start}"
    html = await fetch_page(session, url, get_headers())
    soup = BeautifulSoup(html, 'html.parser')
    results = []
    for item in soup.find_all("div", class_="SoaBEf"):
        result = {
            "search_engine": "Google",
            "search_string": query,
            "link": "",
            "title": "",
            "media": "",
            "timestamp": ""
        }
        if (a_tag := item.find("a")) is not None:
            result["link"] = a_tag["href"].split("&ved=")[0]
        media_tag = item.find("div", class_="MgUUmf")
        if media_tag:
            result["media"] = media_tag.get_text(strip=True)
        title_tag = item.find("div", class_="MBeuO")
        if title_tag:
            result["title"] = title_tag.get_text(strip=True)
        timestamp_tag = item.find("div", class_="LfVVr") or item.find("span", class_="WGvvNb")
        if timestamp_tag:
            result["timestamp"] = clean_timestamp(timestamp_tag.get_text(strip=True))
        results.append(result)
    return results

async def process_bing(session, query: str, page: int) -> list:
    url = f"https://www.bing.com/news/search?q={query}&first={page*10}"
    html = await fetch_page(session, url, get_headers())
    soup = BeautifulSoup(html, 'html.parser')
    results = []
    for item in soup.find_all("div", class_="news-card"):
        result = {
            "search_engine": "Bing",
            "search_string": query,
            "link": "",
            "title": "",
            "media": "",
            "timestamp": ""
        }
        if (a_tag := item.find("a", class_="title")) is not None:
            result["link"] = a_tag["href"]
            result["title"] = a_tag.get_text(strip=True)
            result["media"] = extract_website_name(result["link"])
        timestamp_tag = item.find("span", attrs={"tabindex": "0"})
        if timestamp_tag:
            result["timestamp"] = clean_timestamp(timestamp_tag.get_text(strip=True))
        results.append(result)
    return results

async def process_yahoo(session, query: str, page: int) -> list:
    url = f"https://news.search.yahoo.com/search?p={query}&b={page*10+1}"
    html = await fetch_page(session, url, get_headers())
    soup = BeautifulSoup(html, 'html.parser')
    results = []
    for article in soup.find_all("div", class_="NewsArticle"):
        result = {
            "search_engine": "Yahoo",
            "search_string": query,
            "link": "",
            "title": "",
            "media": "",
            "timestamp": ""
        }
        link_tag = article.find("a", class_="thmb")
        if link_tag:
            result["link"] = link_tag["href"]
            result["title"] = link_tag.get("title", "").strip()
        media_tag = article.find("span", class_="s-source")
        if media_tag:
            result["media"] = media_tag.get_text(strip=True)
        timestamp_tag = article.find("span", class_="s-time")
        if timestamp_tag:
            result["timestamp"] = clean_timestamp(timestamp_tag.get_text(strip=True))
        results.append(result)
    return results

async def fetch_engine(session, engine: str, query: str, pages: int) -> list:
    tasks = []
    for page in range(pages):
        if engine == "google":
            tasks.append(process_google(session, query, page))
        elif engine == "bing":
            tasks.append(process_bing(session, query, page))
        elif engine == "yahoo":
            tasks.append(process_yahoo(session, query, page))
    engine_results = await asyncio.gather(*tasks)
    # Flatten the list of lists.
    results = [item for sublist in engine_results for item in sublist]
    return results

async def fetch_query(session, query: str, pages: int, engines: list) -> list:
    all_results = []
    tasks = [fetch_engine(session, engine, query, pages) for engine in engines]
    engine_results = await asyncio.gather(*tasks)
    for results in engine_results:
        all_results.extend(results)
    return all_results
