
//ID = 2724147

public class hibernate_class_23 {
	private static final ThreadLocal<Session> threadLocal = new ThreadLocal<Session>();
	private  static Configuration configuration = new AnnotationConfiguration();    
	private static org.hibernate.SessionFactory sessionFactory;
	static {
		try {
			String configFile="";
			configuration.configure(configFile);
			sessionFactory = configuration.buildSessionFactory();
		} catch (Exception e) {}
	}
	private hibernate_class_23() {}
	public static Session getSession() throws HibernateException {
		Session session = (Session) threadLocal.get();
		if (session == null || !session.isOpen()) {
			if (sessionFactory == null) {
				//    rebuildSessionFactory();//This method basically does what the static init block does
			}
			session = (sessionFactory != null) ? sessionFactory.openSession(): null;
			threadLocal.set(session);
		}
		return session;
	}
}