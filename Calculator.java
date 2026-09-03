import java.util.Scanner;

public class Calculator {
    private static final Scanner INPUT_SCANNER = new Scanner(System.in);

    public static void main(String[] args) {
        System.out.println("Java Calculator");
        System.out.println("---------------");

        boolean keepRunning = true;
        while (keepRunning) {
            printMenu();
            int menuChoice = readMenuChoice();

            if (menuChoice == 7) {
                keepRunning = false;
                continue;
            }

            double firstNumber = readNumber("Enter the first number: ");
            double secondNumber = readNumber("Enter the second number: ");
            calculateAndDisplay(menuChoice, firstNumber, secondNumber);
            System.out.println();
        }

        System.out.println("Thank you for using the calculator!");
        INPUT_SCANNER.close();
    }

    private static void printMenu() {
        System.out.println("Choose an operation:");
        System.out.println("1. Add (+)");
        System.out.println("2. Subtract (-)");
        System.out.println("3. Multiply (*)");
        System.out.println("4. Divide (/)");
        System.out.println("5. Modulo (%)");
        System.out.println("6. Power (^)");
        System.out.println("7. Exit");
    }

    private static int readMenuChoice() {
        while (true) {
            System.out.print("Enter your choice (1-7): ");
            String userInput = INPUT_SCANNER.nextLine().trim();

            try {
                int menuChoice = Integer.parseInt(userInput);
                if (menuChoice >= 1 && menuChoice <= 7) {
                    return menuChoice;
                }
            } catch (NumberFormatException ignored) {
                // The validation message below applies to non-integer input too.
            }

            System.out.println("Invalid choice. Please enter a number from 1 to 7.");
        }
    }

    private static double readNumber(String prompt) {
        while (true) {
            System.out.print(prompt);
            String userInput = INPUT_SCANNER.nextLine().trim();

            try {
                double parsedNumber = Double.parseDouble(userInput);
                if (Double.isFinite(parsedNumber)) {
                    return parsedNumber;
                }
            } catch (NumberFormatException ignored) {
                // The validation message below applies to malformed input too.
            }

            System.out.println("Invalid number. Please enter a finite numeric value.");
        }
    }

    private static void calculateAndDisplay(
            int menuChoice, double firstNumber, double secondNumber) {
        double result;
        String operator;

        switch (menuChoice) {
            case 1:
                result = firstNumber + secondNumber;
                operator = "+";
                break;
            case 2:
                result = firstNumber - secondNumber;
                operator = "-";
                break;
            case 3:
                result = firstNumber * secondNumber;
                operator = "*";
                break;
            case 4:
                if (secondNumber == 0) {
                    System.out.println("Error: Cannot divide by zero.");
                    return;
                }
                result = firstNumber / secondNumber;
                operator = "/";
                break;
            case 5:
                if (secondNumber == 0) {
                    System.out.println("Error: Cannot calculate modulo by zero.");
                    return;
                }
                result = firstNumber % secondNumber;
                operator = "%";
                break;
            case 6:
                result = Math.pow(firstNumber, secondNumber);
                operator = "^";
                break;
            default:
                throw new IllegalArgumentException("Unsupported menu choice: " + menuChoice);
        }

        System.out.printf("Result: %s %s %s = %s%n",
                formatNumber(firstNumber),
                operator,
                formatNumber(secondNumber),
                formatNumber(result));
    }

    public static double squareRoot(double number) {
        return Math.sqrt(number);
    }

    public static double percentage(double number, double percentage) {
        return number * percentage / 100;
    }

    public static long factorial(int number) {
        if (number < 0) {
            throw new IllegalArgumentException("Factorial is not defined for negative numbers.");
        }
        if (number > 20) {
            throw new ArithmeticException("Factorial result exceeds the range of long.");
        }

        long factorialResult = 1;
        for (int factor = 2; factor <= number; factor++) {
            factorialResult *= factor;
        }
        return factorialResult;
    }

    public static double average(double firstNumber, double secondNumber) {
        return firstNumber / 2 + secondNumber / 2;
    }

    private static String formatNumber(double number) {
        if (Double.isFinite(number) && number == Math.rint(number)
                && number >= Long.MIN_VALUE && number <= Long.MAX_VALUE) {
            return String.valueOf((long) number);
        }
        return String.valueOf(number);
    }
}