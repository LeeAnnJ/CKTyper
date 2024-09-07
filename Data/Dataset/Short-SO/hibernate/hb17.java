

public class hb17 {
    public static void h1(){
        Appender clazz = null;
        String typename = clazz.getName();
        Type type = (Type) TypeFactory.heuristicType(typename);
        boolean serializable = type!=null && type instanceof SerializableType;
    }

}
