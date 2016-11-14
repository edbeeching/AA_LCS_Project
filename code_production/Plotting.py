# Plotting.py


from PyQt4 import QtGui, QtCore
import PandasModel
import pandas as pd
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plot
import numpy as np
import Statistics as stats





###############################################
#                  PIE CHART                  #
###############################################
def init_pieChart():
	figure = plot.figure()
	update_pieChart(figure,100,50) # to remove
	return figure

def update_pieChart(figure,length,lengthLCS):
	# figure.clear()
	# figure = plot.figure()
	# canvas = FigureCanvas(figure)

	ax = figure.add_subplot(111)
	ax.clear()
	
	labels = ['Original','Copied']
	plagiarismPercentage = (lengthLCS / (length * 1.0))
	print ('\n')
	p2 = int(100 * plagiarismPercentage)
	p1 = int(100 - p2)
	sizes = [p1,p2]
	print (p1)
	print (p2)
	colors = ['green','red']

	ax.pie(
		sizes,
		colors=colors,
		autopct='%1.1f%%',
		startangle=90
	)
	ax.axis('equal')
	patches, texts = ax.pie(sizes, colors=colors, startangle=90)
	ax.legend(patches, labels, loc="best")

	# canvas.draw()
	# return canvas





#################################################
#                  FIRST GRAPH                  #
#################################################

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



##################################################
#                  SECOND GRAPH                  #
##################################################


def subplotByCategoryLabels(self,axIn,axOut):
	handles,labelsX = axIn.get_legend_handles_labels()
	labels = ['non','light','heavy','cut']
	axOut.legend(handles,labels,loc='center')
	axOut.get_xaxis().set_visible(False)
	axOut.get_yaxis().set_visible(False)
	axOut.set_title('legend')

def subplotByCategory(self,task,ax):
	xl = pd.ExcelFile("../corpus-final09.xls")
	df = xl.parse("File list")
	dfTask = df.loc[df['Task'] == task]
	selectNon = dfTask.loc[df['Category'] == 'non']
	selectLight = dfTask.loc[df['Category'] == 'light']
	selectHeavy = dfTask.loc[df['Category'] == 'heavy']
	selectCut = dfTask.loc[df['Category'] == 'cut']

	colName = 'LCS Ratio (By Sentence, Advanced Pre)'
	ax.plot(selectNon[colName],'yo')
	ax.plot(selectLight[colName],'gs')
	ax.plot(selectHeavy[colName],'b^')
	ax.plot(selectCut[colName],'rD')
	
	ax.set_xlabel('#File')
	ax.set_ylabel('LCS Ratio')
	
	ax.set_title('Task '+task)

def plotByCategory(self):
	figure = plot.figure()
	canvas = FigureCanvas(figure)

	figure.suptitle('LCS Ratios / Plagiarism Category', fontsize=20)
	
	ax1 = figure.add_subplot(231)
	subplotByCategory(self,'a',ax1)

	ax2 = figure.add_subplot(232)
	subplotByCategory(self,'b',ax2)

	ax3 = figure.add_subplot(233)
	subplotByCategory(self,'c',ax3)

	ax4 = figure.add_subplot(234)
	subplotByCategory(self,'d',ax4)

	ax5 = figure.add_subplot(235)
	subplotByCategory(self,'e',ax5)

	ax6 = figure.add_subplot(236)
	subplotByCategoryLabels(self,ax1,ax6)


	plot.tight_layout()
	figure = plot.gcf()

	canvas.draw()
	return canvas


#################################################
#                  THIRD GRAPH                  #
#################################################

def plotByCategory2(self):
	figure = plot.figure()
	canvas = FigureCanvas(figure)

	xl = pd.ExcelFile("../corpus-final09.xls")
	df = xl.parse("File list")

	colName = 'LCS Ratio (By Sentence, Advanced Pre)'

	# selectNon = df.loc[df['Category'] == 'non']
	
	categories = ['non','light','heavy','cut']
	colors = ['y.','g.','b.','r.']

	ax = figure.add_subplot(111)
	ax.axis([-1,4,0,1.2])

	values = []
	means = []
	std_devs = []
	for x in range(0,4):
		values.append(df.loc[df['Category'] == categories[x]][colName])
		ax.plot(len(values[x])*[x],values[x],colors[x])
		m = stats.mean(values[x])
		std = stats.standard_deviation(values[x])
		m_str = str('%.3f' % round(m,3))
		std_str = str('%.3f' % round(std,3))
		ax.text((x+.1),m,'mean = '+m_str+'\nstd =  '+std_str)


	handles,labelsX = ax.get_legend_handles_labels()
	ax.legend(handles,categories,loc='lower right')

	ax.yaxis.grid()
	ax.xaxis.set_ticklabels(['','non','light','heavy','cut',''])

	canvas.draw()
	return canvas




