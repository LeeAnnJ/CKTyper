


public class hb15<GlobalConfigScope> {
    private static Object Type;

    @OneToMany(cascade = CascadeType.ALL, mappedBy="globalConfig", orphanRemoval = true)
    private Set<GlobalConfigScope> gcScopeSet;
}
