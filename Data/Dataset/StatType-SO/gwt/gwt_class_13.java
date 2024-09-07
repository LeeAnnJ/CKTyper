
//ID = 1692017

@SuppressWarnings("deprecation")
public class gwt_class_13 {
	public class ERD1 implements EntryPoint {

		public void onModuleLoad() {

		 AbsolutePanel boundaryPanel = new AbsolutePanel();
		    boundaryPanel.setPixelSize(1000, 1000);

//		    final Diagram d = new Diagram(boundaryPanel);

		 Button b = new Button();
		 b.addClickListener(new ClickListener(){

		  public void onClick1(Widget sender) {
		  }

		@Override
		public void onClick(Widget sender) {
			// TODO Auto-generated method stub
			
		}

		 });

		 boundaryPanel.add(b, 10, 40);

		 RootPanel.get().add(boundaryPanel);
		} 
		}
}
