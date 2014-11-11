#-------------------------------------------------------------------------------
# This Example shows how to access routes of an assignment calculation.
# For each route are listed the following values: number of nodes, length,
# running time, origin zone, destination zone and the id of all
# nodes.
#-------------------------------------------------------------------------------
import platform
import win32com.client as com
import os
import numpy

# create the Visum-Object (connect the variable Visum to the software VISUM)
Visum = com.Dispatch("Visum.Visum.130")

if platform.win32_ver()[1].startswith('5'):
    public = os.environ["ALLUSERSPROFILE"]
else :
    public = os.environ["PUBLIC"]

versionPath = public + '\Documents\PTV Vision\PTV Visum 13\Examples\COM\Network\EXAMPLE.VER'

# load version
Visum.LoadVersion(versionPath)

# get the demand segment code
DSeg = Visum.Net.DemandSegments.ItemByKey('C')

# get first O-Zone for use in SetObjects-statement
Iter = Visum.Net.Zones.Iterator
OZone = Iter.Item

PathList = Visum.Lists.CreatePrTPathList
PathList.AddColumn("OrigZoneNo")
PathList.AddColumn("DestZoneNo")
PathList.AddColumn("Index")
PathList.AddColumn("Vol(AP)")
PathList.AddColumn("tCur")
PathList.AddColumn("Length")

# get PrTPathlist
print "Origin;Destination;Route Number;NumNodes;Length [m];Time [s];Volume;Nodes"
i = 0
List = PathList.SaveToArray()
while i < len(List):
    NodeList = DSeg.GetPathNodes(List[i][0],List[i][1],List[i][2])
    AllNodes = NodeList.GetAll
    FromNode = AllNodes[1].AttValue("No")
    TheNodes = str(FromNode)
    j = 0
    while j < len(AllNodes):
        ToNode = AllNodes[j].AttValue("No")
        TheNodes = TheNodes + " - " + str(ToNode)
        j += 1
    print List[i][0], ";",List[i][1],";",List[i][2],";",len(AllNodes),";",List[i][5],";",List[i][4],";",List[i][3], ";",TheNodes
    i+=1

# close Visum
DSeg = None
AllNodes = None
FromNode = None
ToNode = None
TheNodes = None
PathList = None
NodeList = None
List = None
OZone = None
Iter = None
Visum = None
