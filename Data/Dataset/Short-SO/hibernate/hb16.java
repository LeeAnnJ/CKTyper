

public class hb16<Car_OneToMany> {
    @OneToMany(cascade = {CascadeType.ALL})
    @Column(name = "ListOfCarsDrivenByDriver")
    private List<Car_OneToMany> listOfCarsBeingDriven = new ArrayList<Car_OneToMany>();
}
