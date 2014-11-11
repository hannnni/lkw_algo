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

# initialize all filters
Visum.Filters.InitAll

# read O-D matrix
DSeg = Visum.Net.DemandSegments.ItemByKey('C')
DSeg.ODMatrix.Open(public + "\Documents\PTV Vision\PTV Visum 13\Examples\COM\Network\PUT.FMA")

# read assignment parameters
Proc = Visum.Procedures
Proc.Open(public + r"\Documents\PTV Vision\PTV Visum 13\Examples\COM\Network\autoequi.par")
Proc.Execute()

# write version file
saveVersionPath = public + '\Documents\PTV Vision\PTV Visum 13\Examples\COM\Network\EXAMPLE_StartAassignment.VER'
Visum.SaveVersion(saveVersionPath)

# close Visum
DSeg = None
Proc = None
Visum = None
