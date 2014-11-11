
#Load library
import numpy

#Function to calculate intrazonal
def calcIntrazonal(mat, factor=0.5):
	"""Set diagonal of matrix as factor * nearest destination zone
	"""
	
	#Copy matrix
	mat = mat.copy()
	
	#Set intrazonal
	for i in range(0,mat.shape[0]):
		mat[i,i] = min(mat[i][mat[i]>0]) * factor
	return mat

##################

#Get skim matrix 1
mat = numpy.array(Visum.Net.SkimMatrices.ItemByKey(2).GetValues())

#Calculate intrazonal
mat = calcIntrazonal(mat, 0.5)

#Return skim to Visum
Visum.Net.SkimMatrices.ItemByKey(2).SetValues(mat)

