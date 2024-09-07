//ID = 26862650


public class xstream_class_39 {

	private static XStream xstream = new XStream(){
	        public HierarchicalStreamWriter createWriter(Writer out) {  
	            return new PrettyPrintWriter(out) {  
	                // Add CDATA block  
	                boolean cdata;//I need to add cdata for some fields only  
	                boolean isNeedUpper;//only some will need this

	                protected void writeText(QuickWriter writer, String text) {  
	                    if (cdata) {  
	                        writer.write("<![CDATA[");  
	                        writer.write(text);  
	                        writer.write("]]>");  
	                    } else if (isNeedUpper){  
	                        writer.write(text.toUpperCase());  
	                    }  
	                    else writer.write(text);
	                }  
	            };  
	        }  
	    };
}