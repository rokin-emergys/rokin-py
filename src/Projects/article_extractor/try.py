import requests
import json
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
from urllib.parse import quote_plus

def get_headers():
    return {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Referer": "https://www.google.com/",
        "DNT": "1"
    }

def clean_media_name(media_text):
    """Cleans and extracts the media company name."""
    if not media_text:
        return ""
    
    # Remove unwanted characters and phrases
    media_text = media_text.replace("·", "").strip()
    media_text = media_text.split("-")[0].strip()  # Remove trailing dashes and text
    media_text = media_text.split("|")[0].strip()  # Remove trailing pipes and text
    return media_text

def clean_timestamp(timestamp_text):
    """Standardizes timestamp format."""
    if not timestamp_text:
        return ""
    
    # Remove unwanted phrases
    timestamp_text = timestamp_text.replace("·", "").strip()
    timestamp_text = timestamp_text.replace("ago", "").strip()
    return timestamp_text

def fetch_google_news(query, pages=1):
    results = []
    base_url = "https://www.google.com/search?q={query}&tbm=nws&start={start}"
    
    for page in range(pages):
        start = page * 10
        url = base_url.format(query=quote_plus(query), start=start)
        
        try:
            response = requests.get(url, headers=get_headers(), timeout=15)
            if response.status_code != 200:
                continue
                
            soup = BeautifulSoup(response.text, "html.parser")
            news_items = soup.find_all("div", class_="SoaBEf")
            
            for item in news_items:
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
                if title := item.find("div", class_="MBeuO"):
                    result["title"] = title.get_text(strip=True)
                if media := item.find("div", class_="CEMjEf"):
                    result["media"] = clean_media_name(media.get_text(strip=True))
                if timestamp := item.find("div", class_="LfVVr"):
                    result["timestamp"] = clean_timestamp(timestamp.get_text(strip=True))
                
                results.append(result)
                
            time.sleep(random.uniform(2, 4))
            
        except Exception as e:
            print(f"Google error: {e}")
    
    return results

def fetch_bing_news(query, pages=1):
    results = []
    base_url = "https://www.bing.com/news/search?q={query}&first={start}"
    
    for page in range(pages):
        start = page * 10
        url = base_url.format(query=quote_plus(query), start=start)
        
        try:
            response = requests.get(url, headers=get_headers(), timeout=15)
            if response.status_code != 200:
                continue
                
            soup = BeautifulSoup(response.text, "html.parser")
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
                if media := item.find("div", class_="source"):
                    result["media"] = clean_media_name(media.get_text(strip=True))
                if timestamp := item.find("span", class_="time"):
                    result["timestamp"] = clean_timestamp(timestamp.get_text(strip=True))
                
                results.append(result)
                
            time.sleep(random.uniform(2, 3))
            
        except Exception as e:
            print(f"Bing error: {e}")
    
    return results

def fetch_yahoo_news(query, pages=1):
    results = []
    base_url = "https://search.yahoo.com/search?p={query}&b={start}"
    
    for page in range(pages):
        start = (page * 10) + 1  # Yahoo uses 1-based indexing
        url = base_url.format(query=quote_plus(query), start=start)
        
        try:
            response = requests.get(url, headers=get_headers(), timeout=15)
            if response.status_code != 200:
                continue
                
            soup = BeautifulSoup(response.text, "html.parser")
            news_items = soup.find_all("div", class_="algo")
            
            for item in news_items:
                result = {
                    "search_engine": "Yahoo",
                    "search_string": query,
                    "link": "",
                    "title": "",
                    "media": "",
                    "timestamp": ""
                }
                
                if a_tag := item.find("h3"):
                    a_link = a_tag.find("a")
                    if a_link:
                        result["link"] = a_link["href"]
                        result["title"] = a_link.get_text(strip=True)
                if media := item.find("span", class_="fz-ms"):
                    result["media"] = clean_media_name(media.get_text(strip=True))
                if timestamp := item.find("span", class_="timestamp"):
                    result["timestamp"] = clean_timestamp(timestamp.get_text(strip=True))
                
                results.append(result)
                
            time.sleep(random.uniform(2, 3))
            
        except Exception as e:
            print(f"Yahoo error: {e}")
    
    return results

def fetch_news(query, pages=1, engines=["google", "bing", "yahoo"]):
    all_results = []
    
    if "google" in engines:
        all_results.extend(fetch_google_news(query, pages))
    if "bing" in engines:
        all_results.extend(fetch_bing_news(query, pages))
    if "yahoo" in engines:
        all_results.extend(fetch_yahoo_news(query, pages))
    
    return all_results

def load_config():
    """Loads search queries from config.json"""
    with open("config.json", "r") as file:
        config = json.load(file)
    
    companies = config.get("companies", [])
    keywords = config.get("keywords", [])
    num_pages = config.get("num_pages", 1)
    
    return companies, keywords, num_pages

if __name__ == "__main__":
    companies, keywords, num_pages = load_config()
    all_results = []

    for company in companies:
        for keyword in keywords:
            search_query = f"{company} {keyword}"
            print(f"Fetching news for: {search_query}")
            all_results.extend(fetch_news(search_query, num_pages))

    if all_results:
        df = pd.DataFrame(all_results)
        df = df[["search_engine", "search_string", "title", "media", "timestamp", "link"]]
        output_file = "news_results.csv"
        df.to_csv(output_file, index=False)
        print(f"Saved {len(df)} results to {output_file}")
    else:
        print("No results found")