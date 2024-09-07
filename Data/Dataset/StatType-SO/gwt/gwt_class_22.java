
//ID = 2237142

public class gwt_class_22 extends Composite {

    private static TestViewUiBinder uiBinder = GWT.create(TestViewUiBinder.class);

    interface TestViewUiBinder extends UiBinder<VerticalPanel, gwt_class_22> {}

    @UiField Label testObjectStringLabel;
    @UiField Label innerObjectStringLabel;
    @UiField VerticalPanel listObjectsPanel;
    @UiField Button button;
    @UiField Label errorMessageLabel;

    public gwt_class_22(String firstName) {
        initWidget(uiBinder.createAndBindUi(this));
    }

    @UiHandler("button")
    void onClick(ClickEvent e) {

    }

}