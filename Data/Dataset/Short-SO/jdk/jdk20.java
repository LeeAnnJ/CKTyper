

public class jdk20 {
    private static InputStream inputStream;

    public static void h1() throws IOException {
        BufferedInputStream bis = new BufferedInputStream(inputStream);
        ByteArrayOutputStream buf = new ByteArrayOutputStream();
    }
}
