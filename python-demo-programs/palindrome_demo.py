"""Demonstrate palindrome detection with text normalization."""


def is_palindrome(text: str) -> bool:
    """Return whether text reads the same forward and backward."""
    normalized_text = "".join(character.lower() for character in text if character.isalnum())
    return normalized_text == normalized_text[::-1]


def main() -> None:
    """Check several example phrases."""
    phrases = ["Racecar", "Never odd or even", "Hello, Python!"]

    for phrase in phrases:
        result = "is" if is_palindrome(phrase) else "is not"
        print(f'"{phrase}" {result} a palindrome.')


if __name__ == "__main__":
    main()