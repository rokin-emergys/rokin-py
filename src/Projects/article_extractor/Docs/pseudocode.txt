START

# Load Configuration
load_config()

# Iterate over each company
for each company in company_list:
    
    # Iterate over each keyword for the current company
    for each keyword in keyword_list:
        
        # Construct search query
        query = construct_search_query(company, keyword)
        
        # Fetch news from search engines
        google_results = fetch_news("Google", query)
        bing_results = fetch_news("Bing", query)
        yahoo_results = fetch_news("Yahoo", query)
        
        # Extract relevant information from results
        google_data = extract_data(google_results)
        bing_data = extract_data(bing_results)
        yahoo_data = extract_data(yahoo_results)
        
        # Append results
        append_results(google_data)
        append_results(bing_data)
        append_results(yahoo_data)

# Save all results to CSV file
save_to_csv()

END
