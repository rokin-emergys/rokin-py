def remove_duplicates(data):
    """
    Remove duplicate elements from a list while maintaining the original order.

    Args:
        data (list): A list of elements which may contain duplicates.

    Returns:
        list: A list with duplicates removed, maintaining the original order.
    """
    seen = set()
    unique_data = []
    for item in data:
        if item not in seen:
            unique_data.append(item)
            seen.add(item)
    return unique_data
