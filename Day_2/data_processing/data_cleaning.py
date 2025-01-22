def remove_duplicates(data):
    """
    Remove duplicate elements from a list.

    Args:
        data (list): A list of elements which may contain duplicates.

    Returns:
        list: A list with duplicates removed, containing only unique elements.
    """
    return list(set(data))
