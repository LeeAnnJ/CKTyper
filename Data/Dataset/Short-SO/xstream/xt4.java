


public class xt4 {
    public static void h1(){
        XStream xstream = new XStream(new JettisonMappedXmlDriver());
        xstream.alias("entity", Entity[].class);
    }
}
