# News Scraper

This is an asynchronous web scraper built using Python, `aiohttp`, and `BeautifulSoup` to extract news articles from specified websites and save them as Markdown files.

## Features

- Asynchronous fetching of web pages for efficiency
- Uses `BeautifulSoup` to parse HTML
- Extracts and saves article titles and content in Markdown format
- Handles logging for error tracking
- Cleans and formats extracted content

## Prerequisites

Ensure you have Python 3.7 or later installed.

### Required Python Packages

Install dependencies using pip:

```sh
pip install aiohttp beautifulsoup4 html2text lxml
```

## Directory Structure

```
media_scraper/
|── Docs/                   # Flowcharts and pseudocodes
│── logs/                   # Stores log files
│── extracted_content/      # Stores extracted articles
│── src/ 
|   |── media_scraper.py    # Main script
│── README.md               # Documentation
```

## Usage

Run the script using:

```sh
python src/media_scraper.py
```

## How It Works

1. **Fetching Pages**: The script fetches article pages asynchronously using `aiohttp`.
2. **Parsing Content**: It extracts the title and content using `BeautifulSoup` and CSS selectors.
3. **Cleaning and Formatting**: The content is converted to Markdown using `html2text`.
4. **Saving the Article**: The extracted content is saved in the `extracted_content/` directory.
5. **Logging**: Logs are stored in `logs/news_scraping.log`.

## Configuration

The script currently scrapes articles from:

- [Indian Express](https://indianexpress.com)
- [The Hindu](https://www.thehindu.com)

To add more sources, modify the `main()` function and update the CSS selectors accordingly.

## Example Output

A successfully scraped article will be saved as:

```
extracted_content/indianexpress_China_announces_measures_against_Google.md
```

## Error Handling

- If a title or content selector is incorrect, an error is logged.
- Any network issues will be caught and logged.

