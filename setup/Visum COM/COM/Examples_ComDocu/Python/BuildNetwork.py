import platform
import win32com.client as com
import os

# create the Visum-Object (connect the variable Visum to the software VISUM)
Visum = com.Dispatch("Visum.Visum.130")

if platform.win32_ver()[1].startswith('5'):
    public = os.environ["ALLUSERSPROFILE"]
else :
    public = os.environ["PUBLIC"]

versionPath = public + '\Documents\PTV Vision\PTV Visum 13\Examples\COM\Network\EXAMPLE.VER'

# clear network for safety
Net = Visum.Net


Net.AddTSystem("Car", "PRT")
Net.AddTSystem("Train", "PUT")
Net.AddTSystem("Walk", "PUTWALK")

# linktypes always exis, just set attribute valuse
linktype20 = Net.LinkTypes.ItemByKey(20)
linktype30 = Net.LinkTypes.ItemByKey(30)
linktype20.SetAttValue("TSYSSET", "Car")
linktype20.SetAttValue("CAPPRT", "800")
linktype20.SetAttValue("V0PRT", "40")
linktype20.SetAttValue("VMAX_PRTSYS(Car)", "40")
linktype30.SetAttValue("TSYSSET", "Car,Train")
linktype30.SetAttValue("CAPPRT", "1000")
linktype30.SetAttValue("V0PRT", "50")
linktype30.SetAttValue("VMAX_PRTSYS(Car)", "50")
linktype30.SetAttValue("VDEF_PUTSYS(Train)", "30")

# nodes
node1 = Net.addnode(1)
node2 = Net.addnode(2)
node3 = Net.addnode(3)
node4 = Net.addnode(4)
node5 = Net.addnode(5)

# set coordinates; default values remain at "0"
node1.SetAttValue("XCOORD", "1000")
node1.SetAttValue("yCOORD", "1000")
node2.SetAttValue("yCOORD", "1000")
node4.SetAttValue("XCOORD", "1000")
node5.SetAttValue("XCOORD", "500")

# links
Net.AddLink(1, 1, 2, 30)
Net.AddLink(2, 2, 3, 30)
Net.AddLink(3, 3, 4, 30)
Net.AddLink(4, 4, 1, 30)
Net.AddLink(5, 1, 5, 20)
Net.AddLink(6, 2, 5, 20)
Net.AddLink(7, 3, 5, 20)
Net.AddLink(8, 4, 5, 20)

# zones an connectors
zone1 = Net.AddZone(1)
zone2 = Net.AddZone(2)
zone1.SetAttValue("NAME", "zone 1")
zone1.SetAttValue("XCOORD", "1100")
zone1.SetAttValue("YCOORD", "1100")
zone2.SetAttValue("NAME", "zone 2")
zone2.SetAttValue("XCOORD", "-100")
zone2.SetAttValue("YCOORD", "-100")
Net.AddConnector(zone1, node1)
Net.AddConnector(zone2, node3)

# stops, stopareas and stoppoints
stop1 = Net.AddStop(1)
stoparea1 = Net.AddStopArea(1,1,1)
stoppoint1 = Net.AddStopPointOnNode(1,1,1)
stop2 = Net.AddStop(2)
stoparea2 = Net.AddStopArea(2,2,3)
stoppoint2 = Net.AddStopPointOnNode(2,2,3)

# line and lineroutes
line1 = Net.AddLine("line 1", "Train")

direction1 = Net.Directions.ItemByKey(">")
direction2 = Net.Directions.ItemByKey("<")

myrouteforward = Visum.CreateNetElements()
myrouteforward.Add(stoppoint1)
myrouteforward.Add(stoppoint2)

myroutebackward = Visum.CreateNetElements()
myroutebackward.Add(stoppoint2)
myroutebackward.Add(stoppoint1)

routesearchparameters = Visum.CreateNetReadRouteSearchTSys()
routesearchparameters.SearchShortestPath(1,False,False, 2,0,1)

lineroute1 = Net.AddLineRoute("lineroute 1", line1, direction1, myrouteforward, routesearchparameters)
lineroute2 = Net.AddLineRoute("lineroute 2", line1, direction2, myroutebackward, routesearchparameters)

# timeprofiles
tp1 = Net.AddTimeProfile("timeprofile 1", lineroute1)
tp2 = Net.AddTimeProfile("timeprofile 2", lineroute2)

tpis = tp1.TimeProfileItems.GetAll
tpi1 = tpis[1]
tpi1.SetAttValue("Arr",120)
tpi1.SetAttValue("Dep",120) #because Dep=Arr at the last TP item
tpis = tp2.TimeProfileItems.GetAll
tpi2 = tpis[1]
tpi2.SetAttValue("Arr",120)
tpi2.SetAttValue("Dep",120)

# write version file
saveVersionPath = public + '\Documents\PTV Vision\PTV Visum 13\Examples\COM\Network\EXAMPLE_BuildNetwork.VER'
Visum.SaveVersion(saveVersionPath)

# close visum

linktype20 = None
linktype30 = None
node1 = None
node2 = None
node3 = None
node4 = None
node5 = None
zone1 = None
zone2 = None
stop1 = None
stop2 = None
stoparea1 = None
stoparea2 = None
stoppoint1 = None
stoppoint2 = None
line1 = None
lineroute1 = None
lineroute2 = None
myrouteforward = None
myroutebackward = None
direction1 = None
direction2 = None
routesearchparameters = None
tp1 = None
tp2 = None
tpis = None
tpi1 = None
tpi2 = None
Visum = None

