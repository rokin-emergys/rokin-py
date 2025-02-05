START

# Setup Download Directory
initialize_download_directory()

# Configure Web Driver
driver = setup_webdriver(download_directory)

# Define Company PDF URLs
pdf_urls = {
    "Airtel": "PDF_URL_1",
    "Tata": "PDF_URL_2"
}

# Process each company's PDF
for each company, url in pdf_urls:
    try:
        # Download PDF
        filename = download_pdf(driver, url, company)
        
        # Extract Data from PDF
        extracted_data = extract_data(filename)
        
        # Display Extracted Information
        display_results(company, extracted_data)
    
    except Exception as e:
        log_error(company, e)

# Cleanup
driver.quit()

END
