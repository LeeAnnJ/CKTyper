


public class jt8 {
    public static  int getFirstDayOfWeek() {
        return ((Calendar.getInstance().getFirstDayOfWeek() + 5) % 7) + 1;
    }

}
