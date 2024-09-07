

public class gwt_class_2 implements EntryPoint {

   public void onModuleLoad() {
      // Create a FormPanel and point it at a service.
      final FormPanel form = new FormPanel();
      form.setAction("/myFormHandler");

      // Because we're going to add a FileUpload widget, 
      // we'll need to set the form to use the POST method, 
      // and multipart MIME encoding.
      form.setEncoding(FormPanel.ENCODING_MULTIPART);
      form.setMethod(FormPanel.METHOD_POST);

      // Create a panel to hold all of the form widgets.
      VerticalPanel panel = new VerticalPanel();
      panel.setSpacing(10);
      form.setWidget(panel);

      // Create a TextBox, giving it a name so that it will be submitted.
      final TextBox tb = new TextBox();
      tb.setWidth("220");

      tb.setName("textBoxFormElement");
      panel.add(tb);

      // Create a ListBox, giving it a name and 
      // some values to be associated with its options.
      ListBox lb = new ListBox();
      lb.setName("listBoxFormElement");
      lb.addItem("item1", "item1");
      lb.addItem("item2", "item2");
      lb.addItem("item3", "item3");
      lb.setWidth("220");
      panel.add(lb);

      // Create a FileUpload widget.
      FileUpload upload = new FileUpload();
      upload.setName("uploadFormElement");
      panel.add(upload);

      // Add a 'submit' button.
      panel.add(new Button("Submit", new ClickHandler() {
         @Override
         public void onClick(ClickEvent event) {
            form.submit();					
         }
      }));

      // Add an event handler to the form.
      form.addSubmitHandler(new FormPanel.SubmitHandler() {
         @Override
         public void onSubmit(SubmitEvent event) {
            // This event is fired just before the form is submitted. 
            // We can take this opportunity to perform validation.
            if (tb.getText().length() == 0) {
               Window.alert("The text box must not be empty");
               event.cancel();
            }					
         }
      });

      form.addSubmitCompleteHandler(new FormPanel.SubmitCompleteHandler() {
         @Override
         public void onSubmitComplete(SubmitCompleteEvent event) {
            // When the form submission is successfully completed,
            // this event is fired. Assuming the service returned 
            // a response of type text/html, we can get the result
            // here.
            Window.alert(event.getResults());					
         }
      });

      DecoratorPanel decoratorPanel = new DecoratorPanel();
      decoratorPanel.add(form);
      // Add the widgets to the root panel.
      RootPanel.get().add(decoratorPanel);
}

}