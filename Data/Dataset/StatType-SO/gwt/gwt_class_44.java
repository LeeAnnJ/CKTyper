
//ID = 3313553

public class gwt_class_44 extends ResizeComposite {

    private static gwt_class_44 instance = null;

    public static void getInstance(final AsyncCallback<gwt_class_44> callback) {
        GWT.runAsync(new RunAsyncCallback() {

            @Override
            public void onSuccess() {
                if (instance == null) {
                    instance = new gwt_class_44();
                }
                callback.onSuccess(instance);
            }

            @Override
            public void onFailure(Throwable reason) {
                callback.onFailure(reason);
            }
        });
    }

    private gwt_class_44() {
        DockLayoutPanel dockLayoutPanel = new DockLayoutPanel(Unit.EM);
        dockLayoutPanel.addNorth(new Label("North!"), 7);
        dockLayoutPanel.addWest(new Label("West!"), 15);
        dockLayoutPanel.add(new Label("Center! :D"));
        initWidget(dockLayoutPanel);
    }

}
