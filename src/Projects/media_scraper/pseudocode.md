START

# Configure Logging
setup_logging()

# Define Scraping Function
function scrape_article(url, title_selector, content_selector):
    try:
        # Fetch Page Content
        page_content = fetch_webpage(url)

        # Parse HTML
        parsed_html = parse_html(page_content)

        # Extract Title
        title = extract_text(parsed_html, title_selector)

        # Extract Article Content
        content = extract_text(parsed_html, content_selector)

        # Clean Unwanted Elements
        cleaned_content = clean_html(content)

        # Convert to Markdown
        markdown_content = convert_to_markdown(cleaned_content)

        # Get Domain Name
        domain = extract_domain(url)

        # Save Article
        save_article(title, markdown_content, domain)

    except Exception as error:
        log_error(url, error)

# Scraping Functions for Specific News Sites
function scrape_indian_express(url):
    scrape_article(url, "h1[itemprop='headline']", "div[itemprop='articleBody']")

function scrape_the_hindu(url):
    scrape_article(url, "h1.title", "section.articlebodycontent")

# Main Execution
if running_as_main:
    scrape_indian_express("INDIAN_EXPRESS_URL")
    scrape_the_hindu("THE_HINDU_URL")

END
