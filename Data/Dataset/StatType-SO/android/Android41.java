//ID = 1182620

public class Android41 extends View {
	public Android41(Context context) {
		super(context);
		setBackgroundColor(Color.RED);
	}

	TextView tv;

	public void adText(TextView tv) {
		this.tv = tv;
		tv.setVisibility(tv.VISIBLE);
	}
}
