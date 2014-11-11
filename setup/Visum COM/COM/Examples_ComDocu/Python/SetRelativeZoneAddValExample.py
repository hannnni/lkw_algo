import platform
import win32com.client as com
import os
import numpy


# create the Visum-Object (connect the variable Visum to the software VISUM)
Visum = com.Dispatch("Visum.Visum.130")

if platform.win32_ver()[1].startswith('5'):
    public = os.environ["ALLUSERSPROFILE"]
else :
    public = os.environ["PUBLIC"]

versionPath = public + '\Documents\PTV Vision\PTV Visum 13\Examples\COM\Network\EXAMPLE.VER'

# load version
Visum.LoadVersion(versionPath)

# get attribute array of AddVal1 values
Result = numpy.array(Visum.Net.Zones.GetMultiAttValues("AddVal1", False))

print Result[0][0].__class__
print Result[0][1].__class__

# read the attribute arary
i = 0
Sum = 0
while i < len(Result):
    Sum = Sum + Result[i][1]
    i += 1

if Sum == 0:
    Sum = 1

#change values in the array to relative values
i = 0
while i < len(Result):
    Result[i][1] = Result[i][1] * 100 / Sum
    i += 1

#write attribute array
Visum.Net.Zones.SetMultiAttValues("AddVal1", Result, False)

# write version file
saveVersionPath = public + '\Documents\PTV Vision\PTV Visum 13\Examples\COM\Network\EXAMPLE_SetRelativeZoneAddVal.VER'
Visum.SaveVersion(saveVersionPath)

# close Visum
Result = None
Visum = None


