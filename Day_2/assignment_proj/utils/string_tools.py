def word_count(text):
    try:
        words = text.split()
        return len(words)
    except TypeError:
        return "Error: Input is not a string"
    except ValueError:
        return "Error: Value error occurred, invalid value"

def find_most_common_word(text):
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
    try:
        return ' '.join(text.split()[::-1])
    except TypeError:
        return "Error: Input is not a string"
    except ValueError:
        return "Error: Value error occurred, invalid value"

def check_palindrome(text):
    try:
        return text == text[::-1]
    except TypeError:
        return "Error: Input is not a string"
    except ValueError:
        return "Error: Value error occurred, invalid value"

