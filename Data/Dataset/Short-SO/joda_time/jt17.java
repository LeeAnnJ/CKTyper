

public class jt17 {
    public static void h1(){
        String dateTime = "2015-07-18T13:32:56.971-0400";

        DateTimeFormatter formatter = DateTimeFormat.forPattern("yyyy-MM-dd'T'HH:mm:ss.SSSZZ")
                .withLocale(Locale.ROOT)
                .withChronology(ISOChronology.getInstanceUTC());
        DateTime dt = formatter.parseDateTime(dateTime);
    }
}
