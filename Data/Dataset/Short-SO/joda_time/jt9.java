

public class jt9 {
    public static void h1() {
        LocalDate today = LocalDate.now();
        ZonedDateTime zdt = today.atStartOfDay().atZone(ZoneId.systemDefault());
        OffsetDateTime odt = zdt.toOffsetDateTime();
    }
}
