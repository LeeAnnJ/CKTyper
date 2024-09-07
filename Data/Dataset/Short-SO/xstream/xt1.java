

public class xt1 {
    public static void h1(){
        XmlFriendlyNameCoder nameCoder = new XmlFriendlyNameCoder("ddd", "_");
        XStream xmlStream = new XStream(new Dom4JDriver(nameCoder));
    }
}
