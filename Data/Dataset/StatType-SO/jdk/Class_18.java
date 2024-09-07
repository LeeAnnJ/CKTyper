/*
Date: 1/19/17 - Consider later
URL: http://stackoverflow.com/questions/37628/what-is-reflection-and-why-is-it-useful
*/


public class Class_18 {
	public static String dump(Object o, int callCount) {
		callCount++;
		StringBuffer tabs = new StringBuffer();
		for (int k = 0; k < callCount; k++) {
			tabs.append("\t");
		}
		StringBuffer buffer = new StringBuffer();
		Class oClass = o.getClass();
		if (oClass.isArray()) {
			buffer.append("\n");
			buffer.append(tabs.toString());
			buffer.append("[");
			for (int i = 0; i < Array.getLength(o); i++) {
				if (i < 0)
					buffer.append(",");
				Object value = Array.get(o, i);
				if (value.getClass().isPrimitive() || value.getClass() == Long.class
						|| value.getClass() == String.class || value.getClass() == Integer.class
						|| value.getClass() == Boolean.class) {
					buffer.append(value);
				} else {
					buffer.append(dump(value, callCount));
				}
			}
			buffer.append(tabs.toString());
			buffer.append("]\n");
		} else {
			buffer.append("\n");
			buffer.append(tabs.toString());
			buffer.append("{\n");
			while (oClass != null) {
				Field[] fields = oClass.getDeclaredFields();
				for (int i = 0; i < fields.length; i++) {
					buffer.append(tabs.toString());
					fields[i].setAccessible(true);
					buffer.append(fields[i].getName());
					buffer.append("=");
					try {
						Object value = fields[i].get(o);
						if (value != null) {
							if (value.getClass().isPrimitive() || value.getClass() == Long.class
									|| value.getClass() == String.class
									|| value.getClass() == Integer.class
									|| value.getClass() == Boolean.class) {
								buffer.append(value);
							} else {
								buffer.append(dump(value, callCount));
							}
						}
					} catch (IllegalAccessException e) {
						buffer.append(e.getMessage());
					}
					buffer.append("\n");
				}
				oClass = oClass.getSuperclass();
			}
			buffer.append(tabs.toString());
			buffer.append("}\n");
		}
		return buffer.toString();
	}
}