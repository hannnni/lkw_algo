#-------------------------------------------------------------------------------
# This example shows how to access the attributes and change the runtime of busses
# according to the volume of cars.
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

# get all Links
AllLinks = Visum.Net.Links.GetAll
for link in AllLinks:
    # read link attributes
    vol = link.AttValue("VolVeh_TSys(C,AP)")
    rtime = link.AttValue("T_PUTSYS(B)")
    length = link.AttValue("Length");

    #calculate new runtime
    rtime = rtime + (vol / 1800) * length

    #write new runtime
    link.SetAttValue("T_PUTSYS(B)",rtime)

# write version file
saveVersionPath = public + '\Documents\PTV Vision\PTV Visum 13\Examples\COM\Network\EXAMPLE_WriteTBus.VER'
Visum.SaveVersion(saveVersionPath)

# delete all objects to close VISUM-software
Visum = None
AllLinks = None
link = None
vol = None
rtime = None
length = None

