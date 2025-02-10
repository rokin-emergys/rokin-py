# PDF Data Extraction and Processing

This project is an asynchronous PDF data extraction tool that downloads PDF files from specified URLs, extracts key data elements using regular expressions, and prints the results. The tool leverages Python’s asynchronous capabilities (`asyncio` and `aiohttp`) together with multi-processing via `concurrent.futures.ProcessPoolExecutor` to efficiently download and process PDFs in parallel. The project has been modularized with helper functions stored in the `src/utils/` directory.

---

## Features

- **Asynchronous PDF Downloads:** Downloads PDF files from specified URLs concurrently.
- **Data Extraction:** Extracts key information from the first 3 pages of each PDF using regular expressions:
  - **CIN:** Corporate Identification Number
  - **Email:** Email addresses
  - **Phone:** Phone numbers (including various Indian formats)
  - **PAN:** Permanent Account Number
  - **Date:** Dates in DD/MM/YYYY format
  - **Website:** Website URLs (HTTP/HTTPS or WWW)
- **Parallel Processing:** Uses `ProcessPoolExecutor` to parallelize PDF data extraction.
- **Modular Design:** Helper functions for downloading, extraction, and printing are located in the `src/utils/` directory.
- **Output:** Downloads PDFs to the `downloads/` directory and stores extracted data as a CSV file in the `extracted_content/` directory.

---

## Requirements

- Python 3.7 or later
- Required Python packages:
  - `aiohttp` for asynchronous HTTP requests
  - `PyPDF2` for PDF parsing
  - `pandas` for saving results in tabular format

Install the required dependencies with:

```bash
pip install aiohttp PyPDF2 pandas
```

---

## Directory Structure

```
annual_reports/
├── Docs/                     
│   └── pseudocode.txt        # Flowcharts and pseudocode
├── downloads/                # Directory where the downloaded PDFs are saved
├── extracted_content/        # Directory where the extracted CSV results are saved
├── src/                      # Source code
│   ├── utils/                # Helper modules
│   │   ├── __init__.py
│   │   ├── downloader.py     # Contains the download_pdf() function
│   │   ├── extractor.py      # Contains the extract_data() function
│   │   └── printer.py        # Contains the print_results() function
│   └── main.py  # Asynchronous main script
└── README.md                 # This README file
```

---

## Script Overview

1. **Download PDFs:**  
   The script downloads PDF files from a dictionary of URLs. Each URL corresponds to a company’s PDF document.

2. **Extract Data:**  
   It uses regular expressions to extract specific data elements:
   - **CIN:** Corporate Identification Number
   - **Email:** Email addresses
   - **Phone:** Phone numbers
   - **PAN:** Permanent Account Number
   - **Date:** Dates in DD/MM/YYYY format
   - **Website:** Website URLs

3. **Parallel Processing:**  
   - **Asynchronous Downloads:** The script uses `asyncio` and `aiohttp` to download PDFs concurrently.
   - **Multi-Process Data Extraction:** Data extraction is parallelized using `ProcessPoolExecutor`.

4. **Results:**  
   - Extracted data is printed to the console with the results categorized by company and data type.
   - A CSV file containing the extracted data is saved in the `extracted_content/` directory.

---

## How to Use

1. **Clone or Download the Repository:**

   Clone or download the repository to your local machine.

2. **Install Dependencies:**

   Ensure that all required Python packages are installed by running:

   ```bash
   pip install aiohttp PyPDF2 pandas
   ```

3. **Configure the URLs (Optional):**

   If needed, update the `pdf_urls` dictionary in the script (inside `src/report_analyzer_async.py`) to add or remove companies and their associated PDF URLs. For example:

   ```python
   pdf_urls = {
       'Airtel': 'https://assets.airtel.in/teams/simplycms/web/docs/Draft-Annual-Return-FY-2021-22.pdf',
       'Tata': 'https://www.tatamotors.com/wp-content/uploads/2023/10/Form-MGT-7.pdf'
   }
   ```

4. **Run the Script:**

   From the project root, run the asynchronous script with:

   ```sh
   python src/main.py
   ```

5. **Output Locations:**

   - **Downloaded PDFs:** Saved in the `downloads/` directory.
   - **Extracted Data:** The CSV file containing the extracted data is saved in the `extracted_content/` directory.

---

## Output Example

For each company, the script prints results similar to:

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

Additionally, the extracted results are saved as a CSV file in the `extracted_content/` directory.

---

## Notes

- **Page Processing:**  
  The script processes only the first 3 pages of each PDF. You can adjust this behavior by modifying the page range in the `extract_data()` function.

- **Regular Expressions:**  
  The regular expressions used for data extraction may need adjustment based on the formatting of the PDFs you are working with.

---
