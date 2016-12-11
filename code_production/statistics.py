# Statistics.py


import math

def mean(l):
	return(sum(l)/len(l))

def standard_deviation(l):
	m = mean(l)
	return(math.sqrt(mean((l - m)**2)))