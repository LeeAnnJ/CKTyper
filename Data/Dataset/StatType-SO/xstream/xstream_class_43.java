
//https://developmentality.wordpress.com/2010/07/13/xstream-introduction-and-java-collections-serialization-problem-workaround/


public class xstream_class_43 {
    public List<Book> books;
 
    public xstream_class_43(List<Book> books) {
        this.books = books;
    }
 
    @Override
    public String toString() {
        StringBuilder b = new StringBuilder();
        b.append("Library with " + books.size() + " books:\n");
        for (Book book : books) {
            b.append(book.toString());
            // Skip a line
            b.append("\n");
        }
        return b.toString();
    }
 
    public static class Book {
        private String title;
        private String author;
 
        public Book(String title, String author) {
            this.title = title;
            this.author = author;
        }
 
        @Override
        public String toString() {
            return "\"" + title + "\" by " + author;
        }
    }
 
    public static void main(String[] args) {
        List<Book> books = new ArrayList<Book>();
        books.add(new Book("The Talent Code: Greatness Isn't Born. It's Grown. Here's How", "Daniel Coyle"));
 
        xstream_class_43 lib = new xstream_class_43(books);
        // Handles conversion of our objects into XML
        XStream stream = new XStream(new DomDriver());
 
        String xml = stream.toXML(lib);
        // fromXML returns a general Object; need to cast it into a Library
        xstream_class_43 lib2 = (xstream_class_43) stream.fromXML(xml);
 
        System.out.println(xml);
        System.out.println(lib);
        System.out.println(lib2);
        System.out.println("Libraries equal: " + lib.toString().equals(lib2.toString()));
    }
}