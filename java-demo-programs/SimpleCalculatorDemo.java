public class SimpleCalculatorDemo {
    public static void main(String[] args) {
        double firstNumber = 18;
        double secondNumber = 5;

        System.out.println("Simple Calculator");
        System.out.println("-----------------");
        System.out.println("First number: " + formatNumber(firstNumber));
        System.out.println("Second number: " + formatNumber(secondNumber));
        System.out.println();

        System.out.println("Add:      " + formatNumber(add(firstNumber, secondNumber)));
        System.out.println("Subtract: " + formatNumber(subtract(firstNumber, secondNumber)));
        System.out.println("Multiply: " + formatNumber(multiply(firstNumber, secondNumber)));

        try {
            System.out.println("Divide:   " + formatNumber(divide(firstNumber, secondNumber)));
        } catch (ArithmeticException error) {
            System.out.println("Divide:   Error - " + error.getMessage());
        }

        System.out.println();
        System.out.println("Trying to divide by zero:");
        try {
            divide(firstNumber, 0);
        } catch (ArithmeticException error) {
            System.out.println("Divide:   Error - " + error.getMessage());
        }
    }

    public static double add(double firstNumber, double secondNumber) {
        return firstNumber + secondNumber;
    }

    public static double subtract(double firstNumber, double secondNumber) {
        return firstNumber - secondNumber;
    }

    public static double multiply(double firstNumber, double secondNumber) {
        return firstNumber * secondNumber;
    }

    public static double divide(double firstNumber, double secondNumber) {
        if (secondNumber == 0) {
            throw new ArithmeticException("Cannot divide by zero.");
        }
        return firstNumber / secondNumber;
    }

    private static String formatNumber(double number) {
        if (Double.isFinite(number) && number == Math.rint(number)
                && number >= Long.MIN_VALUE && number <= Long.MAX_VALUE) {
            return String.valueOf((long) number);
        }
        return String.valueOf(number);
    }
}
