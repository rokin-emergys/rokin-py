def word_count(text):
    """Function to count the number of words in a given text
    Args:
        text (str): The text to be analyzed
    Returns:
        int: Number of words in the text
    """
    try:
        words = text.split()
        return len(words)
    except TypeError:
        return "Error: Input is not a string"
    except ValueError:
        return "Error: Value error occurred, invalid value"

def find_most_common_word(text):
    """Function to find the most common word in a given text
    Args:
        text (str): The text to be analyzed
    Returns:
        str: The most common word in the text
    """
    try:
        if text.strip():
            words = text.split()
            word_counts = {}
            for word in words:
                word_counts[word] = word_counts.get(word, 0) + 1
            return max(word_counts, key=word_counts.get)
        return "Error: Input is either empty or not a valid string"
    except TypeError:
        return "Error: Input is not a string"
    except ValueError:
        return "Error: Value error occurred, invalid value"

def reverse_words(text):
    """Function to reverse the words in a given text
    Args:
        text (str): The text to be reversed
    Returns:
        str: The reversed text
    """
    try:
        return ' '.join(text.split()[::-1])
    except TypeError:
        return "Error: Input is not a string"
    except ValueError:
        return "Error: Value error occurred, invalid value"

def check_palindrome(text):
    """Function to check if a given text is a palindrome
    Args:
        text (str): The text to be checked
    Returns:
        bool: True if the text is a palindrome, False otherwise
    """
    try:
        return text == text[::-1]
    except TypeError:
        return "Error: Input is not a string"
    except ValueError:
        return "Error: Value error occurred, invalid value"

