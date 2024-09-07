
//ID = 3754253



public class hibernate_class_42 {

    private static final Log log = LogFactory.getLog(hibernate_class_42.class);

    private final SessionFactory sessionFactory = getSessionFactory();

    protected SessionFactory getSessionFactory() {
        try {
            return (SessionFactory) new InitialContext()
                    .lookup("java:/hibernate/SessionFactory");
        } catch (Exception e) {
            log.error("Could not locate SessionFactory in JNDI", e);
            throw new IllegalStateException(
                    "Could not locate SessionFactory in JNDI");
        }
    }

    public void persist() {
        log.debug("persisting Empleados instance");
        try {
            sessionFactory.getCurrentSession().persist("aa");
            log.debug("persist successful");
        } catch (RuntimeException re) {
            log.error("persist failed", re);
            throw re;
        }
    }

    public void attachDirty() {
        log.debug("attaching dirty Empleados instance");
        try {
            sessionFactory.getCurrentSession().saveOrUpdate("aa");
            log.debug("attach successful");
        } catch (RuntimeException re) {
            log.error("attach failed", re);
            throw re;
        }
    }

    public void attachClean() {
        log.debug("attaching clean Empleados instance");
        try {
            sessionFactory.getCurrentSession().lock("aa", sessionFactory, null);
            log.debug("attach successful");
        } catch (RuntimeException re) {
            log.error("attach failed", re);
            throw re;
        }
    }

    public void delete() {
        log.debug("deleting Empleados instance");
        try {
            sessionFactory.getCurrentSession().delete("aa");
            log.debug("delete successful");
        } catch (RuntimeException re) {
            log.error("delete failed", re);
            throw re;
        }
    }

//    public Empleados merge(Empleados detachedInstance) {
//        log.debug("merging Empleados instance");
//        try {
//            Empleados result = (Empleados) sessionFactory.getCurrentSession()
//                    .merge(detachedInstance);
//            log.debug("merge successful");
//            return result;
//        } catch (RuntimeException re) {
//            log.error("merge failed", re);
//            throw re;
//        }
//    }
//
//    public Empleados findById(java.lang.Integer id) {
//        log.debug("getting Empleados instance with id: " + id);
//        try {
//            Empleados instance = (Empleados) sessionFactory.getCurrentSession()
//                    .get("com.hibernate.Empleados", id);
//            if (instance == null) {
//                log.debug("get successful, no instance found");
//            } else {
//                log.debug("get successful, instance found");
//            }
//            return instance;
//        } catch (RuntimeException re) {
//            log.error("get failed", re);
//            throw re;
//        }
//    }

    public List findByExample() {
        log.debug("finding Empleados instance by example");
        try {
            Object instance = null;
			List results = sessionFactory.getCurrentSession().createCriteria(
                    "com.hibernate.Empleados").add(Example.create(instance))
                    .list();
            log.debug("find by example successful, result size: "
                    + results.size());
            return results;
        } catch (RuntimeException re) {
            log.error("find by example failed", re);
            throw re;
        }
    }
}