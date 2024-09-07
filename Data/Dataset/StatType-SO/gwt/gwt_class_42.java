
//ID = 2987127

public class gwt_class_42 {
	public class Tesdb3 implements EntryPoint { 

		String url= "http://localhost/phpmyadmin/tesdb3/datauser.php";

		public void LoadData() throws RequestException{             

		    RequestBuilder builder = new RequestBuilder(RequestBuilder.GET, URL.encode(url));

		    builder.sendRequest(null, new RequestCallback(){
		        @Override
		        public void onError(Request request, Throwable exception) {
		            Window.alert("error " + exception);
		        }
		        public void onResponseReceived(Request request,
		                Response response) {
		              if (200 == response.getStatusCode()) {
		                  Window.alert("ok -" + response.getText() + "-" + response.getStatusCode());
		              } else {
		                  Window.alert("error2 -" + response.getText()+ response.getStatusText() + "-" + response.getStatusCode());
		              }         
		        }
		    });
		}

		public void onModuleLoad() {        
		    try {
		        LoadData();
		    } catch (RequestException e) {
		        e.printStackTrace();
		    }       
		}
		}
}
