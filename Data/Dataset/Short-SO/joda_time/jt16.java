


public class jt16 {
    public static int getDaysBetween(DateTime earlier, DateTime later)
    {
        return (int) TimeUnit.MILLISECONDS.toDays(later.getMillis()- earlier.getMillis());
    }

}
