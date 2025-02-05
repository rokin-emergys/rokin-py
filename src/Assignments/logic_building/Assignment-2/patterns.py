def hollow_pyramid(n):
    for i in range(n):
        for j in range(n - i - 1):
            print(" ", end="")

        for j in range(2 * i + 1):
            if j == 0 or j == 2 * i or i == n - 1:
                print("*", end="")
            else:
                print(" ", end="")
        print()

n = 5
# hollow_pyramid(n)

def rev_hollow_pyramid(n):
    for i in range(n):
        spaces = i
        stars = 2*(n-i)-1

        print(" "*spaces, end="")

        for j in range(stars):
            if j == 0 or j == stars - 1  or i == 0:
                print("*", end="")
            else:
                print(" ", end="")
        print()

# rev_hollow_pyramid(n)

def right_triangle(n):
    for i in range(n+1):
        for j in range(i):
            print("*", end="")
        print()

# right_triangle(n)

def rev_right_triangle(n):
    for i in range(n+1):
        for j in range(n-i):
            print("*", end="")
        print()

# rev_right_triangle(n)

def h_pyramid(n):
    for i in range(1, n+1):
        print("*"*i)
    for j in range(n-1, 0, -1):
        print("*"*j)

# h_pyramid(n)

def A_of_stars(n):
    for i in range(n):
        for j in range((2 * n) - 1):
            if (j == n - i - 1) or (j == n + i - 1) or (i == n // 2 and j > n - i - 1 and j < n + i - 1):
                print("*", end="")
            else:
                print(" ", end="")
        print()

# A_of_stars(n)

def number_pattern(n):
    for i in range(n+1):
        for j in range(1, i+1):
            print(j, end="")
        print()

number_pattern(n)