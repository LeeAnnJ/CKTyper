
//ID = 2155194
public class gwt_class_19{
	private void addStartupBox() {
	    VerticalPanel boxPanel = null;      
	    com.google.gwt.user.client.ui.Label title = null;        

	    // Create second panel for the content of a box     
	    com.google.gwt.user.client.ui.VerticalPanel boxContent = new com.google.gwt.user.client.ui.VerticalPanel();
	    boxContent.setSpacing(10);
	    boxContent.setHorizontalAlignment(com.google.gwt.user.client.ui.VerticalPanel.ALIGN_CENTER);

	    // Create content for the box
	    Button but1 = new Button("A");
	    but1.setPixelSize(280, 25);     

	    Button but2 = new Button("B");
	    but2.setPixelSize(280, 25);

	    Button but3 = new Button("C");
	    but3.setPixelSize(280, 25);

	    // Add buttons to boxContent
	    boxContent.add(but1);
	    boxContent.add(but2);
	    boxContent.add(but3);

	    // Add title and boxContent to boxPanel     
	    boxPanel.add(title);
	    boxPanel.add(boxContent);

	    RootPanel.get("boxPanelContainer").add(boxPanel);
	}	
}
