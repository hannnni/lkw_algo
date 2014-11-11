
#PrT Assignment Convergence Chart to Excel
#Ben Stabler, bstabler@ptvamerica.com

import numpy
import VisumPy.excelplot

assignList = Visum.Lists.CreatePrTAssQualityList
assignList.AddColumn("Iteration")
assignList.AddColumn("RelativeGap")
data = assignList.SaveToArray() #assignList.saveToClipboard(9)

iterations = max(numpy.array(data)[:,0])
relgap = list(numpy.array(data)[:,1])

assignList = Visum.Lists.CreatePrTAssQualityList
assignList.AddColumn("DSegCode")
dataDSeg = map(list, assignList.SaveToArray())

plotData = dict()
for i in range(0, len(dataDSeg)):
	if not plotData.has_key(dataDSeg[i][0]):
		plotData[dataDSeg[i][0]] = list()
	plotData[dataDSeg[i][0]].append(relgap[i])

chart = VisumPy.excelplot.Chart('Assignment Convergence', 'Iteration', 'Relative Gap')

for i in range(0, len(plotData.keys())):
	chart.addSeries(range(0, iterations + 1), plotData[plotData.keys()[i]], plotData.keys()[i])
	
chart.chart.ChartType = 65 #line
chart.chart.Axes().Item(2).MaximumScale = 0.1 
chart.chart.Axes().Item(2).ScaleType = -4133 #log scale code
chart.show()