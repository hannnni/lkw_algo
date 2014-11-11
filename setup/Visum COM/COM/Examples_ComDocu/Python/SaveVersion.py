#-------------------------------------------------------------------------------
# This example create a VISUM-Object and load a version file.
# The length of all links , V0 for privat transport and the time for the
# transportsystem bus are modified an the result will be saved in a new version file.
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

# go over all links
AllLinks = Visum.Net.Links.GetAll
for link in AllLinks:
    # get the length in meter
    # then write new length
    Length = link.AttValue("LENGTH")
    Length = Length * 1.1
    link.SetAttValue("Length", Length)

# save the version
saveVersionPath = public + '\Documents\PTV Vision\PTV Visum 13\Examples\COM\Network\EXAMPLE_SaveVersion.VER'
Visum.SaveVersion(saveVersionPath)

# close Visum
Visum = None
