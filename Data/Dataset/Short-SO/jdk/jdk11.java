

public class jdk11 {
    private static boolean h1() {
        boolean hasPermission = true;
        SecurityManager sm = System.getSecurityManager();
        if (sm != null) {
                hasPermission = false;
        }
        return hasPermission;
    }

}
