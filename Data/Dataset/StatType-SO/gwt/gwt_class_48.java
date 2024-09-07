
//ID = 3635828
public class gwt_class_48  implements EntryPoint{
    @Override
    public void onModuleLoad(){
        TabBar bar=new TabBar();
        bar.addTab("foo");
        bar.addTab("bar");
        bar.addTab("baz");
         bar.addSelectionHandler(new SelectionHandler(){

             public void onSelection(SelectionEvent event){
                 //let user know what you just did
                 Window.alert("you clicked tab"+event.getSelectedItem());
             }

         });
        // Just for fun, let's disallow selection of 'bar'.
         bar.addBeforeSelectionHandler(new BeforeSelectionHandler() {
          public void onBeforeSelection(BeforeSelectionEvent event) {
          event.cancel();
            }


         });

    }
}