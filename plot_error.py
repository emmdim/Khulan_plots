import os
import ipdb

import pandas as pd
import matplotlib as mpl
from matplotlib import pyplot as plt
import numpy as np
import seaborn as sns

##PARAMETERS
EXP_NAME = 'test'
MAX_ROUNDS = 699
MAX_YVAL = 14
# DEFINE OUTPUT DIR
RESULTS_DIR = os.path.join( os.getcwd(),'results',EXP_NAME)
GRAPHS_DIR = os.path.join( os.getcwd(), 'graphs',EXP_NAME)

##SET SEABORN STYLE
sns.set_style("whitegrid")
sns.set_context("paper")

##SET MATPLOTLIB STYLE
TICKS_FONTSIZE = 16
LABEL_FONTSIZE=18
LEGEND_FONTSIZE=15

mpl.rcParams['xtick.labelsize'] = TICKS_FONTSIZE 
mpl.rcParams['ytick.labelsize'] = TICKS_FONTSIZE
mpl.rcParams['legend.fontsize'] = TICKS_FONTSIZE
mpl.rcParams['axes.labelsize'] = LABEL_FONTSIZE
mpl.rcParams['axes.titlesize'] = LABEL_FONTSIZE
mpl.rcParams['font.size'] = LABEL_FONTSIZE
plt.rc('legend',**{'fontsize':LEGEND_FONTSIZE})


######################### BASIC FUNCTIONS  ###########################
#######################################################################


def read_results():
	"""Reads the results for all the nodes and returns
	a list of pandas Dataframes, one for each node"""
	#Get list of nodes(files) with results
	nodes = [f for f in os.listdir(RESULTS_DIR) if os.path.isfile(os.path.join(RESULTS_DIR, f))]
	#Load results from each node
	nodes_results = {}
	for node in nodes:
		f = os.path.join(RESULTS_DIR,node)
		try:
			nodes_results[node] = pd.read_csv(f)
			nodes_results[node] = nodes_results[node].replace('None',np.nan)
		except Exception, e:
			ipdb.set_trace()
	return nodes_results

def plot_var_per_round(results, var):
	"""Plot the median acrros nodes of a variable"""
	median = getMedianDF(results,var)
	#Create new figure
	fig = plt.figure()
	#Print the plot
	median.plot()
	#Modify parameters
	plt.ylabel(var)
	plt.xlabel('rounds')
	plt.xlim(0,MAX_ROUNDS)
	plt.ylim(0,MAX_YVAL)
	#Dummy line to avoid bug of matplotlib that closes image right after plot
	#It's a readline function, just press enter
	raw_input('Done')
	#You can also automatically save figures
	fig.savefig(os.path.join(GRAPHS_DIR,var.replace(' ','_')+'_per_round.png'), format='png', dpi=fig.dpi)
	

def plot_var_ecdf_per_round(results, var):
	"""Plot the ECDF of the median accross the nodes of a variable"""
	median = getMedianDF(results,var)
	ecdf = getECDF(median)
	ecdf.plot()
	plt.xlabel(var)
	plt.ylabel('ECDF')
	plt.xlim(0,MAX_YVAL)
	plt.show()
	raw_input('Done')

def plot_comparative(results,variables):
	
	# Get median time series for all varibales
	medians = [getMedianDF(results,var) for var in variables]
	df = pd.concat(medians,axis=1)
	df.plot()
	plt.ylabel('Error')
	plt.xlim(0,MAX_ROUNDS)
	plt.ylim(0,MAX_YVAL)
	plt.show()
	raw_input('Done')




############################### HELPERS  ##############################
#######################################################################

def getMedianDF(nodes_results,var):
	""""Helper function that extracts median time series of the var
	accross the various nodes"""
	series = []
	for name,r in nodes_results.iteritems():
		#Normalize duplicate rounds
		r['round'] = r['round'].apply(np.trunc)
		s = r.groupby('round',axis=0).mean()[var]
		s.name = name
		series.append(s)
	try:
		df = pd.concat(series,axis=1)
	except:
		ipdb.set_trace()
	median = df.median(axis=1)
	median.name = var
	return median



def getECDF(df):
	"""Helper function that caclulates the ECDF of a
	dataframe"""
	df = df.sort_values().value_counts()
	ecdf = df.sort_index().cumsum()*1./df.sum()
	return ecdf

##########################  MAIN  #######################################
#######################################################################


if __name__ == '__main__':
	nodes_results = read_results()
	plot_var_per_round(nodes_results,'HTTP Error')
	#plot_var_ecdf_per_round(nodes_results,'HTTP Error')
	#plot_comparative(nodes_results,['HTTP Error', 'UDP Error'])

