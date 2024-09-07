
//ID = 6387723
public class JodaTime16 {
	public static void main(String[] args) 
	{
	DateTime d1 = new DateTime(2011, 6, 17, 13, 13, 5, 0) ;
	DateTime d2 = new DateTime(2011, 6, 17, 10, 17, 3, 0) ;

	Period negativePeriod = new Period(d1, d2);
	Period positivePeriod = new Period(d2, d1);

	PeriodFormatter pf = new PeriodFormatterBuilder()
	    .minimumPrintedDigits(2)
	    .appendHours()
	    .appendSuffix(":")
	    .rejectSignedValues(true) // Does this do anything?
	    .appendMinutes()
	    .appendSuffix(":")
	    .appendSeconds()
	    .toFormatter();

	System.out.printf("Negative Period: %s\n", pf.print(negativePeriod));
	System.out.printf("Positive Period: %s\n", pf.print(positivePeriod));
	}
}
