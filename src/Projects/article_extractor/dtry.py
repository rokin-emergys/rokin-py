import json
import time
import random
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

SEARCH_CONFIG = {
    'google': {
        'url': 'https://www.google.com/search?q={query}&tbm=nws&start={start}',
        'selectors': {
            'results': 'div.SoaBEf',
            'link': 'a',
            'title': 'div.MBeuO',
            'media': '.CEMjEf',
            'timestamp': '.LfVVr'
        }
    },
    'bing': {
        'url': 'https://www.bing.com/news/search?q={query}&first={start}',
        'selectors': {
            'results': 'div.newsitem',
            'link': 'a.title',
            'title': 'a.title',
            'media': 'div.source',
            'timestamp': 'div.timestamp'
        }
    }
}

class NewsScraper:
    def __init__(self):
        self.driver = self._init_driver()
        self.results = []
        
    def _init_driver(self):
        options = Options()
        options.add_argument("--headless=new")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36")
        options.add_argument("--window-size=1920,1080")
        return webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )

    def load_config(self, path):
        with open(path) as f:
            return json.load(f)

    def generate_queries(self, config):
        return [f"{c} {k}" for c in config['companies'] for k in config['keywords']]

    def scrape_engine(self, query, engine, num_pages):
        config = SEARCH_CONFIG[engine]
        for page in range(num_pages):
            start = page * 10
            url = config['url'].format(
                query=query.replace(' ', '+'),
                start=start
            )
            
            self.driver.get(url)
            self._human_like_delay()
            
            try:
                results = self.driver.find_elements(By.CSS_SELECTOR, config['selectors']['results'])
                for result in results:
                    self._process_result(result, config, query, engine)
            except NoSuchElementException:
                print(f"No results found for {query} on {engine}")
                break

    def _process_result(self, result, config, query, engine):
        try:
            link = result.find_element(By.CSS_SELECTOR, config['selectors']['link']).get_attribute('href')
            title = result.find_element(By.CSS_SELECTOR, config['selectors']['title']).text
            media = result.find_element(By.CSS_SELECTOR, config['selectors']['media']).text
            timestamp = result.find_element(By.CSS_SELECTOR, config['selectors']['timestamp']).text
            
            self.results.append({
                'Search String': query,
                'Search Engine': engine,
                'Link': self._clean_url(link, engine),
                'Title': title,
                'Media': media,
                'Timestamp': timestamp
            })
        except Exception as e:
            print(f"Error processing result: {str(e)}")

    def _clean_url(self, url, engine):
        if engine == 'google':
            return url.split('&ved=')[0]
        return url

    def _human_like_delay(self):
        time.sleep(random.uniform(1.5, 4.5))
        if random.random() < 0.2:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight/3)")
            time.sleep(random.uniform(0.5, 1.5))

    def run(self, config_path, output_file):
        config = self.load_config(config_path)
        queries = self.generate_queries(config)
        
        for query in queries:
            for engine in SEARCH_CONFIG.keys():
                print(f"Scraping {engine} for: {query}")
                self.scrape_engine(query, engine, config['num_pages'])
        
        pd.DataFrame(self.results).to_csv(output_file, index=False)
        self.driver.quit()

if __name__ == "__main__":
    scraper = NewsScraper()
    scraper.run('config.json', 'news_results.csv')