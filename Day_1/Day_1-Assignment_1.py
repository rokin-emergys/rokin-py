# 1. Write a program to remove the occurrence of a specified element from an array.
sample_list = [1, 2, 3, 4, 2, 5, 2, 6]
value_to_remove = 2
for x in sample_list:
    if x == value_to_remove:
        sample_list.remove(x)
print(sample_list)

# 2. Find instersection of two lists.
# list1 = [1, 2, 3, 4, 5]
# list2 = [3, 4, 5, 6, 7]
# intersection = [x for x in list1 if x in list2]
# print(intersection)

# 3. get smallest and largest from a list.
# list3 = [1, 2, 3, 4, 5]
# print(f"Smallest: {min(list3)} and Largest: {max(list3)}")

# 4. Write a Python program to get a list, sorted in increasing order by the last element in each tuple from a given list of non-empty tuples 
'''
Sample list = [(2, 5), (1, 2), (4, 4), (2, 3), (2, 1)] 
Expected output = [(2, 1), (1, 2), (2, 3), (4, 4), (2, 5)] 
# # '''
# list4 = [(2, 5), (1, 2), (4, 4), (2, 3), (2, 1)]

# for i in range(len(list4)):
#     for j in range(i + 1, len(list4)):
#         if list4[i][1] > list4[j][1]:
#             list4[i], list4[j] = list4[j], list4[i]
#
# print(list4)        

# 5. write a python program to make star pattern.
 
# n = 5
# for i in range(n):
#     print(" " * (n - i - 1) + "*"  * (2 * i + 1))
# for i in range(n - 2, -1, -1):
#     print(" " * (n - i - 1) + "*" * (2 * i + 1))

# 6. 
'''Develop a program to calculate the final grades of students based on their scores in three exams: Exam 1, Exam 2, and Exam 3. The final grade is calculated as follows: 
If the average score is greater than or equal to 90, the grade is 'A'. 
If the average score is greater than or equal to 80 and less than 90, the grade is 'B'. 
If the average score is greater than or equal to 70 and less than 80, the grade is 'C'. 
If the average score is greater than or equal to 60 and less than 70, the grade is 'D'. 
If the average score is less than 60, the grade is 'F'. '''

# num_students = int(input("Enter the number of students: "))
# students = []

# for _ in range(num_students):
#     name = input("Enter the student's name: ")
#     exam1 = float(input("Enter the score for Exam 1: "))
#     exam2 = float(input("Enter the score for Exam 2: "))
#     exam3 = float(input("Enter the score for Exam 3: "))
    
#     average_score = (lambda e1, e2, e3: (e1 + e2 + e3) / 3)(exam1, exam2, exam3)
    
#     if average_score >= 90:
#         grade = 'A'
#     elif average_score >= 80:
#         grade = 'B'
#     elif average_score >= 70:
#         grade = 'C'
#     elif average_score >= 60:
#         grade = 'D'
#     else:
#         grade = 'F'
    
#     students.append({
#         'name': name,
#         'exam1': exam1,
#         'exam2': exam2,
#         'exam3': exam3,
#         'average_score': average_score,
#         'grade': grade
#     })

# print("\nStudent Data:")
# print(f"{'Name':<15}{'Exam 1':<10}{'Exam 2':<10}{'Exam 3':<10}{'Average':<10}{'Grade':<5}")
# for student in students:
#     print(f"{student['name']:<15}{student['exam1']:<10}{student['exam2']:<10}{student['exam3']:<10}{student['average_score']:<10.2f}{student['grade']:<5}")

 