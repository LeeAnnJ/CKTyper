


public class ad8 {
       public static void setLocale(Activity activity, String languageCode) {
           Locale locale = new Locale(languageCode);
           Locale.setDefault(locale);
           Resources resources = activity.getResources();
       }
}
