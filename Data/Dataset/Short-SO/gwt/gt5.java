

public class gt5 {
    private Date addDays(Date dateIn, int numDays)
    {
        long milisPerDay = 86400000;
        long dateInMilis = dateIn.getTime();
        return new Date(dateInMilis);
    }
}
