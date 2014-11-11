import platform
import win32com.client as com
import os
import VisumPy

# create the Visum-Object (connect the variable Visum to the software VISUM)
Visum = com.Dispatch("Visum.Visum.130")

if platform.win32_ver()[1].startswith('5'):
    public = os.environ["ALLUSERSPROFILE"]
else :
    public = os.environ["PUBLIC"]

versionPath = public + '\Documents\PTV Vision\PTV Visum 13\Examples\COM\Network\EXAMPLE.VER'

# load version
Visum.LoadVersion(versionPath)

# create AddNetRead-Object and specify desired conflict avoiding method
AddNetReadController = Visum.CreateAddNetReadController
AddNetReadController.SetConflictAvoidingForAll(10000,"tra_")

# create NetRouteSearchTSys-Object and choose route search options
# create one object per TSys if desired
NetReadRouteSearchTSysController = Visum.CreateNetReadRouteSearchTSys()
NetReadRouteSearchTSysController.DontRead()

# create NetRouteSearch-Object and assign NetRouteSearchTSys-objects
NetReadRouteSearchController = Visum.CreateNetReadRouteSearch()
NetReadRouteSearchController.SetForAllTSys(NetReadRouteSearchTSysController)

# additively read the net file, filename from cell B4
Visum.LoadNet(public + '\Documents\PTV Vision\PTV Visum 13\Examples\COM\Network\EXAMPLE.net', True,NetReadRouteSearchController, AddNetReadController)

# write version file
saveVersionPath = public + '\Documents\PTV Vision\PTV Visum 13\Examples\COM\Network\EXAMPLE_AddNetRead.VER'
Visum.SaveVersion(saveVersionPath)

# close Visum
Visum = None
