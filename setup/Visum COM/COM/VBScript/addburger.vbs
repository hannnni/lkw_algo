' for the currently selected node, add a stop / stop area / stop point
' combination and copy selected node attributes over to them

Sub CopyAttributes(fromObj, toObj, attrs)
  for each attr in attrs 
    toObj.AttValue(attr) = fromObj.AttValue(attr)
  next
End Sub

' copy those node attributes to inserted objects
coords = Array ("XCoord", "YCoord")
others = Array ("Name", "Code", "AddVal1", "AddVal2") ' change as needed

' get currently selected node
Set oSelection = Visum.Net.Marking 
oSelection.ObjectType = 1      ' 1 = node

if oSelection.Count > 0 then
  markedNodes = oSelection.GetAll
  For each aNode in markedNodes
    no = aNode.AttValue("NO")
  
    Set oStop = Visum.Net.AddStop(no) 
    CopyAttributes aNode, oStop, coords
    CopyAttributes aNode, oStop, others
  
    Set oStopArea = Visum.Net.AddStopArea(no, oStop, aNode)
    CopyAttributes aNode, oStopArea, coords
    CopyAttributes aNode, oStopArea, others

    Set oStopPoint = Visum.Net.AddStopPointOnNode(no, oStopArea, aNode)
    CopyAttributes aNode, oStopPoint, others
  Next 
end if