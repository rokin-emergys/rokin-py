# Asynchronous News Search Scraper

This project is an asynchronous news search scraper built with Python, `aiohttp`, and `BeautifulSoup`. It fetches news articles from popular search engines (Google, Bing, and Yahoo) and extracts key information such as titles, timestamps, media sources, and article links. The project is modularized for maintainability, with configuration and helper functions located in the `src/utils/` directory.

---

## Features

- **Multi-Engine Support:**  
  Fetches articles from Google, Bing, and Yahoo.

- **Asynchronous Processing:**  
  Uses `aiohttp` to query pages concurrently for improved efficiency.

- **Data Extraction:**  
  Parses HTML with `BeautifulSoup` to extract article titles, timestamps, media sources, and links.

- **Random Delays:**  
  Implements randomized delays to mimic human browsing behavior.

- **Modular Design:**  
  Helper functions are organized under the `src/utils/` folder.

- **Dynamic Configuration:**  
  Search queries and parameters are defined in a `config.json` file.

- **Output:**  
  Consolidates extracted data into a CSV file saved in the `extracted_content/` directory.

- **Logging:**  
  Tracks progress and errors with log files stored in the `logs/` directory.

---

## Prerequisites

- **Python 3.7+**  
- **Required Packages:**

  Install dependencies with:

  ```sh
  pip install aiohttp beautifulsoup4 pandas lxml
  ```

---

## Configuration

The scraper uses a `config.json` file (located in the `src/` directory) to define search queries. The expected format is:

```json
{
  "companies": ["Tata", "Jio", "Apple"],
  "keywords": ["Lawsuits", "Merger", "Bankruptcy"],
  "num_pages": 3
}
```

You can modify this file to change the search parameters as needed.

---

## Directory Structure

```
article_extractor/
├── Docs/                     
│   └── pseudocode.txt         # Flowcharts and pseudocode
├── extracted_content/         # Stores extracted news results (e.g., CSV output)
├── logs/                     # Stores log files
└── src/
    ├── config.json           # Configuration file for search queries
    ├── main.py  # Main asynchronous scraping script
    └── utils/                # Utility modules
        ├── __init__.py       # (Empty file to mark this folder as a package)
        ├── config_loader.py  # Loads configuration from config.json
        ├── common.py         # Contains common helper functions (e.g., filename cleaning, saving articles)
        └── scraper.py  # Contains asynchronous scraping functions using aiohttp and BeautifulSoup
```

---

## Usage

To run the scraper, execute the following command from the project root:

```sh
python src/main.py
```

During execution, you will be prompted to choose which websites to scrape and, optionally, provide custom URLs. If you press Enter without input, the default URLs defined in the configuration will be used.

---

## How It Works

1. **Fetching Pages:**  
   The scraper queries news search engines asynchronously using `aiohttp`.

2. **Parsing Content:**  
   It uses `BeautifulSoup` to parse the HTML content and extract relevant information such as article titles, timestamps, media sources, and links.

3. **Data Cleaning:**  
   The script cleans timestamps, extracts domain information, and processes HTML content into a suitable format.

4. **Saving Results:**  
   All extracted data is saved into a CSV file in the `extracted_content/` directory.

5. **Logging:**  
   Progress and errors are logged in the `logs/` directory for troubleshooting.

---

## Example Output

A successfully scraped dataset will be saved as:

```
extracted_content/news_results.csv
```

Each row in the CSV file contains the search engine used, the search string, the article title, media source, timestamp, and the article link.

---

## Error Handling

- **Missing Elements:**  
  If a required article element (e.g., title or content) is missing, an empty value is assigned.

- **Network Issues:**  
  Any HTTP errors or network issues encountered during scraping are logged.
