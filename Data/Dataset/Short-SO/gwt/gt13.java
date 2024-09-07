


public class gt13 {
    public final void h1(final ValueChangeEvent<String> event) {
        String token = event.getValue();
        if (token != null) {
            String[] tokens = History.getToken().split(":");
            final String token2 = tokens.length > 1 ? tokens[1] : "";
        }
    }
}
