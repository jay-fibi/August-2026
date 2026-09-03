# Jay - Demo 3: String Utilities and Word Counter

from collections import Counter

SAMPLE_TEXT = (
    "Python is simple. Python is powerful. "
    "Simple code is readable code, and readable code is maintainable."
)


def clean_words(text):
    """Split `text` into lowercase words without punctuation."""
    cleaned = "".join(char.lower() if char.isalnum() else " " for char in text)
    return cleaned.split()


def word_frequency(text, top=5):
    """Return the `top` most common words in `text`."""
    return Counter(clean_words(text)).most_common(top)


def is_palindrome(text):
    """Return True when `text` reads the same forwards and backwards."""
    letters = [char.lower() for char in text if char.isalnum()]
    return letters == letters[::-1]


def reverse_words(text):
    """Return `text` with the order of its words reversed."""
    return " ".join(text.split()[::-1])


def count_vowels(text):
    """Return the number of vowels in `text`."""
    return sum(1 for char in text.lower() if char in "aeiou")


def main():
    print("=" * 40)
    print("  Jay - Demo 3: String Utilities")
    print("=" * 40)

    print(f"Sample text: {SAMPLE_TEXT}\n")
    print(f"Total words   : {len(clean_words(SAMPLE_TEXT))}")
    print(f"Unique words  : {len(set(clean_words(SAMPLE_TEXT)))}")
    print(f"Vowel count   : {count_vowels(SAMPLE_TEXT)}")

    print("\nTop 5 words:")
    for word, count in word_frequency(SAMPLE_TEXT):
        print(f"  {word:<14} {'*' * count} ({count})")

    print("\nPalindrome checks:")
    for phrase in ["Racecar", "A man, a plan, a canal: Panama", "Hello Jay"]:
        print(f"  {phrase!r:<35} -> {is_palindrome(phrase)}")

    print(f"\nReversed words: {reverse_words('Jay writes clean Python code')}")


if __name__ == "__main__":
    main()
