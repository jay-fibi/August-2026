# Jay - Demo 1: Basic Calculator Functions

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


def power(a, b):
    return a ** b


def main():
    print("=" * 40)
    print("  Jay - Demo 1: Calculator")
    print("=" * 40)

    operations = [
        ("Addition", add, 12, 8),
        ("Subtraction", subtract, 12, 8),
        ("Multiplication", multiply, 12, 8),
        ("Division", divide, 12, 8),
        ("Power", power, 2, 10),
        ("Division by zero", divide, 12, 0),
    ]

    for name, operation, a, b in operations:
        try:
            print(f"{name:<18}: {a} and {b} -> {operation(a, b)}")
        except ZeroDivisionError as error:
            print(f"{name:<18}: {a} and {b} -> Error: {error}")


if __name__ == "__main__":
    main()
