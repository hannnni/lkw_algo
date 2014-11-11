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

# create empty link list
LinkList = Visum.Lists.CreateLinkList

# select objects to be shown in list. Here: only active links
LinkList.SetObjects(True)

# select columns to be shown in list
# include all key columns to get a re-readble attribute file
LinkList.AddKeyColumns
LinkList.AddColumn("TSYSSET")

# length of DSeg X, transport system "Bus", analysis horizon
LinkList.AddColumn("VOLPERS_DSEG_TSYS(P-B,AH)")

# save list to attribute file
LinkList.SaveToAttributeFile(public + r"\Documents\PTV Vision\PTV Visum 13\Examples\COM\Network\LINKLIST.ATT", 59)

LinkList = None
Visum = None