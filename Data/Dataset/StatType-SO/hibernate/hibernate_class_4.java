
//ID = 970573

public class hibernate_class_4 {
    private static final SessionFactory sessionFactory;

    static {
        try {
            sessionFactory = new Configuration ().configure ().buildSessionFactory ();
        } catch (HibernateException he) {
            System.err.println (he);
            throw new ExceptionInInitializerError (he);
        }
    }

    public static SessionFactory getSessionFactory () {
        return sessionFactory;
    }
}