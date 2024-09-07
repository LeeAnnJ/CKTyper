

public class jt10 {
    public static void h1(){
        DateTime now = DateTime.now();
        DateTime dateTime = now.plusMinutes(10);
        Seconds seconds = Seconds.secondsBetween(now, dateTime);
    }
}
