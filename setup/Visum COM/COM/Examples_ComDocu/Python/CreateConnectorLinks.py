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

# load version
Visum.LoadVersion(versionPath)

# get minimum link number of inserted links
linkNos = Visum.Net.Links.GetMultiAttValues("NO", True)
nextLinkNo = 0
i = 0
while i < len(linkNos):
    if linkNos[i] > nextLinkNo:
        nextLinkNo = linkNos[i][1]
    i += 1
nextLinkNo += 1000

# get minimum node number for inserted links
nodeNos = Visum.Net.Nodes.GetMultiAttValues("NO", True)
nextNodeNo = 0
i = 0
while i < len(nodeNos):
    if nodeNos[i] > nextNodeNo:
        nextNodeNo = nodeNos[i][1]
    i += 1

nextNodeNo += 1000

# get linktype used for additional links
linktype = 99

# for each connector create a node, a link
# and a new connector

oldConnectors = Visum.Net.Connectors.GetAll
i = 0
while i < len(oldConnectors):
    oldConn = oldConnectors[i]

    #claculate coordinates for intermediate node
    zoneX = oldConn.AttValue("ZONE\XCOORD")
    zoneY = oldConn.AttValue("ZONE\YCOORD")
    nodeX = oldConn.AttValue("NODE\XCOORD")
    nodeY = oldConn.AttValue("NODE\YCOORD")
    viaX = (zoneX + nodeX) / 2
    viaY = (zoneY + nodeY) / 2

    # get referenced objects
    thezone = Visum.Net.Zones.ItemByKey(oldConn.AttValue("ZONE\NO"))
    thenode = Visum.Net.Nodes.ItemByKey(oldConn.AttValue("NODE\NO"))

    # create viaNode
    viaNode = Visum.Net.AddNode(nextNodeNo)
    nextNodeNo += 1
    viaNode.SetAttValue("XCOORD", viaX)
    viaNode.SetAttValue("YCOORD", viaY)

    # create new Connector
    Visum.Net.AddConnector(thezone, viaNode)

    # create newLink
    newLink = Visum.Net.AddLink(nextLinkNo, viaNode, thenode)
    nextLinkNo += 1
    newLink.SetAttValue("TYPENO",linktype)

    # delete old connector
    Visum.Net.RemoveConnector(oldConn)
    i += 2

# write version file
saveVersionPath = public + '\Documents\PTV Vision\PTV Visum 13\Examples\COM\Network\EXAMPLE_CreateConnector.VER'
Visum.SaveVersion(saveVersionPath)

# close visum
oldConnectors = None
oldConn = None
thezone = None
thenode = None
newLink = None
viaNode = None
Visum = None
