

public class jdk6 {
    private static boolean h1() {
        boolean hasPermission = true;
        SecurityManager sm = System.getSecurityManager();
        if (sm != null) {
            sm.checkPermission(new PropertyPermission("user.timezone", "write"));
        }
        return hasPermission;
    }
}

