

public class hb13 {
    private Type h1(Class clazz) throws HibernateException {
        String typename = clazz.getName();
        return (Type) Hibernate.entity(clazz);
    }
}
