# Asynchronous News Search Scraper

This project is an asynchronous news search scraper using Python, `aiohttp`, and `BeautifulSoup` to fetch news articles from Google, Bing, and Yahoo.

## Features

- Supports multiple search engines: Google, Bing, and Yahoo
- Fetches articles asynchronously for efficiency
- Extracts titles, timestamps, media sources, and article links
- Saves results to a CSV file
- Implements random delays to mimic human browsing

## Prerequisites

Ensure you have Python 3.7 or later installed.

### Required Python Packages

Install dependencies using:

```sh
pip install aiohttp beautifulsoup4 pandas lxml
```

## Configuration

The script uses a `config.json` file to define search queries. The expected format is:

```json
{
  "companies": ["Tata", "Jio", "Apple"],
  "keywords": ["Lawsuits", "Merger", "Bankruptcy"],
  "num_pages": 3
}
```

## Directory Structure

```
article_extractor/
│── logs/                  # Stores log files
│── extracted_content/      # Stores extracted news results
│── src/
│   │── article_extractor.py  # Main script
│   │── config.json           # Search configuration
│── Docs/                  # Flowcharts and pseudocode
│── README.md               # Documentation
```

## Usage

Run the script using:

```sh
python src/article_extractor.py
```

## How It Works

1. **Fetching Pages**: The script queries news search engines asynchronously.
2. **Parsing Content**: Extracts relevant information using `BeautifulSoup`.
3. **Data Cleaning**: Cleans timestamps and extracts domains.
4. **Saving Results**: Saves extracted data into a structured CSV file in `extracted_content/`.
5. **Logging**: Tracks progress and errors.

## Example Output

A successfully scraped dataset will be saved as:

```
extracted_content/news_results_async.csv
```

## Error Handling

- If an article element is missing, an empty value is assigned.
- Any network issues or HTTP errors are logged.

