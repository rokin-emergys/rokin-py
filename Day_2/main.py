from data_processing.data_cleaning import remove_duplicates
from utils.math_operations import *

'''
Use the functions from both modules to perform the following tasks: 
1. Calculate the sum, difference, product, and quotient of two numbers. 
2. Remove duplicates from a list of data. '''

# Task 1. Calculate the sum, difference, product, and quotient of two numbers. 
num1 = 10
num2 = 5

print(add(num1, num2))
print(subtract(num1, num2))
print(multiply(num1, num2))
print(divide(num1, num2))

# Task 2. Remove duplicates from a list of data.

data = [1, 2, 3, 4, 5, 1, 2, 3, 4, 5]
print(f"Data before removing duplicates: {data}")

data = remove_duplicates(data)
print(f"Data after removing duplicates: {data}")
