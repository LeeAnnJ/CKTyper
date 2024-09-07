
//ID = 1791178

public class xstream_class_12 {
	public class ListToStringXStreamConverter implements Converter {

		private String alias;

		public ListToStringXStreamConverter(String alias) {
		    super();
		    this.alias = alias;
		}

		@SuppressWarnings("rawtypes")
		@Override
		public boolean canConvert(Class type) {
		    return true;
		}

		@Override
		public void marshal(Object source, HierarchicalStreamWriter writer, MarshallingContext context) {

		    @SuppressWarnings("unchecked")
		    List<String> list = (List<String>)source;

		    for (String string : list) {
		        writer.startNode(alias);
		        writer.setValue(string);
		        writer.endNode();
		    }

		}

		@Override
		public Object unmarshal(HierarchicalStreamReader reader, UnmarshallingContext context) {
		    throw new UnsupportedOperationException("ListToStringXStreamConverter does not offer suport for unmarshal operation");
		}

		}

}
