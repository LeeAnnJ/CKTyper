//ID = 1352950


public class Android50 extends Activity {

	public static final String tag = "TipCalculator";

	/** Called when the activity is first created. */
	@Override
	public void onCreate(Bundle icicle) {
		super.onCreate(icicle);
		setContentView(R.layout.main);

		final EditText mealpricefield = (EditText) findViewById(100);
		final TextView answerfield = (TextView) findViewById(R.id.lay);

		final Button button = (Button) findViewById(101);
		button.setOnClickListener(new Button.OnClickListener() {
			public void onClick(View v) {
				try {
					Log.i(tag, "onClick invoked.");
					String mealprice = mealpricefield.getText().toString();

					Log.i(tag, "mealprice is [" + mealprice + "]");
					String answer = "";

					if (mealprice.indexOf("$") == -1) {
						mealprice = "$" + mealprice;
					}

					float fmp = 0.0F;

					NumberFormat nf = java.text.NumberFormat.getCurrencyInstance();

					fmp = nf.parse(mealprice).floatValue();

					fmp *= 1.2;

					Log.i(tag, "Total Meal Price (unformatted) is [" + fmp + "]");

					answer = "Full Price, including 20% Tip: " + nf.format(fmp);

					answerfield.setText(answer);

					Log.i(tag, "onClick Complete");

				} catch (java.text.ParseException pe) {
					Log.i(tag, "Parse exception caught");
					answerfield.setText("Failed to parse amount?");
				} catch (Exception e) {
					Log.e(tag, "Failed to Calculate Tip:" + e.getMessage());
					e.printStackTrace();
					answerfield.setText(e.getMessage());
				}
			}
		});
	}
}