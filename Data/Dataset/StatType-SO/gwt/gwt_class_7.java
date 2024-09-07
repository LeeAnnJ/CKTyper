
//ID = 1539885



public class gwt_class_7 {
	public class GWTMemoryIssue implements EntryPoint {
		//Run with or without table
		private static final boolean WITH_TABLE = false; 

//		private final TestServiceAsync rpcService = GWT.create(TestService.class);

		private Panel panel;
		private Timer timer;
		private Table table;

		public void onModuleLoad() {
		    RootPanel rootPanel = RootPanel.get();

		    this.panel = new VerticalPanel();
		    this.panel.setSize("100%", "100%");

		    rootPanel.add(panel);

		    if (WITH_TABLE) {
		        loadTable();
		    }else{
		        startUpdateTask();
		    }

		}

		private void startUpdateTask() {
		    this.timer = new Timer() {

		        public void run() {
//		            GWTMemoryIssue.this.getTableData();

		        }
		    };
		    this.timer.scheduleRepeating(2000);
		}

		public void loadTable() {
		    Runnable onLoadCallback = new Runnable() {
		        public void run() {
//		            GWTMemoryIssue.this.table = new Table(createTableData(), createTableOptions());
		            GWTMemoryIssue.this.table.setSize("100%", "100%");
		            GWTMemoryIssue.this.panel.add(GWTMemoryIssue.this.table);
		            GWTMemoryIssue.this.startUpdateTask();
		        }
		    };

//		    VisualizationUtils.loadVisualizationApi(onLoadCallback, Table.PACKAGE);
		}

//		private Options createTableOptions() {
//		    Options options = Options.create();
//
//		    return options;
//		}

//		private DataTable createTableData() {
//		    DataTable data = DataTable.create();
//
//		    data.addColumn(ColumnType.STRING, "Name");
//		    data.addColumn(ColumnType.NUMBER, "Intval 1");
//		    data.addColumn(ColumnType.NUMBER, "Intval 2");
//		    data.addColumn(ColumnType.NUMBER, "Intval 3");
//
//		    return data;
//		}

//		private void getTableData() {
////		    rpcService.getListOfItems(new AsyncCallback<ArrayList<ListItem>>(){
//		        public void onFailure(Throwable caught) {
//		            // Do nothing
//		        }
//
//		        public void onSuccess(ArrayList<ListItem> result) {
//		            if (WITH_TABLE){
////		                GWTMemoryIssue.this.updateTableData(result);
//		            }else{
//		                //Ignore the data from the server
//		            }
//		        }
//		    });
		}

//		private void updateTableData(ArrayList<ListItem> result) {
//		    DataTable data = createTableData();
//
//		    data.addRows(result.size());
//
//		    int row = 0;
//		    for (ListItem li : result) {
//		        data.setValue(row, 0, li.getName());
//		        data.setValue(row, 1, li.getIntVal());
//		        data.setValue(row, 2, li.getIntSecondVal());
//		        data.setValue(row, 3, li.getThirdIntVal());
//		        row++;
//		    }
//
//		    this.table.draw(data, createTableOptions());
//		}
		}
