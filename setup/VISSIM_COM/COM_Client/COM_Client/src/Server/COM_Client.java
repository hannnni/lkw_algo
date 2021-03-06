package Server;

import java.io.*;
import java.net.*;
import java.io.File;

public class COM_Client {
	
	static int adressePort_Detection = 9999;
	static int adressePort_Status = 9998;

	static String currentDir_Status = new File("daten_Status.txt").getAbsolutePath(); 
	static String currentDir_Detection = new File("daten_Detection.txt").getAbsolutePath(); 

	public static void main(String args[]) {
		/**
		 * Einlesen der Konfigurationsdatei - IP, Port an die gesendet werden soll und Pfad, wo die VISSIM *.inp-Datei zu finden ist
		 */
		System.out.println("Start");
		try{
			BufferedReader in = new BufferedReader(new FileReader("config_Server.txt"));
			String zeile = null;
			while ((zeile = in.readLine()) != null) 
			{
				if (zeile.equals("Port zum Empfangen der Detektordaten")) {adressePort_Detection =Integer.parseInt(in.readLine()); }
				else if (zeile.equals("Port zum Empfangen der Statusdaten der Signalgruppen")) {adressePort_Status =Integer.parseInt(in.readLine()); }
			}
		}
		catch(Exception e) {System.out.print(e.toString());}
		
		new Thread_Detection().start();
		new Thread_Status().start();
	}
	
	/**
	 * Thread f�r das Empfangen der Daten der Detectionen bzw. der min�tliche Empfangen der auf Stundenwerte extrapolierten Verkehrsst�ken
	 * �bertragung zeitschrittorientiert sek�ndlich
	 */
	private static class Thread_Detection extends Thread
	{
		public void run()
		{
			try {                 			   
				ServerSocket server_Detection = new ServerSocket(adressePort_Detection);                 
				Socket clientSocket_Detection = server_Detection.accept();                 
				ObjectInputStream in_Detection = new ObjectInputStream(clientSocket_Detection.getInputStream());
				Object o_Detection = in_Detection.readObject(); 
				                
				server_Detection.close();                 
				clientSocket_Detection.close(); 
	
				schreibeDaten_Detection(o_Detection);
			} 
			catch (IOException e) {} 
			catch (ClassNotFoundException e){}     
			
			new Thread_Detection().start();
		}
	}

	/**
	 * Thread f�r das Empfangen der Daten �ber die sich ge�nderten Status der LSA-Anzeigen
	 * �bertragung ereignisorientiert bei �nderung 
	 */
	private static class Thread_Status extends Thread
	{
		public void run()
		{
			try{
				ServerSocket server_Status = new ServerSocket(adressePort_Status);                 
				Socket clientSocket_Status = server_Status.accept();                 
				ObjectInputStream in_Status = new ObjectInputStream(clientSocket_Status.getInputStream());
				Object o_Status = in_Status.readObject();

				server_Status.close();                 
				clientSocket_Status.close(); 
				
				schreibeDaten_Status(o_Status);      
			}
			catch (IOException e) {} 
			catch (ClassNotFoundException e){}
			
			new Thread_Status().start();
		}
	}
	
	private static void schreibeDaten_Detection(Object o_Detection)
	{
		/*
		String[] empfang_Detection = o_Detection.toString().split(",");
	    Wenn auf der Stelle 0 eine 9999 kommt ist die Simulation beendet. Die Threats m�ssen gestoppt und das Programm beendet werden
		
		if (empfang_Detection[0].equals("9999.0"))  { }
		*/
		try{		   
			BufferedWriter out1 = new BufferedWriter( new OutputStreamWriter(new FileOutputStream( currentDir_Detection, true)));
			out1.write(o_Detection.toString());out1.newLine();
			out1.close();		   
		}
		catch(Exception e) {System.out.print(e.toString());}
	}
	
	private static void schreibeDaten_Status (Object o_Status){
		try {		   
			BufferedWriter out2 = new BufferedWriter( new OutputStreamWriter(new FileOutputStream( currentDir_Status, true)));
			out2.write(o_Status.toString());out2.newLine();
			out2.close();		
		}
		catch(Exception e) {System.out.print(e.toString());}
	}
}





