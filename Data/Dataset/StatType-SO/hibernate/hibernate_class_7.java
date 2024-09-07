
//ID = 1205820

public class hibernate_class_7 {
	public class HibernateUtils {
		private final SessionFactory sessionFactory;
		private Session session;

		public HibernateUtils() {
		    this.sessionFactory = new AnnotationConfiguration().configure().buildSessionFactory();
		}

		public HibernateUtils(SessionFactory sessionFactory) {
		    this.sessionFactory = sessionFactory;
		}

		/**
		 *
		 * this is the function that return a session.So i'm free to implements any type of session in here.
		 */
		public Session requestSession() {
//		        if (session != null || session.isOpen()) {
//		            return session;
//		        } else {
		        session = sessionFactory.openSession();

//		        }
		    return session;
		  }
		}
}
