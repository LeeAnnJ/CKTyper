
//ID = 3204328


@Entity
@Table(name = "basic_user")
@NamedQueries({
    @NamedQuery(name = "BasicUser.findAll", query = "SELECT b FROM BasicUser b"),
    @NamedQuery(name = "BasicUser.findByFirstName", query = "SELECT b FROM BasicUser b WHERE b.firstName = :firstName"),
    @NamedQuery(name = "BasicUser.findByLastName", query = "SELECT b FROM BasicUser b WHERE b.lastName = :lastName"),
    @NamedQuery(name = "BasicUser.findByEmail", query = "SELECT b FROM BasicUser b WHERE b.email = :email"),
    @NamedQuery(name = "BasicUser.findByPassword", query = "SELECT b FROM BasicUser b WHERE b.password = :password")})
public class hibernate_class_30 implements Serializable {
    private static final long serialVersionUID = 1L;
    @Basic(optional = false)
    @Column(name = "First_Name")
    private String firstName;
    @Basic(optional = false)
    @Column(name = "Last_Name")
    private String lastName;
    @Id
    @Basic(optional = false)
    @Column(name = "Email")
    private String email;
    @Basic(optional = false)
    @Column(name = "Password")
    private String password;

    public hibernate_class_30() {
    }
}