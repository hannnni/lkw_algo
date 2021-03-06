package vis;

import java.io.*;
import java.net.*;
import java.util.ArrayList;
//import java.util.concurrent.*;

public class tcpip {

	//private static ExecutorService executorService = Executors.newSingleThreadExecutor();
	
	/**
	 * Setzen des Ports auf dem die TCP/IP-Verbindung senden soll
	 */
	static int adressePort_Detection = 9999;
	static int adressePort_Status = 9998;
	static String adresseIP = "127.0.0.1";
	
	public void set_adressePort_Detection (int port){
		adressePort_Detection =port;
	}
	public void set_adressePort_Status (int port){
		adressePort_Status =port;
	}
	public void set_adresseIP (String ip){
		adresseIP = ip;
	}
	
	
	/**
	 * Erstellen des Sendestreams f�r die Daten der Signalgruppenstatus
	 */
	public void sendeDatenSCGrp_Status(int simSekunde, byte[] statusSG, Boolean[]statusSG_Change, ArrayList<ArrayList<Integer>> scID_Grp)
	{
		ArrayList<Integer> tempSendeListe = new ArrayList<Integer>();
		tempSendeListe.add(simSekunde);
		int zaehler =0;
		
		for (int i=0; i<scID_Grp.size();i++){          	
        	for (int j=1;j<scID_Grp.get(i).size();j++)
        	{
        		if (statusSG_Change[zaehler]){  //wird nur gesendet, wenn sich im Status der Signalgruppe auch �nderungen ergeben haben
        			tempSendeListe.add(scID_Grp.get(i).get(0));
        			tempSendeListe.add(scID_Grp.get(i).get(j));
        			tempSendeListe.add((int)statusSG[zaehler]);
        		}
        		zaehler++;
        	}
		}
		send_tcp_ip_Status(tempSendeListe);
		//diese Liste enth�lt [Zeitstempel, LSA-ID, Signalgruppen-ID, q[Fz/h], LSA-ID, Signalgruppen-ID, q[Fz/h], ... , LSA-ID, Signalgruppen-ID, q[Fz/h]]
	}
	
	/**
	 * Erstellen des Sendestreams f�r die Daten der Detektorereignisse
	 */
	public void sendeDatenSC_Detektion(int simSekunde, short[] detection, ArrayList<ArrayList<Integer>> scID_Det)
	{
		ArrayList<Integer> tempSendeListe = new ArrayList<Integer>();
		tempSendeListe.add(simSekunde);
		int zaehler =0;
		
		for (int i=0; i<scID_Det.size();i++){          	
        	for (int j=1;j<scID_Det.get(i).size();j++)
        	{
        		tempSendeListe.add(scID_Det.get(i).get(0));
        		tempSendeListe.add(scID_Det.get(i).get(j));
        		tempSendeListe.add((int)detection[zaehler]);
        		
        		zaehler++;
        	}
		}
		send_tcp_ip_Detection(tempSendeListe);
		//diese Liste enth�lt [Zeitstempel, LSA-ID, Detektor-ID, q[Fz/h], LSA-ID, Detektor-ID, q[Fz/h], ... , LSA-ID, Detektor-ID, q[Fz/h]]
	}
	
	
	
	
	/**
	 * Senden der Daten �ber TCP/IP an einen anderen Rechner
	 */
	public void send_tcp_ip_Detection(ArrayList<Integer> sendeListe)
	{
		try {
			Socket sock = new Socket();       
			sock.connect(new InetSocketAddress(adresseIP,adressePort_Detection));       
			ObjectOutputStream out = new ObjectOutputStream(sock.getOutputStream());         
			out.writeObject(sendeListe);         
			sock.close(); 
		}
	    catch(Exception e) {
	     	System.out.print("Whoops! It didn't work!\n");
	    }
	}
	
	public void send_tcp_ip_Status(ArrayList<Integer> sendeListe)
	{
		try {
			Socket sock = new Socket();       
			sock.connect(new InetSocketAddress(adresseIP,adressePort_Status));       
			ObjectOutputStream out = new ObjectOutputStream(sock.getOutputStream());         
			out.writeObject(sendeListe);         
			sock.close(); 
		}
	    catch(Exception e) {
	      	System.out.print("Whoops! It didn't work!\n");
	    }
	}
}
