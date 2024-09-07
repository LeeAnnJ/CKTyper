
//ID = 1629323


public class gwt_class_10 {
	public void main(){
		final FormPanel form =new FormPanel();
	    VerticalPanel holder = new VerticalPanel();
	    holder.add(new Label("User ID"));
	    TextBox nameTextBox = new TextBox();
	    nameTextBox.setName("userid");
	    holder.add(nameTextBox);

	     Button submitButton = new Button("Submit");
	     holder.add(submitButton);
	    form.add(holder);

	    submitButton.addClickListener(new ClickListener() {

	    public void onClick1(Widget sender) {
	            form.submit();
	    }

		@Override
		public void onClick(Widget sender) {
			// TODO Auto-generated method stub
			
		}
	});
	}
}
