"""Calculate basic statistics for a list of numbers."""


def calculate_statistics(numbers: list[float]) -> dict[str, float]:
    """Return the minimum, maximum, total, and average of a non-empty list."""
    if not numbers:
        raise ValueError("The numbers list cannot be empty.")

    return {
        "minimum": min(numbers),
        "maximum": max(numbers),
        "total": sum(numbers),
        "average": sum(numbers) / len(numbers),
    }


def main() -> None:
    """Calculate and display statistics for example scores."""
    scores = [82.5, 91.0, 76.5, 88.0, 95.0]
    statistics = calculate_statistics(scores)

    print(f"Scores: {scores}")
    print(f"Minimum: {statistics['minimum']}")
    print(f"Maximum: {statistics['maximum']}")
    print(f"Total: {statistics['total']}")
    print(f"Average: {statistics['average']:.2f}")


if __name__ == "__main__":
    main()