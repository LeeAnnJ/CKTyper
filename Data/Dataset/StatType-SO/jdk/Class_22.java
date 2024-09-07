/*
Date: 1/19/17
URL: http://stackoverflow.com/questions/4637215/can-a-progress-bar-be-used-in-a-class-outside-main
*/


public class Class_22 {
	// @see http://stackoverflow.com/questions/4637215
	public class TwoRoot extends JFrame {

		private static final String s = "0.000000000000000";
		private JProgressBar progressBar = new JProgressBar(0, 100);
		private JLabel label = new JLabel(s, JLabel.CENTER);

		public TwoRoot() {
			this.setLayout(new GridLayout(0, 1));
			this.setTitle("???2");
			this.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
			this.add(progressBar);
			this.add(label);
			this.setSize(161, 100);
			this.setLocationRelativeTo(null);
			this.setVisible(true);
		}

		public void runCalc() {
			progressBar.setIndeterminate(true);
			TwoWorker task = new TwoWorker();
			task.addPropertyChangeListener(new PropertyChangeListener() {

				@Override
				public void propertyChange(PropertyChangeEvent e) {
					if ("progress".equals(e.getPropertyName())) {
						progressBar.setIndeterminate(false);
						progressBar.setValue((Integer) e.getNewValue());
					}
				}
			});
			task.execute();
		}

		private class TwoWorker extends SwingWorker<Double, Double> {

			private static final int N = 5;
			private final DecimalFormat df = new DecimalFormat(s);
			double x = 1;

			@Override
			protected Double doInBackground() throws Exception {
				for (int i = 1; i <= N; i++) {
					x = x - (((x * x - 2) / (2 * x)));
					setProgress(i * (100 / N));
					publish(Double.valueOf(x));
					Thread.sleep(1000); // simulate latency
				}
				return Double.valueOf(x);
			}

			@Override
			protected void process(List<Double> chunks) {
				for (double d : chunks) {
					label.setText(df.format(d));
				}
			}
		}

		public void main(String[] args) {
			EventQueue.invokeLater(new Runnable() {

				@Override
				public void run() {
					TwoRoot t = new TwoRoot();
					t.runCalc();
				}
			});
		}
	}

	JFrame progressFrame;
	JProgressBar progressBar;
	JLabel label = new JLabel("Calculating...");;
	Container pane;

	double amountSaved = 0;
	int i = 0;
	int iterations;

	public void createGui(int iterations) {
		//Create all components
		progressFrame = new JFrame("Calculation Progress");
		progressFrame.setSize(300, 100);
		pane = progressFrame.getContentPane();
		pane.setLayout(null);
		label = new JLabel("Calculating...");
		label.setBounds(115, 35, 200, 25);
		progressBar = new JProgressBar(0, iterations);
		progressBar.setBounds(10, 10, 280, 20);
		progressBar.setStringPainted(true);
		//Add components to pane
		pane.add(progressBar);
		pane.add(label);
		//Make frame visible
		progressFrame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		progressFrame.setResizable(false); //No resize
		progressFrame.setLocationRelativeTo(null);
		progressFrame.setVisible(true);
	}

	public void runCalcs(double MP, double StepAmt, double L1, double L2, double C1, double C2, double IM1, double IM2,
			double M1Start, double M2Start) {

		progressBar.setIndeterminate(false);
		TwoWorker task = new TwoWorker(MP, StepAmt, L1, L2, C1, C2, IM1, IM2, M1Start, M2Start);
		task.addPropertyChangeListener(new PropertyChangeListener() {

			@Override
			public void propertyChange(PropertyChangeEvent e) {
				if ("progress".equals(e.getPropertyName())) {
					progressBar.setIndeterminate(false);
					progressBar.setValue((Integer) e.getNewValue());
				}
			}
		});
		task.execute();
	} //end method runCalcs

	public class TwoWorker extends SwingWorker<Double, Double> {

		private final double MP, StepAmt, L1, L2, C1, C2, IM1, IM2, M1Start, M2Start;

		public TwoWorker(double MPa, double StepAmta, double L1a, double L2a, double C1a, double C2a, double IM1a,
				double IM2a, double M1Starta, double M2Starta) {

			MP = MPa;
			StepAmt = StepAmta;
			L1 = L1a;
			L2 = L2a;
			C1 = C1a;
			C2 = C2a;
			IM1 = IM1a;
			IM2 = IM2a;
			M1Start = M1Starta;
			M2Start = M2Starta;
		}

		@Override
		protected Double doInBackground() {

			double M1 = M1Start;
			double M2 = M2Start;

			// Set MinLoop as maximum to start
			// Loan 1
			double N1 = (Math.log10(1 - IM1 * L1 / M1) * -1) / Math.log10(1 + IM1);
			double M1Sum = M1 * N1;
			// Loan 2
			double N2 = (Math.log10(1 - IM2 * L2 / M2) * -1) / Math.log10(1 + IM2);
			double M2Sum = M2 * N2;
			double minLoop = M1Sum + M2Sum;
			double MTotal = 0;

			// Define variables for mins
			double MP1 = 0;
			double MP2 = 0;
			double NP1 = 0;
			double NP2 = 0;
			double MP1Sum = 0;
			double MP2Sum = 0;

			while (M1 <= MP - M2Start && M2 >= M2Start) {
				N1 = (Math.log10(1 - IM1 * L1 / M1) * -1) / Math.log10(1 + IM1);
				M1Sum = N1 * M1;
				N2 = (Math.log10(1 - IM2 * L2 / M2) * -1) / Math.log10(1 + IM2);
				M2Sum = N2 * M2;
				MTotal = M1Sum + M2Sum;
				if (MTotal < minLoop) {
					minLoop = MTotal;
					MP1 = M1;
					MP2 = M2;
					NP1 = N1;
					NP2 = N2;
					MP1Sum = M1Sum;
					MP2Sum = M2Sum;
				} // end if
				i++;
				progressBar.setValue(i);
				M1 = M1 + StepAmt;
				M2 = MP - M1;
				// Reset monthly sums
				M1Sum = 0;
				M2Sum = 0;
			} // end while

			System.out.printf("MP1 = %.2f\n", MP1);
			System.out.printf("MP2 = %.2f\n", MP2);
			System.out.printf("NP1 = %.2f\n", NP1);
			System.out.printf("NP2 = %.2f\n", NP2);
			System.out.printf("MP1Sum = %.2f\n", MP1Sum);
			System.out.printf("MP2Sum = %.2f\n", MP2Sum);
			System.out.printf("MTotal = %.2f\n", minLoop);
			System.out.printf("i = %d\n", i);
			System.out.printf("M1Start = %.2f\n", M1Start);
			System.out.printf("M2Start = %.2f\n", M2Start);
			System.out.printf("MP= %.2f\n", MP);

			// if there's a value for current payments, calculate amount saved
			if (C1 > 0) {
				double CN1 = (Math.log10(1 - IM1 * L1 / C1) * -1) / Math.log10(1 + IM1);
				double CT1 = CN1 * C1;

				double CN2 = (Math.log10(1 - IM2 * L2 / C2) * -1) / Math.log10(1 + IM2);
				double CT2 = CN2 * C2;

				double CTotal = CT1 + CT2;
				amountSaved = CTotal - minLoop;
			} // end if

			return null;

		} // end doInBackGround

		@Override
		protected void done() {
			label.setBounds(133, 35, 200, 25);
			label.setText("Done!");
		}
	} // end TwoWorker

	public double savedReturn() {
		return amountSaved;
	}
}