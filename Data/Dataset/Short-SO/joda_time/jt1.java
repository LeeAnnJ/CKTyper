

public class jt1 {
    public static void f1(){
        DateTimeFormatter dtf = DateTimeFormat.forPattern("MM/dd/yyyy HH:mm:ss");
        DateTime jodatime = dtf.parseDateTime("");
    }

}
