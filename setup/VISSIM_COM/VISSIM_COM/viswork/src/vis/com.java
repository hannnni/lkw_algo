package vis;


/**
 * COM-JAVA-Bridge --> download jacob.jar library
 * link jacob.jar in your used libraries
 * copy jacob-1.16-M1-x86.dll and Interop.VISSIM_COMSERVERLib.dll in C:\windows\system32 folder
 */

/**
 * Anregungungen auch unter blog.naver.com/PostView.nhn?blogId=gckcs2&logNo=10069900534
 */


import com.jacob.activeX.*;
import com.jacob.com.*;
import java.io.*;
import java.util.*;

import vis.tcpip;

public class  com 
{
    
	static tcpip senden = new tcpip();
	
    private ActiveXComponent vissim;
    
    private Dispatch sim; //Simulation
    private Dispatch net; //Simulationsmodell/Netzmodell

    private Dispatch scs; //Signalcontroller/LSA-Nr.
    
    private Dispatch[] det_detection;
    private Dispatch[] scGrp_status;
    

    
    ArrayList<ArrayList<Integer>> scID_Det = new ArrayList<ArrayList<Integer>>(); //Hier befinden sich alle Signalgruppen samt Detektoren drin. dabei ist Position [x][0] immer die LSA-Nummer(ID) und [x][>=1] die Detektoren(ID), die dieser LSA zugeorndet sind
    ArrayList<ArrayList<Integer>> scID_Grp = new ArrayList<ArrayList<Integer>>(); //Hier befinden sich alle Signalgruppen samt Gruppen drin. dabei ist Position [x][0] immer die LSA-Nummer(ID) und [x][>=1] die Signalgruppen(ID), die dieser LSA zugeorndet sind
    
    short[] detection = new short[1]; //Hier befinden sich alle Detektionen der aktuellen Minute bzw. am Ende der Minute der auf die Stunde hochgerechnetet Wert. Die Reihenfolge wird aus scID genommen, nur das hier alle Detektoren hintereinander geschrieben werden
    
    byte[] statusSG = new byte[1]; //Hier befinden sich alle Stati der Signalgruppen der aktuellen Sekunde
    byte[] statusSG_Alt = new byte[1]; //Hier befinden sich alle Status der Signalgruppen der aktuellen Sekunde
    Boolean[] statusSG_Change = new Boolean[1];
    
    /**
     * Einlesen der Detektoren und zugehörigen LSA
     * Vissim starten und ausgewählte Strecke laden (*.inp-Datei)
     * Start Vissim and Load simulationmodell (*.inp-file)
     */
    public void startVissim(String vissimDatei)  //vissimDatei --> path and name of *.inp file
    {
    	/**
         *  Einlesen der Detektoren sowie Signalgruppe und der zugehörigen Lichtsignalanlagen aus der *.inp-Datei       
         */
    	get_SCData(vissimDatei);
    	
		/**
		 * Initialisieren von VISSIM und Laden des Netzmodells (*.inp-Datei)
		 */
    	vissim = new ActiveXComponent("VISSIM.Vissim");
        Dispatch.call((Dispatch)vissim, "LoadNet", vissimDatei, 0);
         
        sim = vissim.getProperty("Simulation").toDispatch();
        net = vissim.getProperty("Net").toDispatch();     
        
        scs = Dispatch.get(net,"SignalControllers").toDispatch();
              
        get_Dispatch_Detection(); //Hier werden die COM-Bridge-Detektoren einmal erstellt bevor die Simulation gestartet wird - dies erspart während der Simulation viel Zeit
        get_Dispatch_Status(); //Hier werden die COM-Bridge-Signalgruppen einmal erstellt bevor die Simulation gestartet wird - dies erspart während der Simulation viel Zeit
    }
    
    /**
     *  Erstellen der COM-Bridge-Detektoren       
     */
    private void get_Dispatch_Detection()
    {
    	Integer zaehler =0;
		for (int i=0; i<scID_Det.size();i++){
	
			Dispatch sc = Dispatch.call(scs, "GetSignalControllerByNumber",scID_Det.get(i).get(0)).toDispatch();
           	Dispatch dets = Dispatch.get(sc,"Detectors").toDispatch();
           	
        	for (int j=1;j<scID_Det.get(i).size();j++)
        	{
        		det_detection[zaehler] = Dispatch.call(dets, "GetDetectorByNumber",scID_Det.get(i).get(j)).toDispatch();
        		zaehler++;
        	}
        }	
    }
    
    /**
     *  Erstellen der COM-Bridge-Signalgruppen
     */
    private void get_Dispatch_Status()
    {
    	Integer zaehler =0;
		for (int i=0; i<scID_Grp.size();i++){
        	
        	Dispatch sc = Dispatch.call(scs, "GetSignalControllerByNumber",scID_Grp.get(i).get(0)).toDispatch();
           	Dispatch scGrps = Dispatch.get(sc,"SignalGroups").toDispatch();
           	
        	for (int j=1;j<scID_Grp.get(i).size();j++)
        	{
        		scGrp_status[zaehler] = Dispatch.call(scGrps, "GetSignalGroupByNumber",scID_Grp.get(i).get(j)).toDispatch();
        		zaehler++;
        	}
        }   
    	
    }
    
    
    /**
     * Auslesen und Setzen der Startzufallszahl - get and set radomseed out of vissim
     * @return Startzufallszahl
     */
    public int getRandomSeed()
    {
        int randomSeed = Integer.parseInt(Dispatch.get(sim, "RandomSeed").toString());
        return randomSeed;
    }
    public void setRandomSeed(int randomSeed)
    {
        Dispatch.put(sim, "RandomSeed", randomSeed);
    }
    
    /**
     * Auslesen  und Setzen der Simulationsdauer - get and set period of simulation out of vissim
     * @return Simulationsdauer
     */
    public double getSimPeriod()
    {
     	double period = Double.parseDouble(Dispatch.get(sim, "Period").toString());
        return period;
    }
    public void setSimPeriod(double period)
    {
        Dispatch.put(sim, "Period", period);
    }
    
    /**
     * Auslesen  und Setzen der Simulationssekunde - get and set simulationsecound out of vissim
     * @return Simulationssekunde
     */
    public double getSimSecond()
    {
        double simSecond = Double.parseDouble(Dispatch.call(sim, "AttValue", "ELAPSEDTIME").toString());
        return simSecond;
    }
    public void setSimSecond(double simSecond)
    {
        Dispatch.put(sim, "ELAPSEDTIME", simSecond);
    }
    
    /**
     * Ermitteln und Setzen der Simulationsschritte pro Simulationssekunde - get and set resolution of simulation out of vissim
     * @return Schritte pro Sekunde
     */
    public double getSimResolution()
    {
        double resolution = Double.parseDouble(Dispatch.get(sim, "Resolution").toString());
        return resolution;
    }
    public void setSimResolution(int resolution)
    {
         Dispatch.put(sim, "Resolution", resolution);
    }
    
    /**
     * Simulation läuft die angegbene Anzahl an Zeitschritten - simulation run specified number of time steps
     */
	Integer sekundenZaehler=0;
    public void run(int simIntervall)
    {
    	sekundenZaehler++;
    	for (int i=0; i<simIntervall; i++)
    	{
    		Dispatch.call(sim, "RunSingleStep");
    	}
    	/**
         * Auslesen der Simulationssekunde aus der Simulation
         */
		int simSekunde = (int)getSimSecond();
    	
    	/**
         * Auslesen der Signalgruppenstatus aus der Simulation
         */
    	
		 
		 getSG_Grp_Status(); //Abfragen des akutellen Status der Signalgruppen
		 Boolean change = get_statusSG_Change(); //Abfragen, ob sich Änderungen zum vorhergehenden Zeitschritt ergeben haben und bei welchen Signalgruppe dies der Fall war - es wird nur gesenden, wenn sich Änderungen ergeben haben
    	 if (change){
    		 senden.sendeDatenSCGrp_Status(simSekunde, statusSG, statusSG_Change, scID_Grp); //senden der sich geänderten Signalgruppen
    	 }

    	/**
         * Auslesen der Detektorereignisse aus der Simulation
         */
		getDetection();

    	/**
         * Minütlich werden die Stundenwerte Extrapoliert und die Detektorzählung genullt
         */	
    	
		if (sekundenZaehler==60){  		
    		//Extrapolation auf einen Stundenwert von Fz/min auf Fz/h
    		for (int i=0; i<detection.length;i++){
    			detection[i]= (short) (detection[i]*60);
    		}
    		
    		//Senden der Stundenwerte
    		senden.sendeDatenSC_Detektion(simSekunde, detection, scID_Det);
    		
    		//Löschen der aktuellen Detektionen
    		for (int i=0; i<detection.length;i++){
    			detection[i]=0;
    		}
    		
    		//Rücksetzen des Minutenzählers
    		sekundenZaehler =0;	
    	}  	
    	
    }
    
    /**
     * Auslesen der Detektorereignisse aus der Simulation
     */
	private void getDetection()
    {	
		for (int i=0;i<detection.length;i++){
			short detectionTemp = Short.parseShort(Dispatch.call(det_detection[i],"AttValue","IMPULSE").toString());
			detection[i]= (short)(detection[i] + detectionTemp);
		}
    }
	
	/**
     * Auslesen der Signalgruppenstatus aus der Simulation
     */
	private void getSG_Grp_Status()
    {
		for (int i=0;i<statusSG.length;i++){
			statusSG[i] = Byte.parseByte(Dispatch.call(scGrp_status[i],"AttValue","STATE").toString());
    		/**
    		 * Statusdefinition von VISSIM
    		 * 0 = Default (means: Use the state of the external controller)
    		 * 1 = Red, 2 = Redamber, 3 = Green, 4 = Amber, 5 = Off, 6 = Undefined,
    		 * 7 = Flashing Amber, 8 = FlashingRed, 9 = Flashing Green, 10 = Flashing Redgreen, 11 = Greenamber, 12 = Off_red
    		 */
		}
    }
	
	/**
     *  Auslesen, ob sich der Status der LSA vom letzten Zeitschritt zum aktuellen Zeitschritt geändert hat
     */
	private Boolean get_statusSG_Change(){
		Boolean rueckgabe = false;
		for (int i =0; i<statusSG.length;i++){
			if (statusSG[i]==statusSG_Alt[i]){
				statusSG_Change[i] = false; 
			}
			else{
				statusSG_Change[i] = true;
				rueckgabe = true;
			}
		}
		statusSG_Alt = new byte[statusSG.length];
		statusSG_Alt = statusSG.clone();
		return rueckgabe;
	}
	
	/**
     *  Einlesen der Detektoren und zugehörigen Lichtsignalanlagen aus der *.inp-Datei       
     */
    private void get_SCData(String vissimDatei){
    	try
    	{
    	    ArrayList<Integer> scID_Detector = new ArrayList<Integer>();
    	    ArrayList<Integer> detectorID = new ArrayList<Integer>();
    	    
    	    ArrayList<Integer> scID_SigGroup = new ArrayList<Integer>();
    	    ArrayList<Integer> groupID = new ArrayList<Integer>();
    		
    	    /**
    	     * Einlesen der *.inp-Datei vor dem Start der Simulation. Nur so kann später während der Simulation Rechenleistung gepart werden, da alle LSA-ID, Detektoren-ID und Signalgruppen-ID bekannt sind
    	     */
    	    File fileName = new File(vissimDatei);
    		FileInputStream fileStream = new FileInputStream(fileName);
    		BufferedInputStream buffStream = new BufferedInputStream(fileStream);
    		DataInputStream dataStream = new DataInputStream(buffStream);

    		while (dataStream.available() != 0) 
    		{          	
    			String currentLine = dataStream.readLine();
    			
    			//Einlesen der LSA-ID und der zugrhörigen Detektoren-ID
    			if (currentLine.startsWith("DETEKTOR"))
    			{
    				int indexStart = currentLine.indexOf("R")+1;
    				int indexStop = currentLine.indexOf("N")-1;
    				detectorID.add(Integer.parseInt(currentLine.substring(indexStart, indexStop).replaceAll(" ","")));
				
    				indexStart = currentLine.indexOf("LSA")+3;
    				indexStop = currentLine.indexOf("FAHRZEUGKLASSEN");
    				scID_Detector.add(Integer.parseInt(currentLine.substring(indexStart, indexStop).replaceAll(" ","")));
		 	    }
    			
    			//Einlesen der LSA-ID und der zugrhörigen Signalgruppen-ID
    			else if (currentLine.startsWith("SIGNALGRUPPE"))
    			{
    				int indexStart = currentLine.indexOf("E")+1;
    				int indexStop = currentLine.indexOf("NAME")-1;
    				groupID.add(Integer.parseInt(currentLine.substring(indexStart, indexStop).replaceAll(" ","")));
				
    				indexStart = currentLine.indexOf("LSA")+3;
    				indexStop = currentLine.length();
    				scID_SigGroup.add(Integer.parseInt(currentLine.substring(indexStart, indexStop).replaceAll(" ","")));
		 	   }   			
    		}
    		
    		/**
    		 * Initialisieren der detection und Beschreiben aller Felder mit 0 - Nur so kann später einfach auf diesen Wert addiert werden und es muss nicht abgefragt werden, ob es schon eine Detektion gab
    		 */
    		det_detection = new Dispatch[detectorID.size()+1];
    		
    		detection = new short[detectorID.size()];
    		for (int i=0; i<detection.length;i++){
    			detection[i]=0;
    		}
    		
    		/**
    		 * Initialisieren der statusSG
    		 */
    		scGrp_status = new Dispatch[scID_SigGroup.size()+1];
    		
    		statusSG = new byte[scID_SigGroup.size()];
    		statusSG_Alt = new byte[scID_SigGroup.size()];
    		statusSG_Change = new Boolean[scID_SigGroup.size()];
    		for (int i=0; i<statusSG.length;i++){
    			statusSG[i]=0;
    			statusSG_Alt[i]=0;
    			statusSG_Change[i]=false;
    		}
    		
    		/**
    		 * Sortierung der DetektorIDs zu den jeweiligen Signalanlagen (LSA-IDS)
    		 */   		
    		while (detectorID.size()!=0)
    		{
    			ArrayList<Integer> temp = new ArrayList<Integer>();
    			int tempscID = scID_Detector.get(0);
    			temp.add(tempscID);
    			temp.add(detectorID.get(0));
    			scID_Detector.remove(0);
    			detectorID.remove(0);	
    			for (int i =0; i<detectorID.size();i++)
    			{
    				if (scID_Detector.get(i).equals(tempscID))
    				{
    	    			temp.add(detectorID.get(i));
    	    			scID_Detector.remove(i);
    	    			detectorID.remove(i);
    	    			i--;
    				}
    			}
    			scID_Det.add(temp);
    		}
    		
    		/**
    		 * Sortierung der SignalgruppenIDs zu den jeweiligen Signalanlagen (LSA-IDS)
    		 */
    		while (groupID.size()!=0)
    		{
    			ArrayList<Integer> temp = new ArrayList<Integer>();
    			int tempscID = scID_SigGroup.get(0);
    			temp.add(tempscID);
    			temp.add(groupID.get(0));
    			scID_SigGroup.remove(0);
    			groupID.remove(0);	
    			for (int i =0; i<groupID.size();i++)
    			{
    				if (scID_SigGroup.get(i).equals(tempscID))
    				{
    	    			temp.add(groupID.get(i));
    	    			scID_SigGroup.remove(i);
    	    			groupID.remove(i);
    	    			i--;
    				}
    			}
    			scID_Grp.add(temp);
    		}
    	}
    	catch (IOException e) {}
    }
}