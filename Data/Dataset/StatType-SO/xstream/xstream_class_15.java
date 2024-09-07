
//ID=328832


public class xstream_class_15 {
	public static void main(String arg[]){
		XStream xs = new XStream();
		xs.registerConverter(new CollectionConverter(xs.getMapper()) {
		    @Override
		    public void marshal(Object source, HierarchicalStreamWriter writer, MarshallingContext context) {
		        org.hibernate.collection.PersistentSet ps = null;
		        super.marshal(new HashSet(ps), writer, context);
		    }

		    @Override
		    public boolean canConvert(Class type) {
		        return type.isAssignableFrom(org.hibernate.collection.PersistentSet.class);
		    }
		}, XStream.PRIORITY_VERY_HIGH);
		Object processInstance = null;
		String s = xs.toXML(processInstance);
	}
}
