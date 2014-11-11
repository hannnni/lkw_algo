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

# get ILinks object
LinkList = Visum.Net.Links
# create Iterator object
LinkIter = LinkList.Iterator

while LinkIter.Valid:
    CurLink = LinkIter.Item
    CurLink.SetAttValue("CAPPRT", CurLink.AttValue("CAPPRT") * 2)
    LinkIter.Next()

# write version file
saveVersionPath = public + '\Documents\PTV Vision\PTV Visum 13\Examples\COM\Network\EXAMPLE_Iterator.VER'
Visum.SaveVersion(saveVersionPath)

# delete all objects to close VISUM-software
LinkList = None
LinkIter = None
CurLink = None
Visum = None