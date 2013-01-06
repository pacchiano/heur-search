##### implements functions to unpack the written results by the experiments_engine.py
from os import listdir
from copy import copy
from os.path import isfile, join
from random import random, randint, sample, choice
from Tkinter import *
from time import time
import math
from matplotlib import pyplot as plt
#######################


def unpack_lrta(logfilename, tracks_path):
	logfile = open(logfilename, "r")
	### unpack lrta values
	line = logfile.readline()
	results = dict([])
	tracks = [f for f in listdir(tracks_path) if isfile(join(tracks_path, f)) ]
	focus_track = None
	counter = 0
	while line != "":
		for track in tracks:
			if track in line:
				counter = 1
				results[track] = [None, None, None]
				focus_track = track
				print focus_track

		if counter == 3: ### total_costs
			results[focus_track][0] = eval(line[:-1])
					
		elif counter == 5: ### error_rate
			results[focus_track][1] = eval(line[:-1])

		elif counter == 7: ### total_convergence_error
			results[focus_track][2] = eval(line[:-1])
		line = logfile.readline()
		counter += 1

	return results



def unpack_lrtak(logfilename, tracks_path):
	logfile = open(logfilename, "r")
	### unpack lrta values
	line = logfile.readline()
	results = dict([])
	tracks = [f for f in listdir(tracks_path) if isfile(join(tracks_path, f)) ]
	focus_track = None
	statistics_pack = [None, None, None, None] ### [k, total_costs, error_rate, total_convergence_error]
	counter = 0

	for track in tracks:
		results[track] = []

	while line != "":
		for track in tracks:
			if track in line:
				counter = 1
				tmp_stat_pack = [None, None, None, None]
				focus_track = track
				print focus_track

		if counter == 2 :### k
			tmp_stat_pack[0] = eval(line[:-1])
			
					
		elif counter == 4 :### total_costs
			tmp_stat_pack[1] = eval(line[:-1])
		
		elif counter == 6 :### error_rate
			tmp_stat_pack[2] = eval(line[:-1])
		
		elif counter == 8 :### total_convergence_error
			tmp_stat_pack[3] = eval(line[:-1])
			results[focus_track].append(copy(tmp_stat_pack))
		
		

		line = logfile.readline()
		counter += 1

	return results


################ READ TEST RESULTS #################

lrta_results = unpack_lrta("./lrta_logfile.txt", "./tra")
lrtak_results = unpack_lrtak("./lrtak_logfile.txt", "./tra")
