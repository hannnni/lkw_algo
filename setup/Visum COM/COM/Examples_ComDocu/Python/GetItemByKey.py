#-------------------------------------------------------------------------------
# This example shows how to access single nodes of a net by using ItemByKey
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

# access node by number (key)
aNode = Visum.Net.Nodes.ItemByKey('10')

print "Code: " + aNode.AttValue("CODE")
print "Name: " + aNode.AttValue("NAME")
print "Type: " + str(aNode.AttValue("TYPENO"))

# delete all objects to close VISUM-software
aNode = None
Visum = None