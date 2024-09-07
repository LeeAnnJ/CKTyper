

public class gt6 {
    public static void h1(){
        long time = System.currentTimeMillis();
        long milisPerYear = new BigInteger("31536000000").longValue();
        String currentYear = String.valueOf((int) Math.floor(time / milisPerYear) + 1970);
    }
}
