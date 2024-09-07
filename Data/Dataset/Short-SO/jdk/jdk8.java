

public class jdk8 {
    public static void h1(){
        DecimalFormat df = new DecimalFormat("0.00", new DecimalFormatSymbols(Locale.FRANCE));
        System.out.println(df.format(""));
    }
}
