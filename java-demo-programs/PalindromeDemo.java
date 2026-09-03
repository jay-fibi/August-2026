public class PalindromeDemo {
    public static void main(String[] args) {
        String originalText = "Never odd or even";
        String normalizedText = originalText.replaceAll("[^a-zA-Z0-9]", "").toLowerCase();
        String reversedText = new StringBuilder(normalizedText).reverse().toString();
        boolean isPalindrome = normalizedText.equals(reversedText);

        System.out.println("Text: " + originalText);
        System.out.println("Is palindrome: " + isPalindrome);
    }
}