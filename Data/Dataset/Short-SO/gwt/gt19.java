
public class gt19 {
       public static String h1(final String format, final String... args) {
           String[] split = format.split("%s");
           final StringBuffer msg = new StringBuffer();
           msg.append(split[split.length - 1]);
           return msg.toString();
       }

}
