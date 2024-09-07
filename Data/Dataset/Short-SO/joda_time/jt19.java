

public class jt19 {
   public static void h1(){
      String input = "04/02/2011 20:27:05" ;
      DateTimeFormatter f = DateTimeFormatter.ofPattern( "dd/MM/uuuu HH:mm:ss" ) ;
      LocalDateTime ldt = LocalDateTime.parse( input , f ) ;
   }
}
