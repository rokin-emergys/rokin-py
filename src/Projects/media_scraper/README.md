# News Scraper

This project is an **asynchronous** web scraper built using Python, `aiohttp`, and `BeautifulSoup` to extract news articles from specified websites and save them as Markdown files. The scraper is designed for efficiency and maintainability by leveraging asynchronous processing and a modular code structure.

---

## Features

- **Asynchronous Fetching:**  
  Retrieves web pages concurrently using `aiohttp` for improved performance.

- **HTML Parsing:**  
  Uses `BeautifulSoup` to parse HTML and extract article components (titles, content, images, etc.).

- **Markdown Conversion:**  
  Converts HTML content into Markdown format using `html2text` for easier reading and portability.

- **Logging:**  
  Records progress and errors into log files for troubleshooting.

- **Content Cleaning:**  
  Cleans and formats extracted text and filenames to ensure safe storage.

- **Modular Design:**  
  Helper functions and configuration logic are organized in the `src/utils/` directory, keeping the main script focused on orchestration.

---

## Prerequisites

Ensure you have **Python 3.7** or later installed.

### Required Python Packages

Install the dependencies using pip:

```sh
pip install aiohttp beautifulsoup4 html2text lxml
```

---

## Configuration

By default, the scraper is configured to extract articles from a set of predefined news sources (e.g., [Indian Express](https://indianexpress.com) and [The Hindu](https://www.thehindu.com), among others). To add or modify sources, update the configuration in the `config.json` file (if used) or adjust the selectors and default URLs in the main script or helper modules.

---

## Directory Structure

```
media_scraper/
├── Docs/                     
│   └── pseudocode.txt         # Flowcharts and pseudocodes
├── extracted_content/         # Stores extracted articles as Markdown files
├── logs/                     # Stores log files (e.g., news_scraping.log)
└── src/
    ├── config.json           # (Optional) Configuration file for news sources
    ├── main.py  # Main asynchronous scraping script
    └── utils/                # Utility modules for the scraper
        ├── __init__.py       # (Empty; marks this folder as a package)
        ├── config_loader.py  # Loads configuration from config.json (if used)
        ├── common.py         # Contains common helper functions (e.g., filename cleaning, saving articles)
        └── scraper.py  # Contains asynchronous scraping functions using aiohttp and BeautifulSoup
```

*Note:* The extracted articles will be saved in the `extracted_content/` directory at the project root—not within `src/`.

---

## Usage

From the project root, run the asynchronous scraper with:

```sh
python src/main.py
```

During execution, you may be prompted to select which websites to process or to provide custom URLs. If you simply press Enter, the default URL for each source will be used.

---

## How It Works

1. **Fetching Pages:**  
   The scraper asynchronously fetches the HTML content of each article page using `aiohttp`.

2. **Parsing Content:**  
   Using `BeautifulSoup` and CSS selectors defined for each source, the scraper extracts the article title, content, and optionally an image URL.

3. **Content Conversion:**  
   The extracted HTML is converted into Markdown format using `html2text`.

4. **Saving Articles:**  
   Each article is saved as a Markdown file in the `extracted_content/` directory. Filenames are generated based on the source domain and a cleaned version of the article title.

5. **Logging:**  
   Progress and errors are logged in `logs/news_scraping.log` for monitoring and troubleshooting.

---

## Example Output

A successfully scraped article might be saved as:

```
extracted_content/indianexpress_China_announces_measures_against_Google.md
```

Each Markdown file contains the article's title, any associated image (if available), and the formatted content.

---

## Error Handling

- **Missing Elements:**  
  If a required element (e.g., title or content) is missing, the script logs an error and skips the article.

- **Network Issues:**  
  HTTP errors and network issues are caught and logged.

- **Selector Mismatches:**  
  Incorrect or outdated CSS selectors will result in an error being logged. Update selectors in the configuration or helper modules as needed.
