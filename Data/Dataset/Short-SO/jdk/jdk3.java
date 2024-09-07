

public class jdk3 {
    public static void h1(String oldDate, String format) throws ParseException {
        DateTimeFormatter dtf  = DateTimeFormatter.ofPattern(format);
        LocalDateTime dt = LocalDateTime.parse(oldDate, dtf);
        ZonedDateTime zdtzone = dt.atZone(ZoneId.of("America/Los_Angeles"));
    }
}
