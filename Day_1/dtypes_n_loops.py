# Integer
my_int = 10
print("Integer:", my_int)

# Float
my_float = 10.5
print("Float:", my_float)

# String
my_string = "Hello, World!"
print("String:", my_string)

# Boolean
my_bool = True
print("Boolean:", my_bool)

# List
my_list = [1, 2, 3, 4, 5]
print("List:", my_list)

# Tuple
my_tuple = (1, 2, 3, 4, 5)
print("Tuple:", my_tuple)

# Set
my_set = {1, 2, 3, 4, 5}
print("Set:", my_set)

# Dictionary
my_dict = {"name": "Rajeev", "age": 21}
print("Dictionary:", my_dict)

# NoneType
my_none = None
print("NoneType:", my_none)


# For loop
print("For loop:")
for i in range(5):
    print(i)

# While loop
print("While loop:")
i = 0
while i < 5:
    print(i)
    i += 1

# Nested loop
print("Nested loop:")
for i in range(3):
    for j in range(2):
        print(f"i: {i}, j: {j}")

# Loop with else
print("Loop with else:")
for i in range(5):
    print(i)
else:
    print("Loop completed")

# Break statement
print("Break statement:")
for i in range(5):
    if i == 3:
        break
    print(i)

# Continue statement
print("Continue statement:")
for i in range(5):
    if i == 3:
        continue
    print(i)

# write a program to print the first 10 numbers and in each iteration print sum of current and previous number
sum = 0
for i in range(1, 11):
    sum += i
    print(f"Current number: {i}, Sum: {sum}")