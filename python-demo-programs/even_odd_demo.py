"""Demonstrate how to determine whether numbers are even or odd."""


def describe_number(number: int) -> str:
    """Return a message describing whether a number is even or odd."""
    number_type = "even" if number % 2 == 0 else "odd"
    return f"{number} is {number_type}."


def main() -> None:
    """Check a few example numbers."""
    numbers = [7, 12, 25, 40]

    for number in numbers:
        print(describe_number(number))


if __name__ == "__main__":
    main()