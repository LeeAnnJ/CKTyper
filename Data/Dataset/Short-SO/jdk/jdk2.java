

public class jdk2 {
    public static void main(String args[]){
        String userDirPropertyName = "user.dir";
        File initialUserDir = new File(System.getProperty(userDirPropertyName));
        System.out.println("files in " + initialUserDir.getAbsolutePath() + ":");
    }
    }


