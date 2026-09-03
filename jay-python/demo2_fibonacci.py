# Jay - Demo 2: Fibonacci Series and Recursion

def fibonacci_iterative(count):
    """Return the first `count` Fibonacci numbers using a loop."""
    series = []
    current, following = 0, 1
    for _ in range(count):
        series.append(current)
        current, following = following, current + following
    return series


def fibonacci_recursive(position):
    """Return the Fibonacci number at `position` using recursion."""
    if position < 2:
        return position
    return fibonacci_recursive(position - 1) + fibonacci_recursive(position - 2)


def factorial(number):
    """Return the factorial of `number` using recursion."""
    if number < 0:
        raise ValueError("Factorial is not defined for negative numbers.")
    if number in (0, 1):
        return 1
    return number * factorial(number - 1)


def is_prime(number):
    """Return True when `number` is a prime number."""
    if number < 2:
        return False
    divisor = 2
    while divisor * divisor <= number:
        if number % divisor == 0:
            return False
        divisor += 1
    return True


def main():
    print("=" * 40)
    print("  Jay - Demo 2: Fibonacci and Recursion")
    print("=" * 40)

    print(f"First 10 Fibonacci numbers : {fibonacci_iterative(10)}")
    print(f"Fibonacci at position 12   : {fibonacci_recursive(12)}")
    print(f"Factorial of 6             : {factorial(6)}")

    primes = [number for number in range(2, 30) if is_prime(number)]
    print(f"Primes below 30            : {primes}")

    try:
        factorial(-3)
    except ValueError as error:
        print(f"Expected error             : {error}")


if __name__ == "__main__":
    main()
