
public class jdk13 {
    public static boolean isMac() {
        String os = System.getProperty("os.name");
        return os.contains("mac");
    }

}
