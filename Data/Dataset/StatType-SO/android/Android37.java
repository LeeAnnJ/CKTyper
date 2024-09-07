//ID = 1111980

public class Android37 extends Activity implements Runnable {
    public ProgressDialog mProgress;

    // UI has a button that when pressed calls send

    public void send() {
         mProgress = ProgressDialog.show(this, "Please wait", 
                      "Please wait", 
                      true, true);
        Thread thread = new Thread(this);
        thread.start();
    }

    public void run() {
        try {
			Thread.sleep(10000);
		} catch (InterruptedException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
        Message msg = new Message();
        mHandler.sendMessage(msg);
    }

    private final Handler mHandler = new Handler() {
        @Override
        public void handleMessage(Message msg) {
            mProgress.dismiss();
        }
    };
}

