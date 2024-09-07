
//ID = 3353405


public class gwt_class_45  implements EntryPoint{

    @Override
    public void onModuleLoad(){
        Label label=new Label("hello world");
        Button button=new Button("say something");
        button.addClickHandler(new ClickHandler(){
     @Override
     public void onClick (ClickEvent event){
         Window.alert("hello again");

            }



        });

    RootPanel.get().add(label);
    RootPanel.get().add(button);



    }
}