# Jay - Simple Calculator Program

def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero!")
    return a / b

def get_number(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def main():
    operations = {
        "1": ("Addition (+)", add),
        "2": ("Subtraction (-)", subtract),
        "3": ("Multiplication (*)", multiply),
        "4": ("Division (/)", divide),
    }

    print("=" * 30)
    print("  Jay's Simple Calculator")
    print("=" * 30)

    while True:
        print("\nSelect an operation:")
        for key, (name, _) in operations.items():
            print(f"  {key}. {name}")
        print("  5. Exit")

        choice = input("Enter choice (1-5): ").strip()

        if choice == "5":
            print("Goodbye!")
            break

        if choice not in operations:
            print("Invalid choice. Please try again.")
            continue

        num1 = get_number("Enter first number: ")
        num2 = get_number("Enter second number: ")

        name, operation = operations[choice]
        try:
            result = operation(num1, num2)
            print(f"\nResult: {num1} {name.split()[-1].strip('()')} {num2} = {result}")
        except ZeroDivisionError as e:
            print(f"\nError: {e}")

if __name__ == "__main__":
    main()
