
//ID = 3143234


public class xstream_class_5{
	public class Test {
	    public void main(String[] args) throws FileNotFoundException {
	        XStream xs = new XStream(new DomDriver());
	        Foo f = new Foo(1, "booo", new Bar(42));
	        PrintWriter pw = new PrintWriter("a.xml");
	        xs.toXML(f,pw);
	    }
	}


	public class Bar {
	    public int id;

	    public Bar(int id) {
	        this.id = id;
	    }

	}


	public class Foo {
	    public int a;
	    public String b;
	    public Bar boo;
	    public Foo(int a, String b, Bar c) {
	        this.a = a;
	        this.b = b;
	        this.boo = c;
	    }
	}

}
