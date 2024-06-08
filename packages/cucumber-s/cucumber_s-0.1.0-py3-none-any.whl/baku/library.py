objectives = [
    "Count the number of characters in a string",
    "Count the number of words in a string",
    "Count the number of occurrences of a character in a string",
    "Count the number of vowels and consonants in a string",
    "Count even and odd numbers in a list",
    "Perform various string operations on 'Bring It On'",
    "Perform various string operations on 'Bamboozled'",
    "Find the factorial of a number by recursion and using a predefined function",
    "Filter only even numbers from a given list",
    "Print specific patterns",
    "Create a module and use it in another program",
    "Store student data using a dictionary",
    "Display basic operations on an array",
    "Perform operations on a list of names",
    "Check if a number is prime",
    "Generate a Fibonacci sequence"
]

programs = [
    """
    string = input("Enter a string: ")
    print("Number of characters:", len(string))
    """,
    """
    string = input("Enter a string: ")
    print("Number of words:", len(string.split()))
    """,
    """
    string = input("Enter a string: ")
    char = input("Enter a character to count: ")
    print(f"Number of occurrences of {char}:", string.count(char))
    """,
    """
    string = input("Enter a string: ")
    vowels = "aeiouAEIOU"
    v_count = sum(1 for char in string if char in vowels)
    c_count = sum(1 for char in string if char.isalpha() and char not in vowels)
    print("Number of vowels:", v_count)
    print("Number of consonants:", c_count)
    """,
    """
    numbers = [int(input()) for _ in range(int(input("Enter the range of numbers: ")))]
    evens = sum(1 for num in numbers if num % 2 == 0)
    odds = len(numbers) - evens
    print("Total even numbers:", evens)
    print("Total odd numbers:", odds)
    """,
    """
    text = "Bring It on"
    print(text.upper())
    print(text.lower())
    print(text.capitalize())
    print(text.title().swapcase())
    """,
    """
    text = "Bamboozled"
    print(text[:2])
    print(text[-2:])
    print(text.lower())
    print(text[:6])
    print(text[::-1])
    """,
    """
    import math
    def factorial_recursive(n):
        return 1 if n == 0 else n * factorial_recursive(n-1)
    num1 = int(input("Enter a number: "))
    num2 = int(input("Enter another number: "))
    print("Factorial by recursion:", factorial_recursive(num1))
    print("Factorial by predefined function:", math.factorial(num2))
    """,
    """
    numbers = [int(input()) for _ in range(int(input("Enter the size of the list: ")))]
    evens = list(filter(lambda x: x % 2 == 0, numbers))
    print("Filtered even elements:", evens)
    """,
    """
    # Pattern a
    for _ in range(10):
        print('*' * 10)

    # Pattern b
    for i in range(1, 11):
        print(str(i) * 10)
    """,
    """
    # my_module.py
    def add(a, b): return a + b
    def sub(a, b): return a - b
    def mul(a, b): return a * b
    def div(a, b): return a / b
    def mod(a, b): return a % b
    def exp(a, b): return a ** b
    def floor(a, b): return a // b

    # my_program.py
    import my_module as md
    a = int(input("Enter a number: "))
    b = int(input("Enter another number: "))
    print("Addition:", md.add(a, b))
    print("Subtraction:", md.sub(a, b))
    print("Multiplication:", md.mul(a, b))
    print("Division:", md.div(a, b))
    print("Modulus:", md.mod(a, b))
    print("Exponentiation:", md.exp(a, b))
    print("Floor Division:", md.floor(a, b))
    """,
    """
    students = {
        "Alice": {"roll_number": 123, "marks": {"Math": 85.5, "Science": 92.0, "English": 78.0}},
        "Bob": {"roll_number": 456, "marks": {"Math": 72.5, "Science": 88.0, "English": 90.0}}
    }
    def access_student(name):
        if name in students:
            info = students[name]
            print(f"Student Name: {name}")
            print(f"Roll Number: {info['roll_number']}")
            print("Marks:", ", ".join(f"{subject}: {mark}" for subject, mark in info["marks"].items()))
        else:
            print(f"Student named {name} not found.")
    access_student("Alice")
    """,
    """
    import array as arr
    a = arr.array('i', [1, 2, 3, 4, 5])
    print("Array:", a)
    a.append(6)
    print("After append:", a)
    a.insert(1, 9)
    print("After insert:", a)
    a.remove(3)
    print("After remove:", a)
    print("Index of 4:", a.index(4))
    a.reverse()
    print("Reversed array:", a)
    """,
    """
    names = ["Anil", "Anmol", "Aditya", "Alka", "Avi"]
    print("Names in the list:", names)
    names.insert(2, "Anuj")
    print("Insert 'Anuj' in the list:", names)
    names.append("Bhumika")
    print("Append the name 'Bhumika' to the list:", names)
    names.remove("Avi")
    print("Remove 'Avi' from the list:", names)
    names[0] = "Anil Kumar"
    print("Replace 'Anil' with 'Anil Kumar':", names)
    names.sort()
    print("Sort the list:", names)
    names.reverse()
    print("Reverse the list:", names)
    print("Length of the list:", len(names))
    """,
    """
    def is_prime(n):
        if n <= 1:
            return False
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0:
                return False
        return True
    num = int(input("Enter a number: "))
    print(f"{num} is prime:", is_prime(num))
    """,
    """
    def fibonacci(n):
        fib_seq = [0, 1]
        while len(fib_seq) < n:
            fib_seq.append(fib_seq[-1] + fib_seq[-2])
        return fib_seq
    num = int(input("Enter the number of terms: "))
    print("Fibonacci sequence:", fibonacci(num))
    """
]

def select_program():
    print("Select a program objective by number:")
    for i, objective in enumerate(objectives, 1):
        print(f"{i}. {objective}")
    choice = int(input("Enter the program number: "))
    if 1 <= choice <= len(programs):
        return programs[choice - 1]
    else:
        print("Invalid choice. Please try again.")
        return select_program()

def create_python_file():
    program_code = select_program()
    filename = input("Enter the filename (without .py extension): ") + ".py"
    with open(filename, "w") as file:
        file.write(program_code)
    print(f"Python file '{filename}' created successfully.")

if __name__ == "__main__":
    create_python_file()
