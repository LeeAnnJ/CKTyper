//ID = 1188346
public class Android42 extends Activity implements OnErrorListener, 

OnBufferingUpdateListener,
OnCompletionListener, OnPreparedListener, SurfaceHolder.Callback{

private static final String TAG = "MediaPreview";

private MediaPlayer mp;
private SurfaceView mPreview;
private SurfaceHolder holder;
private Button btnPlay;
private Button btnPause;
private Button btnReset;
private Button btnStop;

private String mPath;

@Override
protected void onCreate(Bundle savedInstanceState) {

    super.onCreate(savedInstanceState);
    setContentView(R.layout.media_preview);

    mPreview = (SurfaceView)findViewById(R.id.myImage);
    btnPlay = (Button)findViewById(100);
    btnPause = (Button)findViewById(101);
    btnReset = (Button)findViewById(102);
    btnStop = (Button)findViewById(103);

    getPathFromParentDialog();

    btnPlay.setOnClickListener(new View.OnClickListener(){

        @Override
        public void onClick(View v) {
            playVideo();
        }
    });

    btnPause.setOnClickListener(new View.OnClickListener(){

        @Override
        public void onClick(View v) {
            // TODO Auto-generated method stub
            if(mp != null){
                mp.pause();
            }
        }
    });

    btnReset.setOnClickListener(new View.OnClickListener(){

        @Override
        public void onClick(View v) {
            if(mp != null){
                mp.seekTo(0);
            }
        }
    });

    btnStop.setOnClickListener(new View.OnClickListener(){

        @Override
        public void onClick(View v) {
            if(mp != null){
                mp.stop();
                mp.release();
            }
        }
    });

    getWindow().setFormat(PixelFormat.TRANSPARENT);
    holder = mPreview.getHolder();
    holder.addCallback(this);
    holder.setFixedSize(400, 300);
}

@Override
protected void onResume() {

    setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_LANDSCAPE);
    super.onResume();
}

@Override
public boolean onError(MediaPlayer mp, int what, int extra) {
    if(mp != null){
        mp.stop();
        mp.release();
    }
    return false;
}

@Override
public void onBufferingUpdate(MediaPlayer mp, int percent) {
    // TODO Auto-generated method stub

}

@Override
public void onCompletion(MediaPlayer mp) {
    // TODO Auto-generated method stub

}

@Override
public void onPrepared(MediaPlayer mp) {
    // TODO Auto-generated method stub

}

@Override
public void surfaceChanged(SurfaceHolder holder, int format, int width,
        int height) {
    // TODO Auto-generated method stub

}

@Override
public void surfaceCreated(SurfaceHolder holder) {
    // TODO Auto-generated method stub

}

@Override
public void surfaceDestroyed(SurfaceHolder holder) {
    // TODO Auto-generated method stub

}

private void playVideo() {
    try{
        mp = new MediaPlayer();
        mp.setOnErrorListener(this);
        mp.setOnBufferingUpdateListener(this);
        mp.setOnCompletionListener(this);
        mp.setOnPreparedListener(this);
        mp.setAudioStreamType(2);

        mp.setDisplay(mPreview.getHolder());
        Runnable r = new Runnable(){
            @Override
            public void run() {
                try{
                    setDataSource(mPath);
                }
                catch(Exception ex){
                    Log.e(TAG, ex.getMessage());
                }
                try {
                    mp.prepare();
                    Log.v(TAG, "Duration: ===> " + mp.getDuration());
                } catch (IllegalStateException e) {
                    // TODO Auto-generated catch block
                    e.printStackTrace();
                } catch (IOException e) {
                    // TODO Auto-generated catch block
                    e.printStackTrace();
                    Log.e(TAG, e.getMessage());
                }
                mp.start();
            }

        };
        new Thread(r).start();
    }
    catch(Exception ex){
        String sDummy = ex.toString();
        if(mp != null){
            mp.stop();
            mp.release();
        }
    }

}

private void setDataSource(String path) throws IOException {
    if(!URLUtil.isNetworkUrl(mPath)){
        mp.setDataSource(mPath);
    }
    else{
        URL url = new URL(mPath);
        URLConnection cn = url.openConnection();
        cn.connect();
        InputStream stream = cn.getInputStream();
        if(stream == null){
            throw new RuntimeException("stream is null");
        }
        File fileTemp = File.createTempFile("mediaplayerTmp", "dat");
        String tempPath = fileTemp.getAbsolutePath();
        FileOutputStream out = new FileOutputStream(fileTemp);
        byte buf[] = new byte[128];
        do{
            int numRead = stream.read(buf);
            if(numRead <= 0){
                break;
            }
            out.write(buf, 0, numRead);
        }while(true);
        mp.setDataSource(tempPath);
        try{
            stream.close();
        }
        catch(Exception ex){
            String sDummy = ex.toString();
        }
    }
}

private void getPathFromParentDialog()
{
    Intent intent = getIntent();
    mPath = intent.getExtras().getString("Path");
}
}
