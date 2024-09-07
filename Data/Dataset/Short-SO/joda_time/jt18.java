

public class jt18 {
    public static void h1() throws ParseException {
        SimpleDateFormat sdf = new SimpleDateFormat("dd/MM/yyyy HH:mm:ss"); //  04/02/2011 20:27:05

        Date date = sdf.parse("dateValue");
        System.out.println(date);
    }
}
