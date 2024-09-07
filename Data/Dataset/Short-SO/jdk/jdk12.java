
public class jdk12 {
    public static boolean h1() {
        String os = System.getProperty("os.name").toLowerCase();
        return os.indexOf("windows") != -1 || os.indexOf("nt") != -1;
    }
}
