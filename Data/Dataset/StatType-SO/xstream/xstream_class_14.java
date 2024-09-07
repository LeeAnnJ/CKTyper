
//ID = 3533894

public class xstream_class_14 {
	public class SingleValueEnumConverter extends AbstractSingleValueConverter
	{
	    @SuppressWarnings("rawtypes")
		private final Class enumType;

	    public SingleValueEnumConverter(Class type)
	    {
	        this.enumType = type;
	    }

	    public boolean canConvert(Class c)
	    {
	        return c.equals(enumType);
	    }

	    public Object fromString(String value)
	    {
	        return Enum.valueOf(enumType, value);
	    }
	}
}
