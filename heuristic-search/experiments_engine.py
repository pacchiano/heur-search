from os import listdir
from os.path import isfile, join
from random import random, randint, sample, choice
from Tkinter import *
from time import time
import math
from matplotlib import pyplot as plt
### local imports
from track_extract_final import extract_track
from landscape import structuredSpace


def analyze_lrta(logfilename, tracks_path, use_manhattan, iterations):
	tracks = [f for f in listdir(tracks_path) if isfile(join(tracks_path, f)) ]
	
	logfile = open(logfilename, "w")

	for track in tracks:
		### construct track
		(states, start, display) = extract_track(tracks_path + "/" + track,  use_manhattan) ### recall: True as argument means a manhattan distance.
		experimental_space = structuredSpace(states, start)
		total_costs = []
		total_convergence_error = [] ### stores the total deviation. 

		print track
		### test for lrta
		for i in range(iterations):
			total_convergence_error.append(experimental_space.get_total_error())
			total_costs.append(experimental_space.simulate_space_lrta(start))  #### lrta run
			if i%5 == 0:
				print i

		error_rate = [total_convergence_error[0]] + [total_convergence_error[i] - total_convergence_error[i-1] for i in range(len(total_convergence_error))]
		### write results
		logfile.write(track)
		logfile.write("\n")
		logfile.write("total_costs")
		logfile.write("\n")	
		logfile.write(str(total_costs))
		logfile.write("\n")
		logfile.write("error_rate")
		logfile.write("\n")	
		logfile.write(str(error_rate))
		logfile.write("\n")
		logfile.write("total_convergence_error")
		logfile.write("\n")
		logfile.write(str(total_convergence_error))
		logfile.write("\n")

	logfile.close()

def analyze_lrtak_old(logfilename, tracks_path, use_manhattan, max_k, iterations):
	tracks = [f for f in listdir(tracks_path) if isfile(join(tracks_path, f)) ]
	logfile = open(logfilename, "w")

	for track in tracks:
		### construct track
		(states, start, display) = extract_track(tracks_path + "/" + track,  use_manhattan) ### recall: True as argument means a manhattan distance.
		print track
		### test for lrtak
		for k in range(1, max_k+1):
			experimental_space = structuredSpace(states, start)
			total_costs = []
			total_convergence_error = [] ### stores the total deviation. 
			for i in range(iterations):
				total_convergence_error.append(experimental_space.get_total_error())
				total_costs.append(experimental_space.simulate_space_lrta_old(k, start)) #### lrtak old run
				if i%5 == 0:
					print i

			error_rate = [total_convergence_error[0]] + [total_convergence_error[i] - total_convergence_error[i-1] for i in range(len(total_convergence_error))]
			### write results
			logfile.write(track)
			logfile.write("\n")
			logfile.write(str(k))
			logfile.write("\n")
			logfile.write("total_costs")
			logfile.write("\n")	
			logfile.write(str(total_costs))
			logfile.write("\n")
			logfile.write("error_rate")
			logfile.write("\n")	
			logfile.write(str(error_rate))
			logfile.write("\n")
			logfile.write("total_convergence_error")
			logfile.write("\n")
			logfile.write(str(total_convergence_error))
			logfile.write("\n")


	logfile.close()


def analyze_lrtak_new(logfilename, tracks_path, use_manhattan, max_k, iterations):
	tracks = [f for f in listdir(tracks_path) if isfile(join(tracks_path, f)) ]
	logfile = open(logfilename, "w")

	for track in tracks:
		### construct track
		(states, start, display) = extract_track(tracks_path + "/" + track,  use_manhattan) ### recall: True as argument means a manhattan distance.
		print track
		### test for lrtak
		for k in range(1, max_k+1):
			experimental_space = structuredSpace(states, start)
			total_costs = []
			total_convergence_error = [] ### stores the total deviation. 
			for i in range(iterations):
				total_convergence_error.append(experimental_space.get_total_error())
				total_costs.append(experimental_space.simulate_space_lrtak_new(k, start)) #### lrtak new run
				if i%5 == 0:
					print i

			error_rate = [total_convergence_error[0]] + [total_convergence_error[i] - total_convergence_error[i-1] for i in range(len(total_convergence_error))]
			### write results
			logfile.write(track)
			logfile.write("\n")
			logfile.write(str(k))
			logfile.write("\n")
			logfile.write("total_costs")
			logfile.write("\n")	
			logfile.write(str(total_costs))
			logfile.write("\n")
			logfile.write("error_rate")
			logfile.write("\n")	
			logfile.write(str(error_rate))
			logfile.write("\n")
			logfile.write("total_convergence_error")
			logfile.write("\n")
			logfile.write(str(total_convergence_error))
			logfile.write("\n")


	logfile.close()


####################### RUN TESTS ##########################

logfilename = "lrta_logfile.txt"
tracks_path = "./tra"
use_manhattan = False
iterations = 500
print "LRTA"
analyze_lrta(logfilename, tracks_path, use_manhattan, iterations)

logfilename = "lrta_logfile_manhattan.txt"
tracks_path = "./tra"
use_manhattan = True
iterations = 500
print "Manhattan LRTA"
analyze_lrta(logfilename, tracks_path, use_manhattan, iterations)


logfilename = "lrtak_logfile.txt"
tracks_path = "./tra"
use_manhattan = False
iterations = 500
max_k = 100
print "Single LRTAK"
analyze_lrtak_new(logfilename, tracks_path, use_manhattan, max_k, iterations)

logfilename = "lrtak_logfile_manhattan.txt"
tracks_path = "./tra"
use_manhattan = True
iterations = 500
max_k = 100
print "Manhattan LRTAK"
analyze_lrtak_new(logfilename, tracks_path, use_manhattan, max_k, iterations)



