# Plotting.py


from PyQt4 import QtGui, QtCore
import PandasModel
import pandas as pd
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plot


def plotAllLCS(self):
	figure = plot.figure()
	canvas = FigureCanvas(figure)
	
	xl = pd.ExcelFile("../corpus-final09.xls")
	df = xl.parse("File list")

	colors = ['y-','g-','b-','r-']
	
	labels = [
		'LCS Ratio (No Preprocessing)',
		'LCS Ratio (Light Preprocessing)',
		'LCS Ratio (Advanced Preprocessing)',
		'LCS Ratio (By Sentence, Advanced Pre)'
	]

	figure.suptitle('LCS Ratios / file', fontsize=20)

	ax = figure.add_subplot(111)

	for i in range(0,4): ax.plot(df[labels[i]], colors[i])
	
	handles,labelsX = ax.get_legend_handles_labels()
	ax.legend(handles,labels, loc='lower right')

	ax.set_xlabel('#File')
	ax.set_ylabel('LCS Ratio')
	
	canvas.draw()
	return canvas

def plotRatioOverCategory(self,task):
	xl = pd.ExcelFile("../corpus-final09.xls")
	df = xl.parse("File list")

	categories = ['non','light','heavy','cut']

	dfTask = df.loc[df['Task'] == task]
	
	selectNon = dfTask.loc[df['Category'] == 'non']
	selectLight = dfTask.loc[df['Category'] == 'light']
	selectHeavy = dfTask.loc[df['Category'] == 'heavy']
	selectCut = dfTask.loc[df['Category'] == 'cut']
	
	figure = plot.figure()
	canvas = FigureCanvas(figure)

	ax = figure.add_subplot(111)
	
	figure.suptitle('LCS Ratios / Plagiarism Category', fontsize=20)
	colName = 'LCS Ratio (By Sentence, Advanced Pre)'

	ax.plot(selectNon[colName],'y-')
	ax.plot(selectLight[colName],'g-')
	ax.plot(selectHeavy[colName],'b-')
	ax.plot(selectCut[colName],'r-')

	handles,labelsX = ax.get_legend_handles_labels()

	labels = ['non','light','heavy','cut']
	ax.legend(handles,labels,loc='lower right')
	ax.text(0,0,'TASK '+task,fontsize=15)

	ax.set_xlabel('#File')
	ax.set_ylabel('LCS Ratio')


	canvas.draw()
	return canvas

	# print(select)



