import re
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from PyPDF2 import PdfReader

# Configuration
download_dir = os.path.join(os.getcwd(), 'downloads')
os.makedirs(download_dir, exist_ok=True)

# Selenium WebDriver Setup
def setup_driver():
    options = Options()
    options.add_experimental_option('prefs', {
        "download.default_directory": download_dir,
        "plugins.always_open_pdf_externally": True,
        "download.directory_upgrade": True
    })
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Download PDF
def download_pdf(driver, url, filename):
    driver.get(url)
    time.sleep(5)
    
    files = sorted(os.listdir(download_dir), key=lambda f: os.path.getctime(os.path.join(download_dir, f)), reverse=True)
    if files:
        latest_file = os.path.join(download_dir, files[0])
        
        # Remove existing file if it already exists
        if os.path.exists(filename):
            os.remove(filename)
        
        os.rename(latest_file, filename)


# Extract Data from PDF
def extract_data(pdf_path):
    patterns = {
        'cin': r'[A-Z]\d{5}[A-Z]{2}\d{4}[A-Z]{3}\d{6}',
        'email': r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}',
        'phone': r'(\+91[-\s]?[6-9]\d{9}|[6-9]\d{9}|\d{2,5}[-\s]?\d{5,8})',
        'pan': r'\b[A-Z]{5}[0-9]{4}[A-Z]\b',
        'date': r'\b(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/\d{4}\b',
        'website': r'\bhttps?://[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(?:/\S*)?\b|\bwww\.[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(?:/\S*)?\b'
    }
    results = {key: set() for key in patterns}
    
    try:
        reader = PdfReader(pdf_path)
        for page in reader.pages[:3]:
            text = page.extract_text() or ''
            for key, pattern in patterns.items():
                results[key].update(re.findall(pattern, text))
    except Exception as e:
        print(f"Error processing PDF: {e}")
    
    return results

# Print Results
def print_results(data, company):
    print(f"\n{'='*40}\nResults for {company}\n{'='*40}")
    for key, values in data.items():
        print(f"\n{key.upper()} ({len(values)} found):")
        for v in values:
            print(f"- {v}")

# Main Execution
pdf_urls = {
    'Airtel': 'https://assets.airtel.in/teams/simplycms/web/docs/Draft-Annual-Return-FY-2021-22.pdf',
    'Tata': 'https://www.tatamotors.com/wp-content/uploads/2023/10/Form-MGT-7.pdf'
}

driver = setup_driver()
for company, url in pdf_urls.items():
    try:
        filename = os.path.join(download_dir, f"{company}_MGT-7.pdf")
        download_pdf(driver, url, filename)
        print_results(extract_data(filename), company)
    except Exception as e:
        print(f"Error processing {company}: {e}")
driver.quit()
