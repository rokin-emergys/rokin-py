def print_results(data: dict, company: str) -> None:
    """This function displays the extracted information, categorizing it based on 
    predefined keys (e.g., CIN, email, phone, etc.). It formats the output neatly 
    to enhance readability.

    Args:
        data (dict): A dictionary containing extracted data, where keys are categories 
                     (e.g., "email", "phone") and values are sets of matched results.
        company (str): The name of the company associated with the extracted data.

    Returns:
        None
    """
    print(f"\n{'=' * 40}\nResults for {company}\n{'=' * 40}")
    for key, values in data.items():
        print(f"\n{key.upper()} ({len(values)} found):")
        for v in values:
            print(f"- {v}")
