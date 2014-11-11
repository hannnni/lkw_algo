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

# create net element container and put net elements in
NetElementContainer = Visum.CreateNetElements()
Flowbundle = Visum.Net.DemandSegments.ItemByKey('P').Flowbundle
Link = Visum.Net.Links.ItemByKey(11,20)
Node = Visum.Net.Nodes.ItemByKey(12)
NetElementContainer.Add(Link)
NetElementContainer.Add(Node)

# execute flow bundle calculation
Flowbundle.Clear
Flowbundle.Execute(NetElementContainer)

# write version file
saveVersionPath = public + '\Documents\PTV Vision\PTV Visum 13\Examples\COM\Network\EXAMPLE_FlowbundleAnalysis.VER'
Visum.SaveVersion(saveVersionPath)

# close Visum
NetElementContainer = None
Flowbundle = None
Link = None
Node = None
Visum = None