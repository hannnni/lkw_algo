#-------------------------------------------------------------------------------
# This example shows how to access single nodes of a net by using Item.
# Attention: Item identifies a node by its index in the INodes-Container-Object.
# A Node cannot be uniquely identified through the index, the index is subject
# to change if the VISUM network is altered.
# Accessing by Item should only be used with loops (i.e. processing all available
# nodes).
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
i = 0
while i < len(AllNodes):
    print AllNodes[i].AttValue("NO"), ";",AllNodes[i].AttValue("CODE"), ";",AllNodes[i].AttValue("NAME"), ";", str(AllNodes[i].AttValue("TYPENO"))
    i += 1

# delete all objects to clos VISUM-software
i = None
AllNodes = None
Visum = None