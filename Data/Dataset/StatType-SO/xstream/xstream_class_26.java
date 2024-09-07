
//ID=17871210


public class xstream_class_26 {
	public class IntegerListConverter implements SingleValueConverter {
	    @Override
	    public boolean canConvert(Class clazz) {
	        return List.class.isAssignableFrom(clazz);
	    }

	    @Override
	    public Object fromString(String arg0) {
	        Collection<Integer> collection = new ArrayList<Integer>();
	        String[] integerStrings = arg0.split(" ");
	        for (int i = 0; i < integerStrings.length; i++) {
	            collection.add(Integer.valueOf(integerStrings[i]));
	        }
	        return collection;
	    }

	    @Override
	    public String toString(Object arg0) {
	        List collection = (List) arg0;
	        StringBuffer sb = new StringBuffer();
	        boolean first = true;
	        for (Object object : collection) {
	            if (first) {
	                first = false;
	            } else {
	                sb.append(' ');
	            }
	            sb.append(object.toString());
	        }
	        return sb.toString();
	    }
	}
}
