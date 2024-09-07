/*
Date: 1/19/17 - Consider later
URL: http://stackoverflow.com/questions/2885173/how-do-i-create-a-file-and-write-to-a-file-in-java
*/


public class Class_11 {

	public static void main(String[] args) {
		try {
			// Create new file
			String content = "This is the content to write into create file";
			String path = "D:\\a\\hi.txt";
			File file = new File(path);

			// If file doesn't exists, then create it
			if (!file.exists()) {
				file.createNewFile();
			}

			FileWriter fw = new FileWriter(file.getAbsoluteFile());
			BufferedWriter bw = new BufferedWriter(fw);

			// Write in file
			bw.write(content);

			// Close connection
			bw.close();
		} catch (Exception e) {
			System.out.println(e);
		}

		JFileChooser c = new JFileChooser();
		c.showOpenDialog(c);
		File writeFile = c.getSelectedFile();
		String content = "Input the data here to be written to your file";

		try {
			FileWriter fw = new FileWriter(writeFile);
			BufferedWriter bw = new BufferedWriter(fw);
			bw.append(content);
			bw.append("hiiiii");
			bw.close();
			fw.close();
		} catch (Exception exc) {
			System.out.println(exc);
		}
	}
}