




@Entity
public class hibernate_class_49 implements Serializable {
    /**
     * 
     */
    private static final long serialVersionUID = 1L;
    private String username;
    private String password;
    private Integer VERSION;

    @Version
    public Integer getVERSION() {
        return VERSION;
    }

    public void setVERSION(Integer vERSION) {
        VERSION = vERSION;
    }
    @NaturalId
    public String getUsername() {
        return username;
    }


    public void setUsername(String username) {
        this.username = username;
    }

    public String getPassword() {
        return password;
    }

    public void setPassword(String password) {
        this.password = password;
    }

}
