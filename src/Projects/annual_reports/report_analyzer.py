import re
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from PyPDF2 import PdfReader

def setup_driver(download_dir):
    """Configure ChromeDriver for PDF downloads"""
    chrome_options = Options()
    chrome_options.add_experimental_option('prefs', {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "plugins.always_open_pdf_externally": True,
        "safebrowsing.enabled": True
    })
    return webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )

def download_pdf(driver, url, filename):
    """Download PDF using Selenium and rename file"""
    driver.get(url)
    time.sleep(5)  # Wait for download to complete
    
    # Rename most recent PDF file
    files = sorted(
        [os.path.join(download_dir, f) for f in os.listdir(download_dir)],
        key=os.path.getctime,
        reverse=True
    )
    if files:
        os.rename(files[0], os.path.join(download_dir, filename))

def extract_data_from_pdf(pdf_path):
    """Extract required information from PDF pages 1-3"""
    patterns = {
        'cin': re.compile(r'\b([A-Z]\d{5}[A-Z]{2}\d{4}[A-Z]{3}\d{6})\b'),
        'email': re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'),
        'phone': re.compile(r'(\+91[\-\s]?[6-9]\d{9}|[6-9]\d{9}|\d{2,5}[-\s]?\d{5,8})'),
        'pan': re.compile(r'\b[A-Z]{5}[0-9]{4}[A-Z]\b'),
        'date': re.compile(r'\b(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/(\d{4})\b'),
        'website': re.compile(r'(?:https?://)?(?:www\.)?[a-zA-Z0-9-]+\.[a-zA-Z]{2,}(?:/\S*)?')
    }

    results = {key: [] for key in patterns}
    
    try:
        with open(pdf_path, 'rb') as file:
            reader = PdfReader(file)
            for page_num in [0, 1, 2]:  # Pages 1-3 (0-indexed)
                if page_num >= len(reader.pages):
                    continue
                
                text = reader.pages[page_num].extract_text()
                if not text:
                    continue
                
                # Clean text for better pattern matching
                text = text.replace('\n', ' ')
                
                # Find all matches for each pattern
                for key, pattern in patterns.items():
                    matches = pattern.findall(text)
                    if key == 'phone':
                        # Flatten tuple matches from groups
                        matches = [m for group in matches for m in group if m]
                    results[key].extend(matches)
                    
    except Exception as e:
        print(f"Error processing PDF: {e}")
    
    return results

def print_results(data, company):
    """Display extracted information in readable format"""
    print(f"\n{'='*40}\nResults for {company}\n{'='*40}")
    for key, values in data.items():
        print(f"\n{key.upper()} ({len(values)} found):")
        for v in set(values):  # Remove duplicates
            print(f"- {v}")

# Configuration
download_dir = os.path.join(os.getcwd(), 'downloads')
os.makedirs(download_dir, exist_ok=True)

# PDF URLs
pdf_urls = {
    'Airtel': 'https://assets.airtel.in/teams/simplycms/web/docs/Draft-Annual-Return-FY-2021-22.pdf',
    'Tata': 'https://www.tatamotors.com/wp-content/uploads/2023/10/Form-MGT-7.pdf'
}

# Main execution
driver = setup_driver(download_dir)

for company, url in pdf_urls.items():
    try:
        filename = os.path.join(download_dir, f"{company}_MGT-7.pdf")
        download_pdf(driver, url, filename)
        extracted_data = extract_data_from_pdf(filename)
        print_results(extracted_data, company)
    except Exception as e:
        print(f"Error processing {company}: {e}")

driver.quit()