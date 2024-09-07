
//ID = 1212669



/**
 * Several models are date range sensitive, this base class provides that basic
 * functionality.
 * 
 * @author jim
 * 
 */
@MappedSuperclass
public abstract class hibernate_class_8 {
private static final long serialVersionUID = 1L;
private Date from;
private Date thru;

/**
 * Determines if a model is active. A model is active if now is after or
 * equal to from , and thru is either null, or after now, or equal to now.
 */
@Transient
public boolean isActive() {
 Date now = new Date();
 boolean afterFrom = from.before(now) || from.equals(now);
 boolean beforeThru = thru == null || thru.after(now)
   || thru.equals(now);
 return afterFrom && beforeThru;
}

@AssertTrue(message = "Dates are not valid the thru date must be empty, or after the fromdate.")
public boolean areDatesValid() {
 if (thru == null) {
  return true;
 } else {
  return thru.after(from);
 }
}


@Temporal(TemporalType.TIMESTAMP)
@NotNull
@Column(name = "fromDate")
public Date getFrom() {
 return from;
}

public void setFrom(Date from) {
 this.from = from;
}

@Temporal(TemporalType.TIMESTAMP)
public Date getThru() {
 return thru;
}

public void setThru(Date thru) {
 this.thru = thru;
}
}