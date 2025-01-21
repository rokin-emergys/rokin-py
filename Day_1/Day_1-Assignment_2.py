
# 1. Find unique elements across multiple lists.

# list1 = [1, 2, 3, 4, 5]
# list2 = [3, 4, 5, 6, 7]
# list3 = [5, 6, 7, 8, 9]

# all_elements = list1 + list2 + list3
# unique_elements = []

# for element in all_elements:
#     if all_elements.count(element) == 1:
#         unique_elements.append(element)

# print(unique_elements)

# 2. Group Tuples by First Element 
# Q. Given a list of tuples, group them by their first element and create a dictionary where the keys are the first elements, and the values are lists of corresponding second elements. 

# list4 = [(1, 2), (2, 3), (1, 4), (3, 5), (2, 6)]
# grouped_dict = {}

# for key, value in list4:
#     if key in grouped_dict:
#         grouped_dict[key].append(value)
#     else:
#         grouped_dict[key] = [value]

# print(grouped_dict)

# 3. Merge and Sort Multiple Lists
# q. Write a program that accepts three lists of integers, merges them into a single list, removes duplicates, and sorts the final list in descending order. 

# list1 = [1, 2, 3, 4, 5]
# list2 = [3, 4, 5, 6, 7]
# list3 = [5, 6, 7, 8, 9]

# merged_list = list1 + list2 + list3
# merged_list = list(set(merged_list))
# merged_list.sort(reverse=True)
# print(merged_list)  

# 4. Filter Tuples by Sum of Elements 
# q. Write a Python program to filter tuples from a given list where the sum of the elements in the tuple is greater than a specified threshold. 
'''
Example Input: [(1, 2), (3, 4), (5, 1), (2, 6)], Threshold = 6 
Expected Output: [(3, 4), (2, 6)] 
'''

# list5 = [(1, 2), (3, 4), (5, 1), (2, 6)]
# threshold = 6
# filtered_list = [tup for tup in list5 if sum(tup) > threshold] 
# print(filtered_list)

# 5. Calculate Statistics for List of Numbers
# q. Develop a program that takes a list of integers and calculates the following statistics using lambda functions:
# Mean 
# Median 
# Standard deviation 

# import math

# list6 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# mean = lambda lst: sum(lst) / len(lst)
# median = lambda lst: lst[len(lst) // 2] if len(lst) % 2 != 0 else (lst[len(lst) // 2] + lst[len(lst) // 2 - 1]) / 2
# std_dev = lambda lst: math.sqrt(sum([(x - mean(lst)) ** 2 for x in lst]) / len(lst))

# print(mean(list6))
# print(median(list6))
# print(std_dev(list6))

# 6. Find Longest Word in a List

# list7 = ['apple', 'banana', 'cherry', 'date', 'elderberry', 'fig', 'grape']
# longest_word = max(list7, key=len)
# print(longest_word)

# 7. Count Element Frequency in Nested Lists
'''Write a Python program to count the frequency of each element across all nested lists. 
Example Input: [[1, 2, 3], [2, 3, 4], [3, 4, 5]] 
Expected Output: {1: 1, 2: 2, 3: 3, 4: 2, 5: 1} '''

# list8 = [[1, 2, 3], [2, 3, 4], [3, 4, 5]]
# frequency_dict = {}

# for sublist in list8:
#     for element in sublist:
#         if element in frequency_dict:
#             frequency_dict[element] += 1
#         else:
#             frequency_dict[element] = 1

# print(frequency_dict)

# 8. Sort a Dictionary by Values

# dict1 = {'apple': 5, 'banana': 3, 'cherry': 4, 'date': 1, 'elderberry': 2}
# sorted_dict = dict(sorted(dict1.items(), key=lambda x: x[1]))
# print(sorted_dict)

# 9. Generate a Pascal’s Triangle

n = 5
pascal_triangle = [[1]]
for i in range(1, n):
    prev_row = pascal_triangle[-1]
    new_row = [1]
    for j in range(1, i):
        new_row.append(prev_row[j - 1] + prev_row[j])
    new_row.append(1)
    pascal_triangle.append(new_row)

# for row in pascal_triangle:
#     print(row)

# 10. Transform a List of Strings 
'''
Write a Python program that accepts a list of strings and transforms it into a list of tuples where: 
The first element of the tuple is the string in uppercase. 
The second element is the length of the string. 
The third element is the reversed string. 
Example Input: ['python', 'data', 'science'] 
Expected Output: [('PYTHON', 6, 'nohtyp'), ('DATA', 4, 'atad'), ('SCIENCE', 7, 'ecneics')] '''


# list9 = ['python', 'data', 'science']
# transformed_list = [(word.upper(), len(word), word[::-1]) for word in list9]
# print(transformed_list)
