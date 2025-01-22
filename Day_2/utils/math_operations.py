def add(a, b):
    """
    Adds two numbers and returns a formatted string with the result.

    Parameters:
    a (int or float): The first number.
    b (int or float): The second number.

    Returns:
    str: A formatted string stating the sum of the two numbers.
    """
    return f"Sum of {a} and {b} is {a+b}"

def subtract(a, b):
    """
    Subtracts the second number from the first number and returns the result as a formatted string.

    Args:
        a (int or float): The first number.
        b (int or float): The second number.

    Returns:
        str: A string stating the difference between the two numbers.
    """
    return f"Difference of {a} and {b} is {a-b}"

def multiply(a, b):
    """
    Multiply two numbers and return the result as a formatted string.

    Args:
        a (int or float): The first number.
        b (int or float): The second number.

    Returns:
        str: A string stating the product of the two numbers.
    """
    return f"Product of {a} and {b} is {a*b}"

def divide(a, b):
    """
    Divide two numbers and handle division by zero.

    Args:
        a (float): The numerator.
        b (float): The denominator.

    Returns:
        str: The result of the division or an error message if division by zero occurs.
    """
    try:
        result = a / b
    except ZeroDivisionError:
        return "Cannot divide by zero"
    return f"Quotient of {a} and {b} is {result}"
