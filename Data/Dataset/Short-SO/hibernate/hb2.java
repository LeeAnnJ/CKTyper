


public class hb2 {

        @Entity
        public static class University<Student> {
            private String address;
            @OneToMany(fetch = FetchType.LAZY)
            private List<Student> students;

        }
}
