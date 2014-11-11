package vis;

import java.io.*;
import java.util.ArrayList;

public class start {

	static com vw = new com();
	static tcpip senden = new tcpip();
	
	static String pfadVissim = null;
	static int simDauer =0;
	static int simStartzufallszahl=0;
	static int simIntervall=0;
	
	public static void main(String[] args) {
	
		/**
		 * Einlesen der Konfigurationsdatei - IP, Port an die gesendet werden soll und Pfad, wo die VISSIM *.inp-Datei zu finden ist
		 */
		System.out.println("Start");
		try{
			BufferedReader in = new BufferedReader(new FileReader("config_COM.txt"));
			String zeile = null;
			while ((zeile = in.readLine()) != null) 
			{
				if (zeile.equals("Pfad der VISSIM-Datei")) { pfadVissim = in.readLine(); }
				else if (zeile.equals("IP an die gesendet werden soll")) { senden.set_adresseIP(in.readLine());}
				else if (zeile.equals("Port auf dem die Detektordaten gesendet werden sollen")) {senden.set_adressePort_Detection(Integer.parseInt(in.readLine())); }
				else if (zeile.equals("Port auf dem die Statusdaten der Signalgruppe gesendet werden sollen")) {senden.set_adressePort_Status(Integer.parseInt(in.readLine())); }
				else if (zeile.equals("Simulationsdauer")) {simDauer = Integer.parseInt(in.readLine()); }
				else if (zeile.equals("Startzufallszahl")) {simStartzufallszahl = Integer.parseInt(in.readLine()); }
				else if (zeile.equals("Zeitschritte je Sekunde")) {simIntervall = Integer.parseInt(in.readLine()); }
			}
		}
		catch(Exception e) {System.out.print(e.toString());}

		/**
		 * Initialisieren von VISSIM inklusive der JAVA-COM-Bridge und Laden des Netzmodells (*.inp-Datei)
		 */
		vw.startVissim(pfadVissim);
		
		/**
		 * Setzen der Simulationsparameter
		 */
		vw.setRandomSeed(simStartzufallszahl); //Setzen der Startzufallszahl
		vw.setSimPeriod(simDauer); //Setzen der Simulationsdauer
		vw.setSimResolution(simIntervall); //Setzen Simulationsschritte je Sekunde - Simulationsintervall
		
		/**
		 * Simulationsdurchlauf und das Auslesen der Detektorwerte
		 */
		int i = 0;
		while (i <= simDauer) {   
			vw.run(simIntervall); //Simulation l�uft eine Sekunde (1s) voran
			i++;                         
        }
		
		//senden beenden
		ArrayList<Integer> ende = new ArrayList<Integer>();
		ende.add(9999);
		senden.send_tcp_ip_Detection(ende);
	}
}

