public class MultiplicationTableDemo {
    public static void main(String[] args) {
        int tableNumber = 7;

        System.out.println("Multiplication table for " + tableNumber + ":");
        for (int multiplier = 1; multiplier <= 10; multiplier++) {
            int product = tableNumber * multiplier;
            System.out.println(tableNumber + " x " + multiplier + " = " + product);
        }
    }
}