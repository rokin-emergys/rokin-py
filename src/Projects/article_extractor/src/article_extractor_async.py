import asyncio
import aiohttp
from bs4 import BeautifulSoup
import json
import os
import pandas as pd
import time
import random
from urllib.parse import urlparse


def random_delay(min_delay, max_delay):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            await asyncio.sleep(random.uniform(min_delay, max_delay))
            return await func(*args, **kwargs)
        return wrapper
    return decorator


def get_headers():
    return {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    }

# for Bing results only
def extract_website_name(url):
    if not url:
        return ""
    try:
        domain = urlparse(url).netloc
        if domain.startswith("www."):
            domain = domain[4:]
        return domain.split(".")[0].capitalize()
    except:
        return ""

def clean_timestamp(timestamp_text):
    if not timestamp_text:
        return ""
    return timestamp_text.replace("·", "").strip()

@random_delay(1, 3)
async def fetch_page(session, url, headers):
    async with session.get(url, headers=headers) as response:
        if response.status == 200:
            return await response.text()
        else:
            raise Exception(f"HTTP Error {response.status}")

async def process_google(session, query, page):
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
        if a_tag := item.find("a"):
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

async def process_bing(session, query, page):
    url = f"https://www.bing.com/news/search?q={query}&first={page*10}"
    html = await fetch_page(session, url, get_headers())
    soup = BeautifulSoup(html, 'html.parser')
    results = []
    
    news_items = soup.find_all("div", class_="news-card")
    for item in news_items:
        result = {
            "search_engine": "Bing",
            "search_string": query,
            "link": "",
            "title": "",
            "media": "",
            "timestamp": ""
        }
        
        if a_tag := item.find("a", class_="title"):
            result["link"] = a_tag["href"]
            result["title"] = a_tag.get_text(strip=True)
            result["media"] = extract_website_name(result["link"])
        
        timestamp_tag = item.find("span", attrs={"tabindex": "0"})
        if timestamp_tag:
            result["timestamp"] = clean_timestamp(timestamp_tag.get_text(strip=True))
        
        results.append(result)
    return results

async def process_yahoo(session, query, page):
    url = f"https://news.search.yahoo.com/search?p={query}&b={page*10+1}"
    html = await fetch_page(session, url, get_headers())
    soup = BeautifulSoup(html, 'html.parser')
    results = []
    news_articles = soup.find_all("div", class_="NewsArticle")
    for article in news_articles:
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

async def fetch_engine(session, engine, query, pages):
    tasks = []
    for page in range(pages):
        if engine == "google":
            tasks.append(process_google(session, query, page))
        elif engine == "bing":
            tasks.append(process_bing(session, query, page))
        elif engine == "yahoo":
            tasks.append(process_yahoo(session, query, page))
    return await asyncio.gather(*tasks)

async def fetch_query(session, query, pages, engines):
    all_results = []
    engine_tasks = [fetch_engine(session, engine, query, pages) for engine in engines]
    engine_results = await asyncio.gather(*engine_tasks)
    
    for results in engine_results:
        for page_results in results:
            all_results.extend(page_results)
    return all_results


async def main():
    with open("config.json") as f:
        config = json.load(f)

    companies = config["companies"]
    keywords = config["keywords"]
    pages = config.get("num_pages", 1)
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
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        output_dir = os.path.join(project_root, "extracted_content")
        os.makedirs(output_dir, exist_ok=True)
        
        output_file = os.path.join(output_dir, "news_results_async.csv")
        df.to_csv(output_file, index=False)
        
        print(f"Saved {len(df)} results to {output_file}, time taken: {end_time-start_time} secs")

if __name__ == "__main__":
    asyncio.run(main())
