
//http://www.programcreek.com/java-api-examples/index.php?source_dir=cloudbees-api-client-master/cloudbees-api-client/src/main/java/com/cloudbees/api/config/ConfigParameters.java


public class xstream_class_34 {
	@XStreamAlias("config") 
	public class ConfigParameters extends ParameterHolder { 
	    @XStreamImplicit(itemFieldName = "resource") 
	    private List<ResourceSettings> resources; 
	 
	    @XStreamImplicit(itemFieldName = "env") 
	    private List<Environment> environments; 
	 
	    public ConfigParameters() { 
	    } 
	 
	    public List<Environment> getEnvironments() { 
	        if (environments == null) 
	            environments = new ArrayList<Environment>(); 
	        return environments; 
	    } 
	 
	    public void setEnvironments(List<Environment> environments) { 
	        this.environments = environments; 
	    } 
	 
	    public void setEnvironment(Environment environment) { 
	        deleteEnvironment(environment.getName()); 
	        getEnvironments().add(environment); 
	    } 
	 
	    public Environment getEnvironment(String env) { 
	        for (Environment environment: getEnvironments()) { 
	            if (env.equals(environment.getName())) 
	                return environment; 
	        } 
	        return null; 
	    } 
	    public void deleteEnvironment(String name) { 
	        Iterator<Environment> it = getEnvironments().iterator(); 
	        while (it.hasNext()) { 
	            if (it.next().getName().equals(name)) { 
	                it.remove(); 
	            } 
	        } 
	    } 
	 
	 
	    public List<ResourceSettings> getResources() { 
	        if (resources == null) 
	            resources = new ArrayList<ResourceSettings>(); 
	        return resources; 
	    } 
	 
	    public void setResources(List<ResourceSettings> resources) { 
	        this.resources = resources; 
	    } 
	 
	    public void setResource(ResourceSettings resource) { 
	        deleteResource(resource.getName()); 
	        getResources().add(resource); 
	    } 
	 
	    public ResourceSettings getResource(String name) { 
	        for (ResourceSettings resource : getResources()) { 
	            if (resource.getName().equals(name)) 
	                return resource; 
	        } 
	        return null; 
	    } 
	    public void deleteResource(String name) { 
	        Iterator<ResourceSettings> it = getResources().iterator(); 
	        while (it.hasNext()) { 
	            if (it.next().getName().equals(name)) { 
	                it.remove(); 
	            } 
	        } 
	    } 
	 
	    private XStream createXStream() { 
	        XStream xstream = new XStream() { 
	            protected MapperWrapper wrapMapper(MapperWrapper next) { 
	                return new MapperWrapper(next) { 
	                    public boolean shouldSerializeMember(Class definedIn, String fieldName) { 
	                        return definedIn != Object.class && super.shouldSerializeMember(definedIn, fieldName); 
	                    } 
	 
	                }; 
	            } 
	        }; 
	 
	        xstream.setClassLoader(ConfigParameters.class.getClassLoader()); 
	        xstream.processAnnotations(ResourceSettings.class); 
	        xstream.processAnnotations(Environment.class); 
	        xstream.processAnnotations(ConfigParameters.class); 
	        xstream.processAnnotations(ParameterHolder.class); 
	        return xstream; 
	    } 
	 
	    /**
	     * Returns a string representation of XML. 
	     */ 
	    public String toXML() { 
	        return createXStream().toXML(this); 
	    } 
	 
	    public ConfigParameters parse(String xml) { 
	        if (xml == null) 
	            return new ConfigParameters(); 
	        return (ConfigParameters) createXStream().fromXML(xml); 
	    } 
	}
}
