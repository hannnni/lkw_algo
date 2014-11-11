#For the currently selected node, add a stop / stop area / stop point
#combination and copy sevearl node attributes over to them

#copy those node attributes to inserted objects - change as needed
coords = ["XCOORD","YCOORD"]
others = ["NAME","CODE","ADDVAL1","ADDVAL2"] 

#Function to copy attributes
def copyAttributes(fromObj, toObj, attrs):
	for attr in attrs:
		toObj.SetAttValue(attr, fromObj.AttValue(attr))

#get currently selected node
oSelection = Visum.Net.Marking 
oSelection.ObjectType = 1 # 1 = Node

if oSelection.Count > 0:
	markedNodes = oSelection.GetAll
	for aNode in markedNodes:
	    no = aNode.AttValue("NO")
  
   	    #Create stop
	    oStop = Visum.Net.AddStop(no)
	    copyAttributes(aNode, oStop, coords)
  	    copyAttributes(aNode, oStop, others)

     	    #Create stop area  
    	    oStopArea = Visum.Net.AddStopArea(no, oStop, aNode)
	    copyAttributes(aNode, oStopArea, coords)
	    copyAttributes(aNode, oStopArea, others)

       	    #Create stop point
	    oStopPoint = Visum.Net.AddStopPointOnNode(no, oStopArea, aNode)
    	    copyAttributes(aNode, oStopPoint, others)
