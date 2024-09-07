


public class jdk14 {
    public static void h1(String aFile) throws IOException {
        Desktop desktop = Desktop.getDesktop();
        desktop.open(new File(aFile));
    }

}
