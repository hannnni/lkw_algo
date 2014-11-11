#-------------------------------------------------------------------------------
# This example shows how to access single nodes with For-Each-Loop.
#-------------------------------------------------------------------------------
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

# get all Nodes
AllNodes = Visum.Net.Nodes.GetAll

# print table header for output
print "Node number;Code;Name;Type"

# access all Nodes
for node in AllNodes:
    print node.AttValue("NO"), ";",node.AttValue("CODE"), ";",node.AttValue("NAME"), ";", str(node.AttValue("TYPENO"))


# delete all objects to clos VISUM-software
node = None
AllNodes = None
Visum = None