
public class jdk5 {
    public static void f1() throws MalformedURLException {
        File jar = new File("");
        URLClassLoader loader = new
                URLClassLoader(new URL[]{jar.toURI().toURL()});
    }
}

