public class ArrayStatisticsDemo {
    public static void main(String[] args) {
        int[] scores = {72, 85, 91, 68, 94};
        int totalScore = 0;
        int highestScore = scores[0];

        for (int score : scores) {
            totalScore += score;
            if (score > highestScore) {
                highestScore = score;
            }
        }

        double averageScore = (double) totalScore / scores.length;

        System.out.println("Number of scores: " + scores.length);
        System.out.println("Total score: " + totalScore);
        System.out.printf("Average score: %.2f%n", averageScore);
        System.out.println("Highest score: " + highestScore);
    }
}