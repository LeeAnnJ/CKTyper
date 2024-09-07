

public class jdk1{

    static void h1() {
        IntBinaryOperator plusOperation = (a, b) -> a + b;
        System.out.println("Sum of 10,34 : " + plusOperation.applyAsInt(10, 34));
    }
}