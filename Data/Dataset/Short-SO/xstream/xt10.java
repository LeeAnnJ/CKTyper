
public class xt10 {
    public static void h1(){
        XStream stream = new XStream(new StaxDriver());
        stream.toXML(messages, out);
        StringWriter out = new StringWriter();
    }
}
