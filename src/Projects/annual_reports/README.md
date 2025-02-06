# PDF Data Extraction and Processing

This script downloads PDF files from specified URLs, extracts specific data (such as CIN, email, phone number, PAN, date, and website) using regular expressions, and prints the results. It processes the PDF files asynchronously, using Python's `asyncio`, `aiohttp`, and `concurrent.futures` modules for efficient parallel downloads and data extraction.

## Features

- Downloads PDF files asynchronously from specified URLs.
- Extracts specific information from the first 3 pages of each PDF using regular expressions:
  - CIN (Corporate Identification Number)
  - Email addresses
  - Phone numbers (including Indian phone number formats)
  - PAN (Permanent Account Number)
  - Date in DD/MM/YYYY format
  - Website URLs
- Uses `concurrent.futures.ProcessPoolExecutor` for parallel PDF data extraction.
- Saves the downloaded PDFs to the `downloads/` directory.
- Stores extracted data in a CSV file within the `extracted_content/` directory.

## Requirements

- Python 3.7+
- Required Python packages:
  - `aiohttp` for asynchronous HTTP requests
  - `PyPDF2` for PDF parsing
  - `pandas` (optional, if you wish to store results in tabular format)

You can install the required dependencies with:

```bash
pip install aiohttp PyPDF2
```

## Directory Structure

```
report_analyzer/
├── Docs/                     # Flowchart and pseudocode
├── downloads/                # Directory where the downloaded PDFs will be saved
├── extracted_content/        # Directory where the extracted results (CSV files) will be saved
├── src/                      # Source folder containing the script
│   └── report_analyzer.py    # Python script for downloading PDFs and extracting data
└── README.md                 # This README file
```


## Script Overview

### 1. **Download PDFs**
   The script downloads PDFs from the URLs specified in the `pdf_urls` dictionary. Each company has its associated URL for the PDF document.

### 2. **Extract Data**
   The script uses the following regular expressions to extract data from the PDFs:
   - **CIN:** Corporate Identification Number.
   - **Email:** Email addresses.
   - **Phone:** Phone numbers (including Indian formats).
   - **PAN:** Permanent Account Number (PAN).
   - **Date:** Date in DD/MM/YYYY format.
   - **Website:** Website URLs (HTTP/HTTPS or WWW).

### 3. **Parallel Processing**
   - The script utilizes Python's `asyncio` and `aiohttp` for asynchronous downloading of PDFs.
   - Data extraction is parallelized using `ProcessPoolExecutor` for efficient multi-process execution.

### 4. **Results**
   - Extracted data is printed on the console, showing the results categorized by company and type of information (e.g., CIN, email, etc.).
   - The results are saved to a CSV file in the `extracted_content/` directory.

## How to Use

1. **Clone or Download** the repository to your local machine.

2. **Ensure Dependencies** are installed by running:
   
   ```bash
   pip install aiohttp PyPDF2
   ```

3. **Run the Script**:

   ```sh
   python src/report_analyzer.py
   ```

4. **Download Location**:
   - The downloaded PDFs will be saved in the `downloads/` directory.
   - The results (CSV file) will be saved in the `extracted_content/` directory.

5. **Configure the URLs** (Optional):
   - Modify the `pdf_urls` dictionary in the script to add or remove companies and their associated PDF URLs.

### Example `pdf_urls` Structure:

```python
pdf_urls = {
    'Company Name': 'https://example.com/your-pdf-url.pdf'
}
```

Add or remove companies as needed, and update their URLs accordingly.

## Output Example

For each company, the script will print results similar to:

```
========================================
Results for Airtel
========================================

CIN (1 found):
- A12345ABC1234ABC56789

EMAIL (2 found):
- example@domain.com
- contact@domain.com

PHONE (1 found):
- +91 9876543210

PAN (1 found):
- ABCDE1234F

DATE (1 found):
- 31/12/2021

WEBSITE (1 found):
- https://www.airtel.in
```

Additionally, the extracted results will be saved in the `extracted_content/` directory as `news_results_async.csv`.

## Notes

- The script processes only the first 3 pages of each PDF. This can be adjusted by modifying the range in the `extract_data()` function.
- The regular expressions used for extracting data may need to be adjusted depending on the specific formatting of the PDFs you're working with.
