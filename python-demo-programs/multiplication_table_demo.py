"""Display a multiplication table for an example number."""


def print_multiplication_table(number: int, limit: int = 10) -> None:
    """Print a multiplication table from 1 through the supplied limit."""
    print(f"Multiplication table for {number}")

    for multiplier in range(1, limit + 1):
        product = number * multiplier
        print(f"{number} x {multiplier} = {product}")


def main() -> None:
    """Print the first ten multiples of seven."""
    print_multiplication_table(7)


if __name__ == "__main__":
    main()