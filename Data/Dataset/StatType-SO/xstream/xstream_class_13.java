
//ID=1372467

public class xstream_class_13 {
	public class MyClassAliasingMapper extends ClassAliasingMapper {

	    public MyClassAliasingMapper(Mapper wrapped) {
	        super(wrapped);
	    }

	    @Override
	    public Class realClass(String elementName) {
	        try {
	        } catch (Exception e) {
	            // do nothing we fall back on super's implementation
	        }
	        return super.realClass(elementName);
	    }

	    @Override
	    public String serializedClass(Class type) {
	        try {
	        } catch (Exception e) {
	            // do nothing we fall back on super's implementation
	        }
	        return super.serializedClass(type);
	    }
	}
}
