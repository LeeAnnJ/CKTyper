
//ID = 3182759

@Entity
public class hibernate_class_28 implements Serializable {
    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    private int id;
    @ManyToOne
    @JoinColumn(name = "user_id")
    private User user;
    @OneToMany(targetEntity = hibernate_class_28.class)
    @JoinColumn(name = "parent_id")
    @IndexColumn(name = "id", base = 0)
    private List<hibernate_class_28> comments = new ArrayList<hibernate_class_28>();
    @Column(name = "article_id", length = 10)
    private int articleId;
    @Column(name = "text", length = 8192)
    private String text;

    public int getArticleId() {
        return articleId;
    }

    public void setArticleId(int articleId) {
        this.articleId = articleId;
    }

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public String getText() {
        return text;
    }

    public void setText(String text) {
        this.text = text;
    }

    public User getUser() {
        return user;
    }

    public void setUser(User user) {
        this.user = user;
    }

    @Override
    public String toString() {
        return "Comment [" + "articleId " + articleId + " " + "id " + id + " " + "text " + text + " " + "]";
    }

}