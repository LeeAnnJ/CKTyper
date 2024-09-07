
//ID = 988217


public class gwt_class_3 implements EntryPoint {

 private static final String SERVER_ERROR = "An error occurred while attempting to contact the server. Please check your network connection and try again.";

// private final RPCCallsServiceAsync rpccallService = GWT.create(RPCCallsService.class);

 TextBox nameTxt = new TextBox();
 Button btnSave = getBtnSave();

 public void onModuleLoad() {

  RootPanel.get("inputName").add(nameTxt); 
  RootPanel.get("btnSave").add(btnSave);
 }



 private Button getBtnSave(){

  Button btnSave = new Button("SAVE");

  return btnSave;
 }

 void saveData2DB(String name){  
  AsyncCallback<String> callback = new AsyncCallback<String>() {
   public void onFailure(Throwable caught) {
          Window.alert("WOOOHOOO, ERROR: " + SERVER_ERROR);
    // TODO: Do something with errors.
        }

        public void onSuccess(String result) {
          Window.alert("Server is saying: ' " + result + "'");
        }

  };

//  ArrayList<Address> aa = new ArrayList<Address>();
//  aa.add(new Address("123 sasdf","", "Some City", "AZ", "93923-2321"));
//  aa.add(new Address("23432 asdf", "Appt 34", "Another City", "AZ", "43434-4432"));
//
//  Person p = new Person();
//  p.setName(name);
//  p.setAge(23);
//  p.setGender('m');
//  p.setAddresses(aa);
//
//  // !!!!!!!!!!!!!!!!!!  SERVER CALL !!!!!!!!!!!!!!!!!!
//  rpccallService.saveName(p, callback);
//  // !!!!!!!!!!!!!!!!!!  SERVER CALL !!!!!!!!!!!!!!!!!!

 }
}
