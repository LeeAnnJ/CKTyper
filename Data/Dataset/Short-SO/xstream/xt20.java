

public class xt20 {
    public static void h1(){
        XStream xstream = new XStream();
        ClassAliasingMapper mapper = new ClassAliasingMapper(xstream.getMapper());
        xstream.registerLocalConverter(Test.class, "tags", new CollectionConverter(mapper));
    }
}
